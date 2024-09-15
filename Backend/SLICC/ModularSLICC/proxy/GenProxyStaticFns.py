from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassLevel import Level
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util


class GenProxyStaticFns(TemplateHandler):
    template_file = "cache_static_functions.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_static_fns_str(self, arch: FlatArchitecture, machine_id: str) -> str:
        const_str = "//" + __name__ + self.nl
        const_str += self.string_repl_keys(self.open_template(GenProxyStaticFns.template_file),
                                           [str(arch.init_state),
                                            Util.get_active_cache_line(arch),
                                            machine_id
                                            ]
                                           )
        return const_str + self.nl
