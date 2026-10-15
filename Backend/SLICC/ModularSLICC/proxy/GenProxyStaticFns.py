import re

from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.common.GenMachineStruct import GenMachineStruct


class GenProxyStaticFns(TemplateHandler):
    template_file = "proxy_static_functions.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_static_fns_str(self, arch: FlatArchitecture, machine_id: str,
                                 parked: 'dict[str, list[str]]' = None) -> str:
        const_str = "//" + __name__ + self.nl
        fns = self.string_repl_keys(self.open_template(GenProxyStaticFns.template_file),
                                    [str(arch.init_state),
                                     Util.get_active_cache_line(arch),
                                     machine_id,
                                     "ProxyState"
                                     ]
                                    )
        placement = arch.exclusive_placement() if hasattr(arch, "exclusive_placement") else None
        if placement is not None:
            fns = self._exclusive_fns(fns, arch, machine_id, placement)
        if parked:
            fns = self._parked_fns(fns, parked)
        if Util.partial_messages(arch.global_arch):
            fns += self.open_template("partial_data_functions.sm")
        const_str += fns
        return const_str + self.nl

    # Back-end option park_requests (Util.parked_ports). setState only notes the block: waking its
    # messages there would put them, older, in front of the message the in_port is handling, which
    # is popped afterwards.
    def _parked_fns(self, fns: str, parked: 'dict[str, list[str]]') -> str:
        nl = self.nl
        states = sorted({state for served in parked.values() for state in served})
        cond = (" ||" + nl + "    ").join(f"state == State:{state}" for state in states)
        decls = self.string_repl_keys(self.open_template("parked_functions.sm"), [", ".join(sorted(parked)), cond])
        set_state = "void setState(TBE tbe, Entry cache_entry, Addr LineAddress, State state) {" + nl
        set_state_begin = "  if (is_valid(tbe)) {" + nl + "    tbe.TBEState := state;" + nl
        assert fns.count(set_state) == 1 and fns.count(set_state_begin) == 1, "proxy template changed: setState"
        note = ("  if (state != getState(tbe, cache_entry, LineAddress) && servesParked(state)) {" + nl +
                "    // one block changes state per transition" + nl +
                "    assert(wakeUpPending == false || wakeUpAddr == LineAddress);" + nl +
                "    wakeUpPending := true;" + nl +
                "    wakeUpAddr := LineAddress;" + nl +
                "  }" + nl)
        return fns.replace(set_state, decls + set_state, 1).replace(set_state_begin, note + set_state_begin, 1)

    def _exclusive_fns(self, fns: str, arch: FlatArchitecture, machine_id: str, placement) -> str:
        tag_states, data_states, _ = placement
        fields = ["ProxyState"] + re.findall(r"^\s*\w+\s+(\w+)\s*[,;]", GenMachineStruct.gen_machine_struct_body_str(self, arch), re.M)
        nl, tab = self.nl, self.tab
        get_entry = ('  Entry getEntry(Addr LineAddress), return_by_pointer="yes" {' + nl +
                     '    return static_cast(Entry, "pointer", cache.lookup(LineAddress));' + nl + '  }')
        assert get_entry in fns, "proxy template changed: getEntry"
        decls = (f'structure(PerfectCacheMemory, external="yes") {{{nl}'
                 f'{tab}void allocate(Addr);{nl}{tab}void deallocate(Addr);{nl}'
                 f'{tab}Entry lookup(Addr);{nl}{tab}bool isTagPresent(Addr);{nl}}}{nl}{nl}'
                 f'PerfectCacheMemory tags, template="<{machine_id}_Entry>";{nl}{nl}')
        new_get_entry = (f'Entry getEntry(Addr LineAddress), return_by_pointer="yes" {{{nl}'
                         f'{tab}if (tags.isTagPresent(LineAddress)) {{{nl}'
                         f'{tab}{tab}return tags.lookup(LineAddress);{nl}{tab}}}{nl}'
                         f'{tab}return static_cast(Entry, "pointer", cache.lookup(LineAddress));{nl}}}{nl}{nl}')

        def membership(name, states):
            cond = " || ".join(f"state == State:{s}" for s in states) or "false"
            return f"bool {name}(State state) {{{nl}{tab}return {cond};{nl}}}{nl}{nl}"

        copy = "".join(f"{tab}to.{f} := from.{f};{nl}" for f in fields)
        moves = (f"void moveToTags(Addr LineAddress) {{{nl}"
                 f'{tab}Entry from := static_cast(Entry, "pointer", cache.lookup(LineAddress));{nl}'
                 f"{tab}tags.allocate(LineAddress);{nl}"
                 f"{tab}Entry to := tags.lookup(LineAddress);{nl}{copy}"
                 f"{tab}cache.deallocate(LineAddress);{nl}"
                 f'{tab}DPRINTF(RubySlicc, "tags <- cache (addr: %#x)\\n", LineAddress);{nl}}}{nl}{nl}'
                 f"void moveToCache(Addr LineAddress) {{{nl}"
                 f"{tab}Entry from := tags.lookup(LineAddress);{nl}"
                 f"{tab}cache.allocate(LineAddress, new Entry);{nl}"
                 f'{tab}Entry to := static_cast(Entry, "pointer", cache.lookup(LineAddress));{nl}{copy}'
                 f"{tab}tags.deallocate(LineAddress);{nl}"
                 f'{tab}DPRINTF(RubySlicc, "cache <- tags (addr: %#x)\\n", LineAddress);{nl}}}{nl}{nl}'
                 f"void placeEntry(Addr LineAddress, State state) {{{nl}"
                 f"{tab}if (tagState(state) && cache.isTagPresent(LineAddress)) {{{nl}"
                 f"{tab}{tab}moveToTags(LineAddress);{nl}"
                 f"{tab}}} else if (dataState(state) && tags.isTagPresent(LineAddress) && cache.cacheAvail(LineAddress)) {{{nl}"
                 f"{tab}{tab}moveToCache(LineAddress);{nl}{tab}}}{nl}}}{nl}{nl}")
        fns = fns.replace(get_entry, decls + new_get_entry + membership("tagState", tag_states)
                          + membership("dataState", data_states) + moves)
        set_state_end = "  if (is_valid(cache_entry)) {" + nl + "    cache_entry.ProxyState := state;" + nl + "  }" + nl + "}"
        assert set_state_end in fns, "proxy template changed: setState"
        fns = fns.replace(set_state_end, "  if (is_valid(cache_entry)) {" + nl + "    cache_entry.ProxyState := state;" + nl +
                          "    placeEntry(LineAddress, state);" + nl + "  }" + nl + "}", 1)
        return fns
