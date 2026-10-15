import re
from collections import OrderedDict

from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineActions import GenMachineActions
from Backend.SLICC.ModularSLICC.common.GenMachineStruct import GenMachineStruct
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassCluster import Cluster


class GenProxyActions(TemplateHandler):

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)
        self.generated_action_shorthands = set()

    def gen_proxy_actions_str(self, cluster: Cluster, arch: FlatArchitecture, in_ports: 'OrderedDict[str, str]', out_ports: 'OrderedDict[str, str]',
                              parked: 'dict[str, list[str]]' = None) -> str:

        #                                                 )
        #                           )

        port_actions = [
            # GenMachineActions.gen_pop_action(
            #     self, "mandatory_in", self._gen_queue_pop_action_shorthand("mandatory_in")),
            # GenMachineActions.gen_recycle_action(
            #     self, "mandatory_in", self._gen_recycle_action_shorthand("mandatory_in")),
        ]
        for port_name in sorted(in_ports.values()):
            port_actions.append(
                GenMachineActions.gen_pop_action(self, port_name, self._gen_queue_pop_action_shorthand(port_name)))
            if parked and port_name in parked:
                # option park_requests: the stalled messages of this port wait out of the queue
                port_actions.append(self.string_repl_keys(self.open_template("action_park_port.sm"),
                                                          [port_name, self._gen_recycle_action_shorthand(port_name)]))
                continue
            port_actions.append(
                GenMachineActions.gen_recycle_action(self, port_name, self._gen_recycle_action_shorthand(port_name)))
        if parked:
            port_actions.append(self.open_template("action_wake_parked.sm"))


        return "//" + __name__ + self.nl \
               + self.open_template("action_alloc_entry.sm") + self.nl \
               + self._gen_dealloc_entry_action(arch) + self.nl \
               + self.open_template("action_copy_entryTBE.sm") + self.nl \
               + self._gen_alloc_tbe_action(arch) + self.nl \
               + self.open_template("action_dealloc_tbe.sm") + self.nl \
               + (self.nl * 2).join(port_actions) + (self.nl * 2) \
               + GenMachineActions.gen_empty_action(self) + self.nl

    def _gen_dealloc_entry_action(self, arch: FlatArchitecture) -> str:
        action = self.open_template("action_dealloc_entry_proxy.sm")
        if hasattr(arch, "exclusive_placement") and arch.exclusive_placement() is not None:
            # exclusive policy: the entry may be in the tags (GenProxyStaticFns)
            anchor = "      unset_cache_entry();"
            assert anchor in action, "proxy template changed: deallocEntry"
            action = action.replace(anchor, "      if (tags.isTagPresent(address)) {\n"
                                            "              tags.deallocate(address);\n"
                                            "      }\n" + anchor, 1)
        return action

    def _gen_alloc_tbe_action(self, arch: FlatArchitecture) -> str:
        # Same fields as GenProxyTBE: every integer machine variable lives in the TBE. They are reset
        # explicitly so the ack counters of a new transaction never depend on the TBE defaults.
        inits = [f"check_allocate(TBEs){self.sem}", f"TBEs.allocate(address){self.sem}",
                 f"set_tbe(TBEs[address]){self.sem}", f"tbe.dirty := false{self.sem}"]
        for var_name, variable in arch.machine.variables.items():
            if variable.getText() == "INT_":
                res = GenMachineStruct._gen_int(variable, arch)
                field = re.match(r"\s*int\s+(\w+)", res).group(1)
                inits.append(f"tbe.{field} := 0{self.sem}")
        body = self.nl.join(self.tab + line for line in inits)
        return f'action(a_allocTBE, "aTBE", desc="Allocate TBE entry.") {{{self.nl}{body}{self.nl}}}'

    def _gen_operation_action_shorthand(self, start_state: str, end_state: str) -> str:
        action_shorthand = f'"{start_state[0]}{end_state[0]}0"'
        i = 0
        while action_shorthand in self.generated_action_shorthands:
            i += 1
            action_shorthand = action_shorthand[: -2] + str(i) + '"'
        self.generated_action_shorthands.add(action_shorthand)
        return action_shorthand

    def _gen_queue_pop_action_shorthand(self, port_name: str) -> str:
        action_shorthand = f'"p{port_name}0"'
        i = 0
        while action_shorthand in self.generated_action_shorthands:
            i += 1
            action_shorthand = action_shorthand[: -2] + str(i) + '"'
        self.generated_action_shorthands.add(action_shorthand)
        return action_shorthand

    def _gen_recycle_action_shorthand(self, port_name: str) -> str:
        action_shorthand = f'"r{port_name}0"'
        i = 0
        while action_shorthand in self.generated_action_shorthands:
            i += 1
            action_shorthand = action_shorthand[: -2] + str(i) + '"'
        self.generated_action_shorthands.add(action_shorthand)
        return action_shorthand
