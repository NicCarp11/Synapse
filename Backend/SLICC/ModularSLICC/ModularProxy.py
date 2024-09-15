from Backend.SLICC.ModularSLICC.cache.GenCacheBase import GenCacheBase
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.proxy.GenProxyBase import GenProxyBase
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassCluster import Cluster


class ModularProxy(GenProxyBase):
    TemplateDir = "TempSLICC/machines"

    def __init__(self, cluster: Cluster, arch: FlatArchitecture, file_name: str, cache_id: None | int = None):
        GenProxyBase.__init__(self, self.TemplateDir)

        file_name = file_name.split(".")[0] + f"_proxy{cache_id or ''}.sm"

        out_ports = Util.get_out_ports(arch, True)
        in_ports = Util.get_in_ports(arch, True)

        machine_id = f"L{cache_id or 1}Cache";

        with open(file_name, "w") as slicc_file:
            # Write header
            slicc_file.write(self.gen_proxy_header_str(arch, machine_id))
            # Write (indented) body
            slicc_file.write(
                self.add_tabs(
                    ''.join([
                            # self.gen_cache_state_decl_str(arch, machine_id) + self.nl,
                            # self.gen_cache_events_str(arch, in_ports) + self.nl,
                            # self.gen_cache_struct_str(arch) + self.nl,
                            # self.gen_cache_tbe_str(arch, machine_id) + self.nl,
                            # self.gen_cache_static_fns_str(arch, machine_id) + self.nl,
                            # self.gen_cache_out_ports_str(out_ports) + self.nl,
                            # self.gen_cache_in_ports_str(cluster, arch, in_ports, out_ports) + self.nl,
                            # self.gen_cache_actions_str(cluster, arch, in_ports, out_ports) + self.nl,
                            # self.gen_cache_transitions_str(arch, in_ports),
                        ]),
                    1
                )
                + self.nl
            )
            # Write footer / close the controller
            slicc_file.write(self.gen_proxy_footer_str())
