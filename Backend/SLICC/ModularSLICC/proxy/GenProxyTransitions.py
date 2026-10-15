import re
from collections import OrderedDict

from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.common.GenMachineActions import GenMachineActions
from Backend.SLICC.ModularSLICC.common.GenMachineTransitions import GenMachineTransitions
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyTransitions(TemplateHandler):

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_transitions_str(self, arch: FlatArchitecture, in_ports: 'OrderedDict[str, str]',
                                  parked: 'dict[str, list[str]]' = None) -> str:

        invalid_states = sorted({str(state) for state in Util.get_invalid_states(arch)})
        invalid_states_str = f"{{{', '.join(invalid_states)}}}"
        all_states = sorted({str(state) for state in arch.get_architecture_states_verified()})
        all_states_str = f"{{{', '.join(all_states)}}}"

        dealloc_trans_strs = []
        stall_strs = []
        for port_name in sorted(in_ports.values()):
            dealloc_trans_strs.append(self.string_repl_keys(self.open_template("transition_dealloc_entry.sm"),
                                                            [invalid_states_str,
                                                             port_name,
                                                             GenMachineActions.get_queue_pop_action_name(port_name)
                                                             ]
                                                            )
                                      )
            stall_strs.append(GenMachineTransitions.gen_stall_transition(self, all_states, port_name))

        dealloc_trans_str = (self.nl * 2).join(dealloc_trans_strs)
        stall_str = (self.nl * 2).join(stall_strs)

        # alloc_trans_strs = []
        # next_states = sorted({str(state) for state in Util.get_states_following_invalid_states(arch)})
        #for next_state in next_states:
        #    for state in invalid_states:
        #        alloc_trans_strs.append(self.string_repl_keys(self.open_template("transition_alloc_entry.sm"),
        #                                                      [state,
        #                                                       next_state,
        #                                                       GenMachineActions.get_operation_action_name(state,
        #                                                                                                 next_state
        #                                                                                                 ),
        #                                                       ]
        #                                                      )
        #                                )
        # alloc_trans_str = (self.nl * 2).join(alloc_trans_strs)


        evict_states = sorted(Util.proxy_evict_states(arch))
        evict_trans_str = ""
        if evict_states:
            evict_trans_str = self.string_repl_keys(self.open_template("transition_silent_evict.sm"),
                                                    [f"{{{', '.join(evict_states)}}}"]) + (self.nl * 2)

        before_stalls = dealloc_trans_str + (self.nl * 2) \
               + evict_trans_str
        after_stalls = self.string_repl_keys(self.open_template("transition_alloc_cache_entry.sm"), [all_states_str]) \
               + (self.nl * 2) \
               + self.string_repl_keys(self.open_template("transition_alloc_tbe.sm"), [all_states_str]) \
               + (self.nl * 2) \
               + self.string_repl_keys(self.open_template("transition_dealloc_tbe.sm"), [all_states_str]) \
               + (self.nl * 2)  \
               + GenMachineTransitions.gen_progress_transition(
                    self, map(str, arch.get_architecture_states_verified())) + self.nl
        if parked:
            # option park_requests: every transition but the stalls ends by waking the messages
            # parked for the block whose state the in_port has just changed (setState)
            before_stalls, after_stalls = (self._wake_parked(trans) for trans in (before_stalls, after_stalls))
        return "//" + __name__ + self.nl \
               + before_stalls \
               + stall_str + (self.nl * 2) \
               + after_stalls

    @staticmethod
    def _wake_parked(transitions: str) -> str:
        woken = re.sub(r"^(\s*)(\S[^\n]*;)\n\}", r"\1\2\n\1wakeUpParked;\n}", transitions, flags=re.M)
        assert woken.count("wakeUpParked;") == woken.count("transition("), "proxy transition templates changed"
        return woken
