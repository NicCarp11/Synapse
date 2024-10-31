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

from typing import List, Dict, Tuple, Set, Union
from networkx import MultiDiGraph
import itertools


from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassLevel import Level

from Algorithms.ControllerGeneration.ProxyDirController.GenProxyDirStateMachine import ProxyDirStateMachine
from Algorithms.ControllerGeneration.CompoundBaseController.CompoundDirCacheArchitecture import CompoundDirCacheArchitecture

from DataObjects.FlowDataTypes.ClassBaseAccess import BaseAccess
from Parser.NetworkxParser.ClassProtoParserBase import ProtoParserBase

from DataObjects.States.ClassCompoundState import CompoundState
from DataObjects.States.ClassStatev2 import State_v2
from DataObjects.FlowDataTypes.ClassMessage import Message, BaseMessage
from DataObjects.States.ProxyDirState import ProxyDirState
from DataObjects.Transitions.ClassTransitionv2 import Transition_v2
from DataObjects.FlowDataTypes.ClassEvent import Event, EventAck

from Algorithms.ControllerGeneration.NetworkxGeneral.NestTreeNetworkx import NestTreeNetworkx
from Algorithms.ControllerGeneration.NetworkxGeneral.MergeGraphsNetworkx import MergeGraphsNetworkx
from Algorithms.ControllerGeneration.NetworkxGeneral.CompoundStateGenNetworkx import CompoundStateGenNetworkx
from Algorithms.ControllerGeneration.General.ChainTransitions import ChainTransitions

from Algorithms.HeteroGen.ArchTupleStateOrdering import ArchTupleStateOrdering
from Algorithms.ControllerGeneration.AccessMessageMap.GenAccessMessageMap import GenAccessMessageMap
from Algorithms.ControllerGeneration.ProxyDirController.ClassProxyDirArchitecture import ProxyDirArchitecture

from Algorithms.ProtoAlgoNetworkx.ProtoNetworkxBase import ProtoNetworkxBase

from Debug.Monitor.ClassDebug import Debug
from Debug.Monitor.ProtoCCTable import ProtoCCTablePrinter


class HHDirArchitecture(ArchTupleStateOrdering, NestTreeNetworkx, FlatArchitecture, ProxyDirStateMachine):
    def __init__(self, lower_level: Level, higher_level: Level, map_dict_list: List[Dict[str, List[str]]], gdbg: bool = False):
        self.gdbg = gdbg

        Debug.psection(f"Lower level directory controller {lower_level.parser.filename}")
        ProtoCCTablePrinter().ptransitiontable(list(lower_level.directory.get_architecture_transitions()))
        #Debug.psection(f"Lower level cache controller {lower_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(lower_level.cache.get_architecture_transitions()))

        # Determine Access Mappings
        #Debug.psection(f"GenAccessMessageMap for {lower_level.parser.filename}")
        #lower_level_msg_map = GenAccessMessageMap(lower_level)
        #Debug.psection(f"GenAccessMessageMap for {higher_level.parser.filename}")
        #higher_level_msg_map = GenAccessMessageMap(higher_level)

        #lower_level.directory.print_arch_sub_tree_graphs()
        # Generate Proxy Cache
        lower_level.directory = ProxyDirArchitecture(lower_level)

        #lower_level.directory.print_arch_sub_tree_graphs()

        #Debug.psection(f"Lower level ProxyDir controller {lower_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(lower_level.directory.get_architecture_transitions()))
        
        ProtoNetworkxBase(lower_level)

        #Debug.psection(f"Lower level cache controller for {lower_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(lower_level.cache.get_architecture_transitions()))

        # Update the request names as required by map dict list
        #CompoundDirCacheArchitecture(lower_level, map_dict_list)
        #CompoundDirCacheArchitecture(lower_level)

        #Debug.psection(f"Lower level dircache controller for {lower_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(lower_level.cache.get_architecture_transitions()))

        #Debug.psection(f"Lower level dircache controller for {lower_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(lower_level.directory.get_architecture_transitions()))

        #Debug.psection(f"Higher level initial directory controller {higher_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(higher_level.directory.get_architecture_transitions()))
        #Debug.psection(f"Higher level initial cache controller {higher_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(higher_level.cache.get_architecture_transitions()))

        # Run ProtoGen for the lower and the higher level
        ProtoNetworkxBase(higher_level)

        #Debug.psection(f"Higher level ProtoGen directory controller {higher_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(higher_level.directory.get_architecture_transitions()))
        #Debug.psection(f"Higher level ProtoGen cache controller {higher_level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(higher_level.cache.get_architecture_transitions()))

        # HeteroGen algorithm

        compound_archs: List[CompoundDirCacheArchitecture] = []
        self.arch_translation_table_dict = {}

        compound_archs.append(CompoundDirCacheArchitecture(lower_level))
        self.arch_translation_table_dict[compound_archs[0]] = map_dict_list[0]

        compound_archs.append(CompoundDirCacheArchitecture(higher_level))
        self.arch_translation_table_dict[compound_archs[1]] = map_dict_list[1]

        #Debug.psection(f"CompoundDirCacheArchitecture for {compound_archs[0].level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(compound_archs[0].get_architecture_transitions()))

        #Debug.psection(f"CompoundDirCacheArchitecture for {compound_archs[1].level.parser.filename}")
        #ProtoCCTablePrinter().ptransitiontable(list(compound_archs[1].get_architecture_transitions()))

        ArchTupleStateOrdering.__init__(self, tuple(compound_archs))

        NestTreeNetworkx.__init__(self, compound_archs[0], tuple(compound_archs))

        # Tracks the new states
        self.graph_state_to_heterogen_state_map: Dict[Tuple[Tuple[State_v2], str], CompoundState] = {}

        # Generate the product all states that can theoretically exist
        theoretical_state_space = self.gen_theoretical_state_space(tuple(compound_archs))

        fsm_transitions = self.gen_access_tree_transitions(theoretical_state_space)

        # Prune non-reachable states
        fsm_stable_states = self.get_valid_stable_states(theoretical_state_space, fsm_transitions)
        fsm_init_state = self.gen_initial_state(self.arch_tuple)

        FlatArchitecture.__init__(self, compound_archs[0], self.gdbg)
        self.update_base_fsm(fsm_init_state, fsm_stable_states, set(fsm_transitions))
        lower_level.directory = self
        #higher_level.cache = self

        heterogen_arch = self.merge_base_architectures_and_machines()
        self.update_remote_archs(heterogen_arch, [lower_level, higher_level])

        #allowed_states = set(fsm_stable_states) - set(mod_forbidden_state_list)
        #self.state_sub_tree_dict = self.prune_states_from_graph(self.state_sub_tree_dict,
        #                                                        allowed_states, mod_forbidden_state_list)

        Debug.psection(f"Hierarchical controller for {[proto.parser.filename for proto in [lower_level, higher_level]]}")
        ProtoCCTablePrinter().ptransitiontable(list(self.get_architecture_transitions()))

        Debug.psection(f"Higher level directory controller for {higher_level.parser.filename}")
        ProtoCCTablePrinter().ptransitiontable(list(higher_level.directory.get_architecture_transitions()))

        if self.gdbg:
            self.dbg_tree_graph(self.gen_graph(fsm_transitions))

    ## For every proxy directory state from the compound directory base states, determine which accesses can be served
    #  locally and which accesses involve remote components. There is a list of size N-1 architectures that are
    #  concurrently served to maximize concurrency for accessing remote clusters
    def gen_access_tree_transitions(self, compound_states: List[CompoundState]) -> List[Transition_v2]:
        hetero_transitions: List[Transition_v2] = []
        for compound_state in sorted(compound_states, key=lambda x: str(x)):
            for proxy_dir_state in compound_state.base_states:
                # Get a list of all requestor cluster directory trees and map them to the access types that the
                # remote proxies need to perform.
                remote_access_dir_graph_dict, local_request_dir_graph_set = self.get_request_dir_graphs(proxy_dir_state)
                # Get all remote proxy dir states of the remote architectures to which the access needs to be translated
                remote_proxy_dir_states = [state for state in compound_state.base_states if state != proxy_dir_state]

                # Check if a proxy processor is required, this is the case if the current compound state architecture
                # does not track that memory accesses complete in the order required by the memory consistency model
                remote_proxy_processor: bool = False

                # Generate remote access transitions -> Communication across architectures
                hetero_transitions += self.gen_remote_access_transitions(remote_access_dir_graph_dict,
                                                                         remote_proxy_dir_states,
                                                                         remote_proxy_processor)

                # Generate local access transitions -> No communication across architectures
                hetero_transitions += self.gen_local_access_transitions(local_request_dir_graph_set,
                                                                        remote_proxy_dir_states)

        fsm_graph = self.gen_graph(hetero_transitions)

        # Prune non reachable states
        self.prune_non_reachable_states_graph(fsm_graph)

        return self.get_transitions_from_graph(fsm_graph)

    # Realize this as iterator
    def get_request_dir_graphs(self, proxy_dir_state: State_v2):
        remote_access_dir_graph_dict: Dict[MultiDiGraph, BaseAccess.Access] = {}
        local_access_dir_graph_set: Set[MultiDiGraph] = set()
        proxy_dir_arch: CompoundDirCacheArchitecture = self.get_arch_by_state(proxy_dir_state)
        for request_tree in proxy_dir_arch.state_sub_tree_dict[proxy_dir_state]:
            tree_guard = self.get_transitions_by_start_state(request_tree, proxy_dir_state)[0].guard
            Debug.ptext(self.get_transitions_by_start_state(request_tree, proxy_dir_state)[0].print_in_out_msg())

            # Events are local accesses and do not communicate across hierarchies
            if isinstance(tree_guard, Event):
                local_access_dir_graph_set.add(request_tree)

            if not isinstance(tree_guard, (Message, BaseMessage, BaseAccess.Evict)):
                continue

            # Filter out Load/Store/Evict event if arch is lower-level dir.
            if isinstance(tree_guard, (BaseAccess.Evict, BaseAccess.Access)) and isinstance(proxy_dir_arch, ProxyDirArchitecture):
                continue

            if isinstance(tree_guard, Message):
                tree_guard = tree_guard.base_msg

            # TODO PutE/PutM -> should be remote_accesses as well
            #   _Ideally, L1 PutE/PutM would stage data in L2-CC; without triggering eviction from L2-CC
            #   _Only correct if L2-CC has its own eviction events
            #     -> Eviction from L2-CC means forcefully evicting in L1 before, by simulating store accesses to L1 dir
            #     -> If compound state denotes not-present in L1, L2-CC can evict immediately
            #         -> Still, simulate store to proxy-dir; would return immediately bc not-present in L1
            #     -> Overall, Mechanism should be identical to L2-CC receiving L2_Inv or L2_FwdGet{S,M}
            # TODO GetS->FwdGet_S is local, is that right?
            #     GetS with store access - could be because MSI has no hidden access for S, check this with MESIxMESI.
            #   GetS_load->Fwd_GetS/Fwd_GetM are remote, is that right? (depends on current dir_state - E)
            if proxy_dir_state in proxy_dir_arch.dir_state_req_base_message_access_map and \
                tree_guard in proxy_dir_arch.dir_state_req_base_message_access_map[proxy_dir_state]:
                remote_access_dir_graph_dict[request_tree] = \
                    proxy_dir_arch.dir_state_req_base_message_access_map[proxy_dir_state][tree_guard]
            else:
                local_access_dir_graph_set.add(request_tree)

        return remote_access_dir_graph_dict, local_access_dir_graph_set

    def gen_remote_access_transitions(self,
                                      remote_access_dir_graph_dict: Dict[MultiDiGraph, BaseAccess.Access],
                                      remote_proxy_dir_states: List[ProxyDirState],
                                      remote_proxy_processor: bool) -> List[Transition_v2]:
        hetero_transitions = []
        for remote_proxy_access_tree in remote_access_dir_graph_dict:
            # There must exist one or multiple (N-1 archs) remote proxy access tree, that need to be served, before
            # the directory can respond to its local requestor.
            remote_proxy_graph = self.get_access_proxy_dir_graph(remote_access_dir_graph_dict[remote_proxy_access_tree],
                                                             remote_proxy_dir_states)

            if len(self.get_terminal_nodes_by_attribute(remote_proxy_graph))>1:
                terminal_nodes: [State_v2] = []
                #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(remote_proxy_graph)))
                for terminal_node in self.get_terminal_nodes_by_attribute(remote_proxy_graph):
                    if not terminal_node.stable:

                        stable_start = terminal_node.start_state_set[0].stable_state

                        outself = self.get_access_proxy_dir_graph(remote_access_dir_graph_dict[remote_proxy_access_tree], [stable_start])
                        outself = self.copy_graph(outself)
                        # Only keep path from transient terminal node to actual terminal node
                        #traces = self.get_trans_traces(outself, terminal_node, self.get_terminal_nodes_by_attribute(remote_proxy_graph))
                        #for trace in traces:
                        #    self.add_transition_to_graph(remote_proxy_graph, trace)
                        #MergeGraphsNetworkx().merge_identical_start_state_graphs(traces)
                        outself.remove_edge(stable_start, terminal_node)
                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(outself)))
                        # Merge the extra transitions into original remote access graph
                        for transition in self.get_transitions_from_graph(outself):
                            self.add_transition_to_graph(remote_proxy_graph, transition)

                    else:
                        terminal_nodes.append(terminal_node)

                self.clear_terminal_nodes_attribute(remote_proxy_graph)
                self.set_terminal_nodes_attribute(remote_proxy_graph, terminal_nodes)
                #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(remote_proxy_graph)))
                #print("toto")

            ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(remote_proxy_graph)))
            nest_graph = self.nest_graphs(remote_proxy_graph, remote_proxy_access_tree)

            sub_nesting: Dict = {}
            for remote_proxy_dir_state in remote_proxy_dir_states:
                transition_list: List[Transition_v2] = self.get_transitions_from_graph(remote_proxy_graph)
                for transition in transition_list:
                    remote_proxy_dir_arch: CompoundDirCacheArchitecture = self.get_arch_by_state(remote_proxy_dir_state)
                    transition_guard = transition.guard
                    if (remote_proxy_dir_state in remote_proxy_dir_arch.cache_state_fwd_message_access_map
                            and transition_guard in remote_proxy_dir_arch.dir_state_req_base_message_access_map[remote_proxy_dir_state]):
                        start_state = self.get_transitions_from_graph(remote_proxy_access_tree)[0].start_state
                        store_access_tree = self.get_access_proxy_dir_graph(remote_proxy_dir_arch.dir_state_req_base_message_access_map[remote_proxy_dir_state][transition_guard], [start_state])

                        #print("toto")
                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(store_access_tree)))
                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(remote_proxy_access_tree)))
                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(remote_proxy_graph)))
                        #for terminal_node in self.get_terminal_nodes_by_attribute(remote_proxy_graph):
                        #    print(terminal_node)

                        sub_graph = MultiDiGraph()
                        #sub_graph.add_edge(transition_list[0].start_state, transition_list[0].final_state, transition=transition_list[0])
                        sub_graph.add_edge(transition.start_state, transition.final_state, transition=transition)
                        self.clear_root_node_attribute(sub_graph)
                        self.clear_terminal_nodes_attribute(sub_graph)
                        #self.set_root_node_attribute(sub_graph, transition_list[0].start_state)
                        self.set_root_node_attribute(sub_graph, transition.start_state)
                        self.set_terminal_nodes_attribute(sub_graph, transition.final_state)

                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(sub_graph)))

                        # Can't merge with multiple start guard
                        #sub_graph2 = self.copy_graph(remote_proxy_access_tree)
                        #sub_graph3 = MergeGraphsNetworkx().merge_identical_start_state_graphs([store_access_tree, remote_proxy_access_tree])
                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(sub_graph3)))

                        sub_nesting[transition_guard] = self.nest_graphs(store_access_tree, sub_graph)

                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(nest_graph)))
                        #for terminal_node in self.get_terminal_nodes_by_attribute(nest_graph):
                        #    print(terminal_node)
                        #print("toto")



            for guard in sub_nesting.keys():
                graph: MultiDiGraph = sub_nesting[guard]
                ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(nest_graph)))
                for transition in self.get_transitions_from_graph(nest_graph):
                    if transition.guard == guard:
                        start_state = transition.start_state
                        final_state = transition.final_state

                        trans = self.get_transitions_from_graph(graph)
                        #ProtoCCTablePrinter().ptransitiontable(trans)
                        terminal_nodes: List[CompoundState] = self.get_terminal_nodes_by_attribute(graph)
                        root_node = self.get_root_node_by_attribute(graph)
                        for trans2 in trans:
                            if trans2.start_state == root_node:
                                trans2.start_state = start_state
                            if trans2.final_state in terminal_nodes:
                                trans2.final_state = final_state
                        #ProtoCCTablePrinter().ptransitiontable(trans)

                        nest_graph.remove_edge(start_state, final_state)
                        self.add_transition_to_graph(nest_graph, trans)
                        #self.clear_root_node_attribute(graph)
                        #self.clear_terminal_nodes_attribute(graph)
                        #self.set_root_node_attribute(graph, start_state)
                        #self.set_terminal_nodes_attribute(graph, final_state)
                        #ProtoCCTablePrinter().ptransitiontable(list(self.get_transitions_from_graph(nest_graph)))
                        #print("toto")





            # Nest the remote operation tree in
            #nest_graph = self.nest_graphs(remote_proxy_graph, remote_proxy_access_tree)

            # Remove the proxy processor component that is naturally included in certain protocols if not required
            # for correctness, this is when the issuing cluster cache has a proxy processor that monitors that the
            # memory accesses complete in the order required by the memory consistency model. If no remote proxy
            # processor is required, then prune all event handling to maximize concurrency among remote accesses to
            # different addresses
            if not remote_proxy_processor:
                nest_graph = self.prune_event_execution(nest_graph)

            self.prune_evict_proxy_msg_assign(nest_graph)

            # Update the transition states by new compound states whose base states are sorted according to the
            # architecture tuple
            hetero_transitions += self.det_sort_state_graph(nest_graph)

        return hetero_transitions

    ## The passed access needs to be performed in every remote proxy cache. Iterate over the remote proxy cache states
    #  passed as arguments and perform access, the requestor cluster wants to do.
    #  @param self access: Access, remote_proxy_dir_states: List[State_v2])
    def get_access_proxy_dir_graph(self, access: BaseAccess.Access,
                                   remote_proxy_dir_states: List[State_v2]) -> MultiDiGraph:

        remote_tree_dict: Dict[CompoundDirCacheArchitecture, MultiDiGraph] = {}
        # For every state and architecture find the remote proxy access trees that correspond with the access that needs
        # to be performed
        for remote_proxy_dir_state in remote_proxy_dir_states:
            remote_proxy_dir_arch: CompoundDirCacheArchitecture = self.get_arch_by_state(remote_proxy_dir_state)

            # Extract the translation dict from the architecture translation, this is currently only designed for two
            # architectures being merged, but can easily be extended
            translation_table_dict = self.arch_translation_table_dict[remote_proxy_dir_arch]

            for required_access in translation_table_dict[str(access)]:
                access_trees: List[MultiDiGraph] = []
                for msg_tree in remote_proxy_dir_arch.state_sub_tree_dict[remote_proxy_dir_state]:
                    tree_guard = self.get_transitions_by_start_state(msg_tree, remote_proxy_dir_state)[0].guard

                    if not isinstance(tree_guard, BaseAccess.Access):
                        continue

                    if str(tree_guard) == required_access:
                        access_trees.append(msg_tree)

                if not len(access_trees):
                    return

                #Debug.perror("No matching access guard tree found in remote architecture. Check translation table",
                #             len(access_trees) > 0)

                if len(access_trees) > 1:
                    remote_tree_dict[remote_proxy_dir_arch] = \
                        MergeGraphsNetworkx().merge_identical_start_state_graphs(access_trees)
                else:
                    remote_tree_dict[remote_proxy_dir_arch] = access_trees[0]

        # Merge remote trees
        remote_tree = None
        if len(remote_tree_dict) > 1:
            # Generate a cartesian product of all remote trees.
            Debug.perror("Merge remote trees. Either chain them up, or better execute them concurrently!!!")
        else:
            remote_tree = remote_tree_dict[list(remote_tree_dict.keys())[0]]

        return remote_tree

    def gen_local_access_transitions(self, local_access_dir_graph_set: Set[MultiDiGraph],
                                     remote_proxy_dir_states: List[ProxyDirState]) -> List[Transition_v2]:
        hetero_transitions = []
        for request_tree in local_access_dir_graph_set:
            updated_tree = CompoundStateGenNetworkx().gen_compound_states_graph(request_tree, remote_proxy_dir_states)
            hetero_transitions += self.det_sort_state_graph(updated_tree)

        return hetero_transitions

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

    def prune_evict_proxy_msg_assign(self, remote_proxy_graph: MultiDiGraph):
        for transition in self.get_transitions_from_graph(remote_proxy_graph):
            for operation in transition.operations:
                if str(operation) in ProtoParserBase.k_assign:
                    tokens = operation.getChildren()
                    if len(tokens) == 3 and [str(token) for token in tokens] == ["proxy_msg","=","evict"]:
                        transition.operations.remove(operation)

    def prune_event_execution(self, remote_proxy_graph: MultiDiGraph):
        root_node = self.get_root_node_by_attribute(remote_proxy_graph)
        terminal_nodes = self.get_terminal_nodes_by_attribute(remote_proxy_graph)
        traces: List[List[Transition_v2]] = self.get_trans_traces(remote_proxy_graph, root_node, terminal_nodes)

        remote_proxy_transitions: List[Transition_v2] = []
        for trace in traces:
            for trans_ind in range(0, len(trace)):
                self.remove_event_operation(trace[trans_ind])
                if trans_ind > 0:
                    chain_trans = self.chain_event_transitions(trace[trans_ind-1], trace[trans_ind])
                    if chain_trans:
                        # Remove preceding transition and replace it with new chained one
                        del remote_proxy_transitions[-1]
                        remote_proxy_transitions.append(chain_trans)
                        continue
                remote_proxy_transitions.append(trace[trans_ind])

        # Filter the transitions
        remote_proxy_transitions: Set[Transition_v2] = set(remote_proxy_transitions)

        # Generate new tree from filtered transitions
        new_graph = self.gen_graph(remote_proxy_transitions)
        self.set_root_node_attribute(new_graph, root_node)
        self.set_terminal_nodes_attribute(new_graph, terminal_nodes)

        return new_graph

    @staticmethod
    def remove_event_operation(transition: Transition_v2):
        remove_op = [operation for operation in transition.operations
                     if str(operation) in (ProtoParserBase.k_event, ProtoParserBase.k_event_ack)]

        transition.operations = [operation for operation in transition.operations
                                 if str(operation) not in (ProtoParserBase.k_event, ProtoParserBase.k_event_ack)]
        transition.out_event = None

    @staticmethod
    def chain_event_transitions(first_trans: Transition_v2, second_trans: Transition_v2) -> Union[Transition_v2, None]:
        if isinstance(second_trans.guard, Event) or isinstance(second_trans.guard, EventAck):
            return ChainTransitions.chain_transitions(first_trans, second_trans)
        return None

    def gen_initial_state(self, compound_archs: Tuple[CompoundDirCacheArchitecture]):
        return CompoundState(self.sort_states_by_architecture(list([arch.init_state for arch in compound_archs])))

    @staticmethod
    def gen_theoretical_state_space(compound_archs: Tuple[CompoundDirCacheArchitecture]):
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
    def merge_base_architectures_and_machines(self) -> CompoundDirCacheArchitecture:
        # Select reference architecture
        ref_arch: CompoundDirCacheArchitecture = self.arch_tuple[0]
        # Copy all other architecture descriptions into new architecture
        for copy_arch in self.arch_tuple[1:]:
            ref_arch.global_arch.merge_base_architecture(copy_arch.global_arch)
            ref_arch.machine.merge_machine(copy_arch.machine)

        return ref_arch

    # Update all remote caches to be aware of the new and renamed directory
    def update_remote_archs(self, new_arch: CompoundDirCacheArchitecture, levels: List[Level]):
        # self.update_directory_names(new_arch, levels)
        self.update_machines_global_arch(new_arch, levels)

    @staticmethod
    def update_directory_names(new_arch: CompoundDirCacheArchitecture, levels: List[Level]):
        for level in levels:
            # TODO should ensure that L2-cache still sends L2 msg to L2-dir, not L1-dir (bridge)
            # Get the current level directory id
            level_dir_id = str(level.directory)
            # TODO should we let bridge be L1-dir or L2-cache?
            # TODO fixthis: introduce duplicate transitions in L2-dir when bridge is L2-cache
            #level_dir_id = str(level.cache)
            for arch in level.get_architectures():
                # Update the directory name in all architectures
                arch.replace_transitions_objects(level_dir_id, str(new_arch))

    @staticmethod
    def update_machines_global_arch(new_arch: CompoundDirCacheArchitecture, levels: List[Level]):
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