#  Copyright (c) 2022.  Nicolai Oswald
#  Copyright (c) 2022.  University of Edinburgh
#  Copyright (c) 2026.  Systems Research Group @ TUM
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

from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.proxy.GenProxyBase import GenProxyBase
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassCluster import Cluster


class ModularProxy(GenProxyBase):
    TemplateDir = "TempSLICC/machines"

    def __init__(self, cluster: Cluster, arch: FlatArchitecture, file_name: str, id_mapping: dict[str, str], cache_id: None | int = None):
        GenProxyBase.__init__(self, self.TemplateDir)

        file_name = file_name.split(".")[0] + f"_proxy{cache_id or ''}_synth.sm"

        out_ports = Util.get_out_ports(arch, True)
        in_ports = Util.get_in_ports(arch, True)

        machine_id = id_mapping[str(arch)]
        parked = Util.parked_ports(cluster, arch, in_ports)
        assert len(parked) <= 1, "stall_and_wait keeps one queue per in_port rank: give the ports a rank"


        with open(file_name, "w") as slicc_file:
            # Write header
            slicc_file.write(self.gen_proxy_header_str(arch, id_mapping))
            # Write (indented) body
            slicc_file.write(
                self.fix_tabs(
                    ''.join([
                            self.gen_proxy_state_decl_str(arch, machine_id) + self.nl,
                            self.gen_proxy_events_str(arch, in_ports) + self.nl,
                            self.gen_proxy_struct_str(arch) + self.nl,
                            self.gen_proxy_tbe_str(arch, machine_id) + self.nl,
                            self.gen_proxy_static_fns_str(arch, machine_id, parked) + self.nl,
                            self.gen_proxy_out_ports_str(out_ports) + self.nl,
                            self.gen_proxy_in_ports_str(cluster, arch, in_ports, out_ports, id_mapping) + self.nl,
                            self.gen_proxy_actions_str(cluster, arch, in_ports, out_ports, parked) + self.nl,
                            self.gen_proxy_transitions_str(arch, in_ports, parked),
                        ]),
                    1
                )
                + self.nl
            )
            # Write footer / close the controller
            slicc_file.write(self.gen_proxy_footer_str())
