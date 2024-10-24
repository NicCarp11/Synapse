from collections import OrderedDict

from typing import Dict

from Algorithms.ControllerGeneration.CompoundBaseController.CompoundDirArchitecture import CompoundDirArchitecture
from Algorithms.ControllerGeneration.CompoundBaseController.CompoundDirCacheArchitecture import \
    CompoundDirCacheArchitecture
from Algorithms.HeteroGen.ClassHHDirArchitecture import HHDirArchitecture
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.common.GenMachineInPorts import GenMachineInPorts
from Backend.SLICC.ModularSLICC.common.GenPCCToSLICC import GenPCCToSLICC
from Backend.SLICC.ModularSLICC.common.GenSLICCTree import GenSLICCTree
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassMultiDict import MultiDict
from DataObjects.States.ClassCompoundState import CompoundState
from Parser.DataTypes.ClassProtoMachine import ProtoMachine


class GenProxyInPorts(TemplateHandler):

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)
        self.all_message_names = set()

    def gen_proxy_in_ports_str(
            self,
            cluster: Cluster,
            arch: FlatArchitecture,
            in_ports: 'OrderedDict[str, str]',
            out_ports: 'OrderedDict[str, str]',
            machine_mappings: dict[str, str],
    ) -> str:
        assert isinstance(arch, HHDirArchitecture)
        alloc_states = self._find_alloc_msgs(arch)
        port_map = Util.get_msg_port_mapping(cluster)
        alloc_ports = dict()
        for port, msgs in port_map.items():
            guards = []
            for s, m in alloc_states:
                if m in msgs:
                    # alloc_ports.setdefault(port, set()).add((s, m))
                    guards.append(f"(st == State:{s} && in_msg.Type == CoherenceMessageType:{m})")
            if len(guards) > 0:
                alloc_ports[port] = self.add_tabs(self.string_repl_keys(self.open_template("proxy_evict_block.sm"),
                            [" || ".join(guards), self._gen_evict_in_port(cluster, arch, out_ports, machine_mappings, f"{port}from_in")
                                                                        .encode('unicode_escape')
                                                                        .decode("utf-8")]), 3)
        return "//" + __name__ + self.nl \
               + GenMachineInPorts.gen_machine_in_ports(
                    self, cluster, arch, True, "Cache", in_ports, out_ports, machine_mappings, evict_code=alloc_ports) \
               + self.nl

    def _find_alloc_msgs(self, arch: HHDirArchitecture) -> set[(str, str)]:
        msgs = set()
        for transition in arch.get_architecture_transitions():
            assert isinstance(transition.start_state, CompoundState)
            state_map = None
            invalid = False
            for cs in transition.start_state.base_states:
                ca = arch.get_arch_by_state(cs)
                if ca.machine.mach_type == ProtoMachine.k_dir:
                    assert isinstance(ca, CompoundDirCacheArchitecture)
                    state_map = ca.dir_state_req_base_message_access_map.get(cs, {})
                if ca.machine.mach_type == ProtoMachine.k_cache:
                    invalid = len(ca.stable_state_access_permission_map.get(cs, {None, None})) == 0
            assert state_map is not None
            if transition.guard in state_map:
                if invalid:
                    msgs.add((str(transition.start_state), str(transition.guard)))
        return msgs


    def _gen_evict_in_port(self, cluster: Cluster, arch: FlatArchitecture, out_ports: 'OrderedDict[str, str]', machine_mappings: dict[str, str], port_name: str) -> str:

        evicts = [s for s in arch.get_architecture_transitions() if str(s.guard) == "evict"]

        evicts_by_start = MultiDict()
        for e in evicts:
            evicts_by_start[str(e.start_state)] = e

        evict_handler = self._gen_access_str(cluster, arch, evicts_by_start, out_ports, machine_mappings, indent_level=2, port_name=port_name)

        return evict_handler

    def _gen_access_str(
            self,
            cluster: Cluster,
            arch: FlatArchitecture,
            transition_map: MultiDict,
            out_ports: 'OrderedDict[str, str]',
            machine_mappings: dict[str, str],
            indent_level: int,
            port_name: str
    ) -> str:

        transitions_strs = []

        for state_name, transitions in transition_map.items():

            slicc_tree_gen = GenSLICCTree(cluster, arch, True, port_name, out_ports,
                                          machine_mappings, allow_port_popping=True, set_final_state=True)

            op_str = ""

            op_str += slicc_tree_gen.gen_slicc_tree(transitions)

            # Also add a dummy event to make sure the simulation makes progress
            op_str += f"{self.nl}{Util.gen_progress_str(self, True)}"

            op_str = self.add_tabs(op_str, 1)

            transition_str = f"if (st == State:{state_name}) {{{self.nl}{op_str}{self.nl}}}"
            transitions_strs.append(transition_str)

        return self.add_tabs(" else ".join(transitions_strs)
                             + f" else {{{self.nl}{self.tab}"
                             + f"{Util.gen_recycle_str(self, True, port_name)}{self.nl}}}",
                             indent_level)