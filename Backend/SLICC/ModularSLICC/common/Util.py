#  Copyright (c) 2022.  Nicolai Oswald
#  Copyright (c) 2022.  University of Edinburgh
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met: redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer;
#  redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution;
#  neither the name of the copyright holders nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#
#
#

from typing import Set, Dict, Tuple, List

from Algorithms.HeteroGen.ArchTupleStateOrdering import ArchTupleStateOrdering
from Algorithms.HeteroGen.ClassHHDirArchitecture import HHDirArchitecture
from Algorithms.HeteroGen.ClassHHDirArchitecture_L2private import HHDirArchitecture_L2private
from Backend.SLICC.ModularSLICC import SLICCTokens
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from DataObjects.Architecture.ArchitectureClassification import ArchitectureClassification
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.Architecture.ClassGlobalBaseArchitecture import GlobalBaseArchitecture
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassState import State
from DataObjects.FlowDataTypes.ClassBaseAccess import Access
from DataObjects.States.ClassCompoundState import CompoundState
from DataObjects.States.ClassStatev2 import State_v2
from DataObjects.Transitions.ClassTransitionv2 import Transition_v2
from Parser.DataTypes.ClassProtoMachine import ProtoMachine

def get_compound_perms(arch: FlatArchitecture, state: CompoundState, default: str | None = None) -> list[tuple[FlatArchitecture, set[str]]]:
    assert isinstance(arch, ArchTupleStateOrdering)
    accesses = []
    for sub_state in state.base_states:
        sub_arch = arch.get_arch_by_state(sub_state)
        accesses.append((sub_arch, get_arch_access_perms(sub_arch, sub_state, default)))
    return accesses

def get_arch_access_perms(arch: FlatArchitecture, state: State_v2, default: str | None = None) -> set[str]:
    if isinstance(state, CompoundState):
        return set.union(*[p for _, p in get_compound_perms(arch, state, default)])
    else:
        t = arch.stable_state_access_permission_map.get(state, {default} if default else {})
        return set(str(a) for a in t)

def get_invalid_states(arch: FlatArchitecture) -> Set[State_v2]:
    if isinstance(arch, HHDirArchitecture) or isinstance(arch, HHDirArchitecture_L2private):
        for i, c in enumerate(arch.arch_tuple):
            if c.machine.mach_type == ProtoMachine.k_cache:
                cs = get_invalid_states(c)
                r = set([state for state in arch.get_architecture_stable_states() if state.base_states[i] in cs])
                return r
        assert False, "HH Dirs should have a cache"
    stable_state_perms = [(state, get_arch_access_perms(arch, state))
                          for state in arch.get_architecture_stable_states()]
    invalid_states = {state
                      for state, perms in stable_state_perms
                      if "load" not in perms and "store" not in perms}
    return invalid_states


def get_evict_trans_states(arch: FlatArchitecture) -> Set[State_v2]:
    evict_states = set()
    for state in arch.get_architecture_states_verified():
        accesses = get_arch_access_perms(arch, state)
        if not state.stable and state.start_state_set:
            stable_state = state.start_state_set[0].stable_state
            accesses_stable_state = get_arch_access_perms(arch, stable_state)
            if len(accesses_stable_state) > 0 and state.end_state_set:
                if state.end_state_set[0].stable_state.state == "I":
                    evict_states.add(state)

    return evict_states

def get_states_following_invalid_states(arch: FlatArchitecture) -> Set[State_v2]:
    invalid_states = get_invalid_states(arch)
    next_states = set()
    for state in invalid_states:
        for trans in state.getaccess():
            next_state = trans.final_state
            next_states.add(next_state)
    return next_states


def _get_hit_events(arch: BaseArchitecture) -> Dict[str, List[Tuple[str, str]]]:
    res = {"load": [], "store": []}
    for state in arch.stable_states:
        for access in state.getaccesshit():
            assert access.final_state in arch.stable_states
            access_type = str(access.guard)
            if access_type in res:
                start_s = str(access.start_state)
                end_s = str(access.final_state)
                res[access_type].append((start_s, end_s))

    return res


def get_local_hit_events(arch: BaseArchitecture) -> Dict[Tuple[str, str], Tuple[str, str]]:
    def _gen_event_name(start_s: str, end_s: str, access_name: str) -> str:
        return f"{start_s}{access_name}{end_s}Event"

    res = {}
    for access, transitions in sorted(_get_hit_events(arch).items()):
        for start_state, end_state in transitions:
            res[(access, start_state)] = (end_state, _gen_event_name(start_state, end_state, access))

    return res


def get_remote_hit_events_port(arch: BaseArchitecture, in_port: str) -> Dict[Tuple[str, str], str]:
    def _gen_event_name(end_s: str, access_name: str, port_name: str) -> str:
        return f"external{access_name}{end_s}{port_name}"

    res = {}
    for access, transitions in sorted(_get_hit_events(arch).items()):
        for _, end_state in transitions:
            res[(access, end_state)] = _gen_event_name(end_state, access, in_port)
    return res


def get_active_cache_line(arch: BaseArchitecture) -> str:
    # TODO this is very hacky. Long story short ProtoGen in its DSL doesn't track which Data variable
    # it is you read from or write to when an access *hits*.
    # For now, we will get around this by assuming every cache has exactly 1 field of type Data,
    # and that it is always this field which is being read from or written to when you hit.
    active_line = None
    var_defs = arch.machine.variables.values()
    for var_def in var_defs:
        if var_def.getText() == SLICCTokens.t_DATA:
            assert active_line is None  # There must be a UNIQUE cache line for the line, see above comment
            active_line = var_def.getChildren()[-1].getText()
    assert active_line is not None
    return active_line


def get_message_data_var(cluster: Cluster) -> str:
    # Similar to get_active_cache_line, we sometimes also need to know precisely which data object
    # in a message is being read from or written to.
    # We therefore assume that the different message types COLLECTIVELY define a single, unique
    # cache line / data block.
    data_var = None

    msg_type_set = set()
    for global_arch in cluster.get_global_architectures():
        msg_type_set.update(global_arch.network.msg_types.values())

    for msg_type in msg_type_set:
        for var, var_type_tree in msg_type.msg_vars.items():
            if str(var_type_tree) == SLICCTokens.t_DATA:
                assert data_var is None or data_var == var, \
                    f"Messages define more than one data block; had {data_var}, found {var}."
                data_var = var

    assert data_var is not None, "Messages define no data block?"
    return data_var


def get_in_ports(arch: BaseArchitecture) -> 'OrderedDict[str, str]':
    def _gen_port_name(network_name: str) -> str:
        # Might want to consider something more sophisticated for this
        return network_name.lower() + "_in"

    in_ports = OrderedDict()
    if arch.machine.check_cache():
        direction = "From"
    else:
        assert arch.machine.check_dir()
        direction = "To"

    #net_node = arch.global_arch.network.network_node
    #definitions = net_node.getChildren()
    #for net in definitions:
    #    net_name = net.getChildren()[1].getText() + direction
    #    assert net_name not in in_ports
    #    in_ports[net_name] = _gen_port_name(net_name)

    for net in arch.global_arch.network.ordered_networks.keys():
        net_name = net + direction
        assert net_name not in in_ports
        in_ports[net_name] = _gen_port_name(net_name)

    for net in arch.global_arch.network.unordered_networks.keys():
        net_name = net + direction
        assert net_name not in in_ports
        in_ports[net_name] = _gen_port_name(net_name)

    return in_ports


def get_out_ports(arch: BaseArchitecture) -> 'OrderedDict[str, str]':
    def _gen_port_name(network_name: str) -> str:
        # Might want to consider something more sophisticated for this
        return network_name.lower() + "_out"

    out_ports = OrderedDict()
    if arch.machine.check_cache():
        direction = "To"
    else:
        assert arch.machine.check_dir()
        direction = "From"

    #net_node = arch.global_arch.network.network_node
    #definitions = net_node.getChildren()
    #for net in definitions:
    #    net_name = net.getChildren()[1].getText() + direction
    #    assert net_name not in out_ports
    #    out_ports[net_name] = _gen_port_name(net_name)

    for net in arch.global_arch.network.ordered_networks.keys():
        net_name = net + direction
        assert net_name not in out_ports
        out_ports[net_name] = _gen_port_name(net_name)

    for net in arch.global_arch.network.unordered_networks.keys():
        net_name = net + direction
        assert net_name not in out_ports
        out_ports[net_name] = _gen_port_name(net_name)

    return out_ports


def gen_stall_str(temp_h: TemplateHandler, arch: BaseArchitecture, port: str) -> str:
    if arch.machine.check_cache():
        return f"trigger(Event:Stall{port}, LineAddress, getEntry(LineAddress), tbe){temp_h.sem}"
    else:
        assert arch.machine.check_dir()
        return f"trigger(Event:Stall{port}, LineAddress, tbe){temp_h.sem}"

def gen_silent_evict(temp_h: TemplateHandler) -> str:
    return f"trigger(Event:deallocevict, LineAddress, getEntry(LineAddress), tbe){temp_h.sem}"


def gen_recycle_str(temp_h: TemplateHandler, cache: bool, port: str) -> str:
    return f'DPRINTF(RubySlicc, "recycling %s on {port} (addr: %#x)\\\\n", st, LineAddress);{temp_h.nl}' \
           f"{port}.recycle(clockEdge(), cyclesToTicks(recycleLatency));{temp_h.nl}" \
           f"{gen_progress_str(temp_h, cache)}"

def gen_progress_str(temp_h: TemplateHandler, arch: BaseArchitecture) -> str:
    if arch.machine.check_cache():
        return f"trigger(Event:Progress, LineAddress, getEntry(LineAddress), tbe){temp_h.sem}"
    else:
        assert arch.machine.check_dir()
        return f"trigger(Event:Progress, LineAddress, tbe){temp_h.sem}"


def gen_tbe_alloc_str(temp_h: TemplateHandler, arch: BaseArchitecture) -> str:
    if arch.machine.check_cache():
        return f"trigger(Event:allocTBE, LineAddress, getEntry(LineAddress), tbe){temp_h.sem}"
    else:
        assert arch.machine.check_dir()
        return f"trigger(Event:allocTBE, LineAddress, tbe){temp_h.sem}"


def gen_tbe_dealloc_str(temp_h: TemplateHandler, arch: BaseArchitecture) -> str:
    if arch.machine.check_cache():
        return f"trigger(Event:deallocTBE, LineAddress, getEntry(LineAddress), tbe){temp_h.sem}"
    else:
        assert arch.machine.check_dir()
        return f"trigger(Event:deallocTBE, LineAddress, tbe){temp_h.sem}"


def must_access_memory(arch: BaseArchitecture) -> bool:
    """
    Checks whether a given architecture must access main memory in order to read/write data.
    :param arch: The architecture to investigate.
    :param level: The level which the architecture lies in.
    :return: A boolean matching the truthfulness of the statement "this architecture must access main memory".
    """
    return arch.machine.check_dir()


def gen_trans_state_name(transition: Transition_v2) -> str:
    """
    Generates a transient state name based on a transition.
    :param transition: The Transition to derive the name from.
    :return: A string consisting of the name of the new state.
    """
    return ''.join(filter(lambda char: char.isalpha() or char == '_' or char == '-',
                          f"{str(transition)}_{str(hash(transition))}")
                   )


def reverse_direction(direction: str) -> str:
    return "From" if direction == "To" else "To"


def get_entry_variable(arch: BaseArchitecture, var_name: str, var_str: str) -> str:
    # Variable is stored in the cache entry if we are a dir or if it is the cache line.
    # Otherwise, it should be kept in the TBE/MSHR.
    if not cache or var_name == get_active_cache_line(arch) or isinstance(arch, HHDirArchitecture) or isinstance(arch, HHDirArchitecture_L2private):
        if arch.machine.mach_id == "cache":
            if var_str == "cl" :
                return f"getCacheBlock(tbe, getEntry(LineAddress), LineAddress)"
            elif var_str == "cl_in_msg" :
                # return f"getEntry(LineAddress).{var_str}"
                # return f"getCacheBlock(tbe, getEntry(LineAddress), LineAddress)"
                return f"setCacheBlock(tbe, getEntry(LineAddress), LineAddress, in_msg.cl);"
            else:
                return f"getCacheBlock(tbe, getEntry(LineAddress), LineAddress)"
        else:
            return f"getEntry(LineAddress).{var_str}"
    else:
        # accessing the tbe requires it to be valid, of course
        return f"tbe.{var_str}"


def check_tbe_valid(temp_h: TemplateHandler, arch: BaseArchitecture, port: str) -> str:
    return f"if (is_invalid(tbe)) {{{temp_h.nl}" \
           f"{temp_h.tab}if (TBEs.areNSlotsAvailable(1, clockEdge())) {{{temp_h.nl}" \
           f"{temp_h.tab * 2}{gen_tbe_alloc_str(temp_h, arch)}{temp_h.nl}" \
           f"{temp_h.tab}}} else {{{temp_h.nl}" \
           f"{temp_h.add_tabs(gen_recycle_str(temp_h, cache, port), 2)}{temp_h.nl}" \
           f"{temp_h.tab}}}{temp_h.nl}}}"



def check_cache_valid(temp_h: TemplateHandler) -> str:
    #return f"if (is_invalid(cache_entry)) {{{temp_h.nl}" \
    #       f"{temp_h.tab}if (cache.cacheAvail(in_msg.addr)) {{{temp_h.nl}" \
    #       f"{temp_h.tab * 2}{gen_tbe_alloc_str(temp_h, cache)}{temp_h.nl}" \
    #       f"{temp_h.tab}}} else {{{temp_h.nl}" \
    #       f"{temp_h.tab * 2}{gen_stall_str(temp_h, cache, port)}{temp_h.nl}" \
    #       f"{temp_h.tab}}}{temp_h.nl}}}"#
    return f"if (is_invalid(getEntry(LineAddress))) {{{temp_h.nl + temp_h.tab}trigger(Event:allocCacheEntry, LineAddress, getEntry(LineAddress), tbe);{temp_h.nl}}}"


def get_message_size(message_dict: Dict[str, str], cluster: Cluster) -> str:
    if get_message_data_var(cluster) in message_dict.keys():
        return "MessageSizeType:Data"
    else:
        return "MessageSizeType:Control"

def get_msg_port_mapping(cluster: Cluster) -> dict[str, set[str]]:
    msgs = {}
    for archss in cluster.get_machine_architectures():
        archs = archss.global_arch.get_dependent_architectures()
        for arch in archs:
            for transition in arch.get_architecture_transitions():
                operations = transition.operations
                for idx, op in enumerate(operations):
                    if str(op) == 'MCAST_' or str(op) == 'SEND_':
                        network = str(op.getChildren()[0])
                        msg_name = str(op.getChildren()[1])
                        msg_type = None
                        for op2 in reversed(operations[:idx]):
                            if str(op2) == 'ASSIGN_' and str(op2.getChildren()[0]) == msg_name:
                                msg_ctor = op2.getChildren()[2]
                                assert str(msg_ctor) == 'MSGCSTR_'
                                msg_type = str(msg_ctor.getChildren()[1])
                                break
                        assert msg_type is not None
                        msgs.setdefault(network, set()).add(msg_type)
    return msgs