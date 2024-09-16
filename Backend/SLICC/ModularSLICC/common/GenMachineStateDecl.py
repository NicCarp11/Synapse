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

from Algorithms.HeteroGen.ArchTupleStateOrdering import ArchTupleStateOrdering
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassCluster import Cluster
from DataObjects.FlowDataTypes.ClassBaseAccess import Access, BaseAccess
from DataObjects.States.ClassCompoundState import CompoundState
from DataObjects.States.ClassStatev2 import State_v2
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler


class GenMachineStateDecl:

    @staticmethod
    def gen_machine_state_decl_body_str(temp_h: TemplateHandler, arch: BaseArchitecture) -> str:
        state_declarations = []
        for state in sorted(arch.get_architecture_states_verified(), key=lambda s: s.state):
            state_declarations.append(
                temp_h.tab + temp_h.string_repl_keys(
                    temp_h.open_template("state_declaration_entry.sm"),
                    [str(state),
                     GenMachineStateDecl._get_access_permission(arch, state)
                     ]
                )
            )

        return temp_h.nl.join(state_declarations)

    @staticmethod
    def _get_access_permission(arch: BaseArchitecture, state: State_v2) -> str:
        # As far as I know, ProtoGen does not know what permission the directory has in a certain state
        # as it does not model requests coming from the memory controller.
        # For now, using this hacky way to find it.
        # This will break down when cache and dir states do not match exactly, like with MESI.
        # So, TODO actually model the mem controller's permissions

        # This definitely needs to evolve in the future...
        if not cache:
            accesses = Util.get_arch_access_perms(arch, state, GenMachineStateDecl.k_busy)

            if GenMachineStateDecl.k_busy in accesses:
                return "Busy"
        else:
            assert arch.machine.check_cache()
            permissions = [str(trans.guard) for trans in state.getaccesshit()]
            if "store" in permissions:
                return "Read_Write"
            elif "load" in permissions:
                return "Read_Only"
            elif not state.stable:
                return "Busy"
            else:
                return "Invalid"
