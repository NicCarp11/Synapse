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
