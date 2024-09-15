from Backend.SLICC.ModularSLICC import SLICCTokens
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.common.GenMachineStruct import GenMachineStruct
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyStruct(TemplateHandler):
    template_file = "entry_structure.sm"

    """
        TODO SLICC adds complexity in that some of a machine's variables
        should go in the TBE, not the Entry... ignoring this for now and just putting it all in the Entry.
    """

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_struct_str(self, arch: FlatArchitecture) -> str:
        const_str = "//" + __name__ + self.nl
        body = None
        for var_name, variable in arch.machine.variables.items():
            # For caches, put only the stable states and the cache line in the Entry.
            # The other variables should go in the TBE.

            if var_name == Util.get_active_cache_line(arch):
                method_fct = SLICCTokens.data_type_map.get(variable.getText(), '_pass_node')
                method = getattr(GenMachineStruct, method_fct)
                res = method(variable)
                if res:
                    body = self.nl + self.tab + res
                    break
        assert body is not None, "No cache line found"

        const_str += self.string_repl_keys(self.open_template(GenProxyStruct.template_file),
                                           ["", "Cache", body]
                                           )
        return const_str + self.nl
