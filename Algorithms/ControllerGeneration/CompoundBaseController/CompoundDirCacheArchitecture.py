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

from typing import List, Dict, Tuple

from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassLevel import Level

from DataObjects.Transitions.ClassTransitionv2 import Transition_v2
from Algorithms.ControllerGeneration.AccessMessageMap.GenAccessMessageMap import GenAccessMessageMap
from DataObjects.FlowDataTypes.ClassMessage import Message, BaseMessage
from DataObjects.ClassMultiDict import MultiDict
from Debug.Monitor.ClassDebug import Debug
from DataObjects.FlowDataTypes.ClassBaseAccess import BaseAccess
from DataObjects.States.ProxyDirState import ProxyDirState

from Algorithms.ControllerGeneration.ProxyDirController.ClassProxyDirArchitecture import ProxyDirArchitecture
from Algorithms.ControllerGeneration.NetworkxGeneral.TreeBaseNetworkx import TreeBaseNetworkx

class CompoundDirCacheArchitecture(FlatArchitecture, GenAccessMessageMap):

    # NOSWALD Transition trees can be debugged using the TreeBaseNetworkx.print_tree_graph(transition_tree) function

    def __init__(self, arch_level: Level, gdbg: bool = False):
        self.cache = arch_level.cache
        self.directory = arch_level.directory
        self.level = arch_level

        # Determine message mappings
        GenAccessMessageMap.__init__(self, arch_level)

        # Generate Proxy Cache

        # Generate Concurrent Cache

        # Determine accesses that must be renamed

        # Update the cache transitions to convey access types
        self.update_cache_req_transitions()
        self.update_cache_fwd_transitions()

        new_transitions = []
        if isinstance(arch_level.directory, ProxyDirArchitecture):
            new_transitions = self.gen_new_directory_req_transitions()
        else:
            new_transitions = self.gen_new_directory_req_transitions()
            # Cheap trick, but works
            self.dir_state_req_base_message_access_map = self.cache_state_fwd_message_access_map
            # TODO: FIX THIS: dirty manual logic because write detection from protocol tuples is broken with `CXL.pcc`
            store_access: BaseAccess = self.level.cache.global_arch.base_access.access_map[self.level.cache.global_arch.base_access.k_store]
            for state in self.dir_state_req_base_message_access_map:
                to_remove = []
                for msg in self.dir_state_req_base_message_access_map[state]:
                    # With `MESI.pcc` in L1, Cmp* message are mis-detected as forwarded requests.
                    if isinstance(msg, BaseMessage) and msg.id.startswith("Cmp"):
                        to_remove.append(msg)
                    # Fix all forwarded requests that are improperly mapped to load access
                    if isinstance(msg, BaseMessage) and msg.id != "BISnpDataL2":
                        self.dir_state_req_base_message_access_map[state][msg] = store_access
                for msg in to_remove:
                    self.dir_state_req_base_message_access_map[state].pop(msg)
            # Union gives same result
            #self.dir_state_req_base_message_access_map.update(self.cache_state_fwd_message_access_map)
            # TODO ChangeThis: cleaner solution is to keep all mappings for dir/cache req to access
            #   Would work similarly for both lower & higher level

        #new_dif = FlatArchitecture(arch_level.directory, gdbg)
        #new_dif.copy_flat_architecture(self.directory)
        #if new_transitions:
        #    new_dif.update_base_fsm(self.directory.init_state, self.directory.stable_states, list(new_transitions))

        if isinstance(arch_level.directory, ProxyDirArchitecture):
            FlatArchitecture.__init__(self, self.directory, gdbg)
            FlatArchitecture.copy_flat_architecture(self, self.directory)
            if new_transitions:
                self.update_base_fsm(self.directory.init_state, self.directory.stable_states, list(new_transitions))
        else:
            FlatArchitecture.__init__(self, self.cache, gdbg)
            FlatArchitecture.copy_flat_architecture(self, self.cache)
        #    TODO This nuked the state_sub_tree_dict of the cache, do we need it?
        #      It seems cache transitions are already well-formed, so perhaps not
        #      Is it useful to update directory fsm with renamed transitions in the higher-level? Check this.
        #    if new_transitions:
        #        self.update_base_fsm(self.cache.init_state, self.cache.stable_states, list(new_transitions))

        # LL CompoundDirCacheArch is a Dir, HL CompoundDirCacheArch is a Cache
        if isinstance(arch_level.directory, ProxyDirArchitecture):
            arch_level.directory = self
        else:
            arch_level.cache = self

    def __str__(self):
        return str(self.arch_name)

    ####################################################################################################################
    # Update cache transitions
    ####################################################################################################################
    # In cache transitions the base messages can be simply replaced and the operation strings updated. This is possible,
    # as the number of transitions stays the same and only the type of access is encoded in the message
    # HeteroGen
    def update_cache_req_transitions(self):
        for state, new_to_orig_map in self.cache_state_to_new_req_base_message_map.items():
            for new_base_message, old_base_message in new_to_orig_map.items():
                # Messages that are not renamed do not need to be updated
                if new_base_message == old_base_message:
                    continue

                access = self.cache_state_new_req_to_access_map[state][new_base_message]

                for transition_tree in self.cache.state_sub_tree_dict[state]:
                    base_transition = self.get_transitions_by_start_state(transition_tree, state)[0]

                    # Only accesses related to the special operations are renamed
                    if isinstance(base_transition.guard, BaseAccess.Access) and base_transition.guard != access:
                        continue

                    for transition in self.get_transitions_from_graph(transition_tree):
                        new_trans, mutation = self.update_transition_base_messages(transition, old_base_message, new_base_message)
                        if mutation:
                            self.cache.add_transition_to_graph(transition_tree, new_trans)

    # HieraGen
    def update_cache_fwd_transitions(self):
        for state, new_to_orig_map in self.remote_cache_state_new_fwd_map.items():
            for new_base_message, old_base_message in new_to_orig_map.items():

                if new_base_message == old_base_message:
                    continue

                for transition_tree in self.cache.state_sub_tree_dict[state]:
                    for transition in self.get_transitions_from_graph(transition_tree):
                        new_trans, mutation = self.update_transition_base_messages(transition, old_base_message, new_base_message)
                        if mutation:
                            self.cache.add_transition_to_graph(transition_tree, new_trans)

    ####################################################################################################################
    # Update and copy directory transitions
    ####################################################################################################################
    # In case of the directory, it is not enough to simply update the transitions, as the number of different messages
    # has changed on the cache side. While messages like ABC_load and ABC_store still have the same the same
    # functionality coherence wise, they convey another access that is performed by the cache to the directory, which
    # can forward the access now to another controller to build Hierachies or HeteroGenous architectures
    def gen_new_directory_req_transitions(self):
        new_transitions: List[Transition_v2] = []
        cache_start_state = self.cache.init_state
        for dir_state in self.dir_state_req_to_new_req_msg_map:

                for transition_tree in self.directory.state_sub_tree_dict[dir_state]:
                    for transition in self.get_transitions_from_graph(transition_tree):

                        req_mutation = False
                        fwd_mutation = False
                        init_req = None
                        mod_trans = transition

                        # Convert proxy cache access into equivalent 
                        if isinstance(transition.final_state, ProxyDirState) and isinstance(transition.guard, BaseAccess.Access):
                            if dir_state in self.dir_state_req_base_message_access_map:
                                for req_msg, access in self.dir_state_req_base_message_access_map[dir_state].items():
                                    if access == transition.guard:
                                        init_req = req_msg
                                        TreeBaseNetworkx.print_tree_graph(transition_tree)   
                                        break
                        else:
                            for new_req, old_req in self.dir_state_req_to_new_req_msg_map[dir_state].items():
                                if self.check_update_guard(transition.guard, old_req):
                                    init_req = new_req
                                    mod_trans, req_mutation = self.update_transition_base_messages(transition, old_req, init_req)
                                    break
      
                        # Determine if forwarded message must be labeled with the specific access (HieraGen)
                        # How a forwarded request must be replabeled is dependent on the 
                        if dir_state in self.dir_state_req_to_new_fwd_msg_map and init_req in self.dir_state_req_to_new_fwd_msg_map[dir_state]:
                            new_fwd = self.dir_state_req_to_new_fwd_msg_map[dir_state][init_req]
                            old_fwd = self.dir_state_fwd_to_new_fwd_msg_map[dir_state][new_fwd]
                            if new_fwd != old_fwd:
                                mod_trans, fwd_mutation = self.update_transition_base_messages(mod_trans, old_fwd, new_fwd)

                        if req_mutation or fwd_mutation:
                            self.directory.add_transition_to_graph(transition_tree, mod_trans)
                            # TODO: Why was this disabled?
                            #   Looks like updated transitions are already merged above
                            #   Do we still need this to be updated,
                            #     for the function to return all transitions, including the new ones?
                            #   Check This: important bc the return value here is used later
                            #     by outer context to generate the updated dir fsm
                            new_transitions.append(mod_trans)

                    TreeBaseNetworkx.print_tree_graph(transition_tree)                

        return self.directory.get_architecture_transitions().union(set(new_transitions))              

    def gen_old_to_new_base_message_multidict(self):
        old_to_new_base_message_list = MultiDict()
        for new_base_message in self.new_req_to_original_base_message_map:
            old_to_new_base_message_list[self.new_req_to_original_base_message_map[new_base_message]] = new_base_message
        return old_to_new_base_message_list

    def update_transition_base_messages(self, transition: Transition_v2,
                                        old_base_message: BaseMessage, new_base_message: BaseMessage, force_mutatation: bool = False) -> Tuple[Transition_v2, bool]:
        mutation = self.check_update_guard(transition.guard, old_base_message) or force_mutatation
        if mutation:
            transition = transition.deepcopy_trans()

        transition.guard = self.update_message(transition.guard, old_base_message, new_base_message)

        out_msgs = []
        for out_msg in list(transition.out_msg):
            out_msgs.append(self.update_message(out_msg, old_base_message, new_base_message))
        transition.out_msg = out_msgs
        
        return transition, mutation

    def check_update_guard(self, guard, old_base_message: BaseMessage) -> bool:
        if isinstance(guard, Message) and guard.base_msg == old_base_message:
            return True
        elif isinstance(guard, BaseMessage) and guard == old_base_message:
            return True
        else:
            return False

    def update_message(self, guard, old_base_message: BaseMessage, new_base_message: BaseMessage):
        if isinstance(guard, Message) and guard.base_msg == old_base_message:
            guard.base_msg = new_base_message
            return guard
        elif isinstance(guard, BaseMessage) and guard == old_base_message:
            return new_base_message
        else:
            return guard

        # The architecture is
    def get_arch_list(self):
        # TODO Murphi backend breaks with following line;
        #      but is this change alright?
        #      Perhaps can find a better fix
        #return [self, self.cache, self.directory]
        if isinstance(self.directory, ProxyDirArchitecture):
            # L1: should return cache arch too, otherwise, NrCacheL1 is too small
            return [self, self.directory, self.cache]
        else:
            # L2: when also return directory arch, a wrong NoneType global_arch constant is created
            return [self, self.cache] #, self.directory]

    def merge_machine_definitions(self):
        # Update the machine definition of the proxy machine
        Debug.perror("Unable to generate proxy cache. Variables in cache and directory have identical identifiers",
                     set(self.directory.machine.variables.keys()).intersection(
                         self.cache.machine.variables))
        self.directory.machine.variables.update(self.cache.machine.variables)
        self.directory.machine.variables_init_val.update(
            self.cache.machine.variables_init_val)
        # Update the machine event definitions from the proxy cache
        Debug.perror("Unable to generate proxy cache. Events in cache and directory have identical identifiers",
                     set(self.directory.machine.variables.keys()).intersection(
                         self.cache.machine.variables))
        self.directory.event_network.event_issue.update(
            self.cache.event_network.event_issue)
        self.directory.event_network.event_ack.update(
            self.cache.event_network.event_ack)

    ####################################################################################################################
    # Hierarchical Functions
    ####################################################################################################################
    def get_flat_base_architecture(self):
        return self.directory
