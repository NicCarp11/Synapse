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

# Contains two architectures, cache and associated directory, and runs all the basic pre processing algorithms
# A class level is the input to the HieraGen and ProtoGen algorithm

from typing import List

from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture

from Debug.Monitor.ClassDebug import Debug
from Algorithms.ModelChecker.NetworkxModelChecker import NetworkxModelChecker

from Parser.NetworkxParser.ClassProtoParser import ProtoParser

from Algorithms.ProtoDirectory.StateTransactionCompl import StateTransactionCompl


class Level(NetworkxModelChecker, Debug):
    def __init__(self, parser: ProtoParser,
                 level_id: str,
                 gdbg: bool = False):

        Debug.__init__(self, gdbg)
        self.p_header("LEVEL: " + level_id)

        self.parser: ProtoParser = parser
        self.level_id: str = level_id
        self.cluster_id: str = ""

        # Register architecture with its global_arch_level
        self.global_arch = self.parser.global_arch
        self.global_arch.register_level(self)

        disable_directory_auto_completion = False

        self.cache = None
        self.directory = None
        self.l2_private = None
        self.mem = None
        self.snoop = False

        if self.parser.get_cache_architecture():
            self.cache = FlatArchitecture(self.parser.get_cache_architecture())
        if self.parser.get_dir_architecture():
            self.directory = FlatArchitecture(self.parser.get_dir_architecture())
            self.l2_private = FlatArchitecture(self.parser.get_dir_architecture())

        if self.parser.get_mem_architecture():
            if not self.directory:
                self.directory = FlatArchitecture(self.parser.get_mem_architecture())
                self.snoop = True
            else:
                self.mem = FlatArchitecture(self.parser.get_mem_architecture())


        # RUN SSP VERIFICATION
        NetworkxModelChecker.__init__(self, {self.cache, self.directory, self.mem})


        self.level_name = "Level: " + str(level_id) + " | " + \
                          str(self.cache) + " && " + str(self.directory)


        # Rename the cache responses to gen_make it possible to infer serialization

        if not self.snoop and not disable_directory_auto_completion:
            # Message name ambiguity solution
            #SerializationMsgRenaming(self.allowed_state_tuples, self.cache, self.directory)
            # Identify missing requests at directory states. It is possible for directories to receive stale requests,
            # because the system state has changed in the meantime, ProtoGen tries to interpret them rather than Nacking
            # them. It is always possible to revert to Nacking, but will cost the protocol performance
            # by reducing concurrency
            StateTransactionCompl(self.state_tuple_list, self.directory)

        # The renaming of constants and networks must be performed in level, because these variables are shared among
        # the architectures
        self.global_arch.update_global_identifiers(level_id)


        # Classify communication

        # Run ProtoGen

        # Do virtual channel assignment, correctness analysis

        # Do renaming if required



        # Update broadcast tokens to broadcast only in level


        # Classify cache and directory ssp_transitions

        # Murphi
        self.unique_id = []


    # Updates the global architecture mapping
    def get_architectures(self) -> List[FlatArchitecture]:
        if self.mem:
            return [self.cache, self.directory, self.mem]
        return [self.cache, self.directory]

    ####################################################################################################################
    # Drawing functions
    ####################################################################################################################

