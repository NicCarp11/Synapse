from collections import OrderedDict

from typing import List, Dict, Tuple

from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineEvents import GenMachineEvents
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyEvents(TemplateHandler):
    template_file = "event_enumeration.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_events_str(self, arch: FlatArchitecture, in_ports: 'OrderedDict[str, str]') -> str:

        const_str = "//" + __name__ + self.nl
        event_strs = []
        for port in sorted(in_ports.values()):
            # event_strs.extend(
            #     self.gen_remote_hit_events(port, Util.get_remote_hit_events_port(arch, port)))
            event_strs.append(f"dealloc{port}, desc=\"Event indicating the cache line + tbe should be deallocated "
                              f"following a message received on {port}.\"{self.sem}")
            event_strs.append(GenMachineEvents.gen_stall_event(self, port))

        event_strs.append(GenMachineEvents.gen_cache_alloc_event(self))
        event_strs.append(GenMachineEvents.gen_tbe_alloc_event(self))
        event_strs.append(GenMachineEvents.gen_tbe_dealloc_event(self))
        event_strs.append(GenMachineEvents.silent_evict_event(self))
        event_strs.append(GenMachineEvents.gen_progress_event(self))

        events_str = self.nl.join(event_strs)

        const_str += self.string_repl_keys(self.open_template(GenProxyEvents.template_file),
                                           ["Cache", self.add_tabs(events_str, 1)]
                                           )

        return const_str + self.nl

    def gen_local_hit_events(self, hit_map: Dict[Tuple[str, str], Tuple[str, str]]) -> List[str]:
        event_strs = []
        for (access, start_state), (end_state, event_name) in sorted(hit_map.items()):
            event_strs.append(
                f"{event_name}, desc=\"{start_state}->{end_state} upon local {access} hit.\"{self.sem}")

        return event_strs

    def gen_remote_hit_events(self, port: str, hit_map: Dict[Tuple[str, str], str]) -> List[str]:
        event_strs = []
        for (access, end_state), event_name in sorted(hit_map.items()):
            event_strs.append(
                f"{event_name}, desc=\"Remote {access} hit ending in state {end_state}. Should pop {port}.\"{self.sem}"
            )

        return event_strs
