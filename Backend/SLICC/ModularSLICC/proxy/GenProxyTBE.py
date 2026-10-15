from Backend.SLICC.ModularSLICC import SLICCTokens
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineStruct import GenMachineStruct
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyTBE(TemplateHandler,):
    template_file = "placeholder_tbe_structure.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_tbe_str(self, arch: FlatArchitecture, machine_id: str) -> str:
        const_str = "//" + __name__ + self.nl
        body_strs = []
        for var_name, variable in arch.machine.variables.items():
            # For caches, put everything except the actual cache line in the TBE
            method_fct = SLICCTokens.data_type_map.get(variable.getText(), '_pass_node')
            method = getattr(GenMachineStruct, method_fct)
            res = method(variable, arch)
            if res and (variable.getText() == "INT_")  or (variable.getText() =="DATA_"):
                body_strs.append(self.tab + res)
        const_str += self.string_repl_keys(self.open_template(GenProxyTBE.template_file),
                                           [machine_id, self.nl.join(body_strs)])
        return const_str + self.nl
