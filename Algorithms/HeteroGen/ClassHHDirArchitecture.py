#  Copyright (c) 2021.  Nicolai Oswald
#  Copyright (c) 2021.  University of Edinburgh
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

from typing import List, Tuple, Set
from networkx import MultiDiGraph
import itertools


from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassLevel import Level

from Algorithms.ControllerGeneration.ProxyDirController.GenProxyDirStateMachine import ProxyDirStateMachine


from DataObjects.States.ClassCompoundState import CompoundState
from DataObjects.FlowDataTypes.ClassMessage import BaseMessage
from DataObjects.Transitions.ClassTransitionv2 import Transition_v2

from Algorithms.ControllerGeneration.NetworkxGeneral.NestTreeNetworkx import NestTreeNetworkx

from Algorithms.HeteroGen.ArchTupleStateOrdering import ArchTupleStateOrdering




class HHDirArchitecture(ArchTupleStateOrdering, NestTreeNetworkx, FlatArchitecture, ProxyDirStateMachine):
    # Realize this as iterator
    ## The passed access needs to be performed in every remote proxy cache. Iterate over the remote proxy cache states
    #  passed as arguments and perform access, the requestor cluster wants to do.
    #  @param self access: Access, remote_proxy_dir_states: List[State_v2])
    ## Sorts the base state in the current compound state according to the architecture ordering
    #  @param self The object pointer.
    def det_sort_state_graph(self, new_graph: MultiDiGraph):
        graph_transitions = self.get_transitions_from_graph(new_graph)

        for graph_transition in graph_transitions:
            graph_transition.update_state(graph_transition.start_state,
                                          self.gen_new_sort_compound_state(graph_transition.start_state))
            if graph_transition.start_state != graph_transition.final_state:
                graph_transition.update_state(graph_transition.final_state,
                                              self.gen_new_sort_compound_state(
                                                  graph_transition.final_state))

        # Create new graph as this is more simple than updating all nodes
        return graph_transitions

    def gen_new_sort_compound_state(self, compound_state: CompoundState):
        sorted_state_tuple = self.sort_states_by_architecture(compound_state.base_states)
        state_id_tuple = (sorted_state_tuple, compound_state.prefix)
        if state_id_tuple not in self.graph_state_to_heterogen_state_map:
            self.graph_state_to_heterogen_state_map[state_id_tuple] = CompoundState(sorted_state_tuple,
                                                                                    compound_state.prefix)
        return self.graph_state_to_heterogen_state_map[state_id_tuple]

    def gen_initial_state(self, compound_archs: Tuple[FlatArchitecture]):
        return CompoundState(self.sort_states_by_architecture(list([arch.init_state for arch in compound_archs])))

    @staticmethod
    def gen_theoretical_state_space(compound_archs: Tuple[FlatArchitecture]):
        theoretical_state_space = list(itertools.product(*[arch.stable_states for arch in compound_archs]))
        return list([CompoundState(state_tuple) for state_tuple in theoretical_state_space])

    @staticmethod
    def get_valid_stable_states(stable_state_list: List[CompoundState],
                                transitions: List[Transition_v2]) -> Set[CompoundState]:
        valid_stable_states: List[CompoundState] = []
        for transition in transitions:
            if transition.start_state in stable_state_list:
                valid_stable_states.append(transition.start_state)
            if transition.final_state in stable_state_list:
                valid_stable_states.append(transition.final_state)
        return set(valid_stable_states)

    ####################################################################################################################
    ### Merge the system descriptors
    ####################################################################################################################
    def merge_base_architectures_and_machines(self) -> FlatArchitecture:
        # Select reference architecture
        ref_arch: FlatArchitecture = self.arch_tuple[0]
        # Copy all other architecture descriptions into new architecture
        for copy_arch in self.arch_tuple[1:]:
            ref_arch.global_arch.merge_base_architecture(copy_arch.global_arch)
            ref_arch.machine.merge_machine(copy_arch.machine)

        return ref_arch

    # Update all remote caches to be aware of the new and renamed directory
    def update_remote_archs(self, new_arch: FlatArchitecture, levels: List[Level]):
        self.update_machines_global_arch(new_arch, levels)

    @staticmethod
    def update_machines_global_arch(new_arch: FlatArchitecture, levels: List[Level]):
        for level in levels:
            for arch in level.get_architectures():
                arch.global_arch = new_arch.global_arch

    # The architecture is
    def get_arch_list(self):
        arch_list = []
        for compound_arch in self.arch_tuple:
            arch_list += compound_arch.get_arch_list()
        return [self] + arch_list

    def get_arch_from_message(self, msg: BaseMessage) -> FlatArchitecture:
        for arch in self.arch_tuple:
            if str(msg) in arch.global_arch.network.base_message_dict:
                return arch
