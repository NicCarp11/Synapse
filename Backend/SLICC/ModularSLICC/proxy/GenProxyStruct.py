from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineStruct import GenMachineStruct
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyStruct(TemplateHandler):
    template_file = "entry_structure.sm"

    # all the variables of the machine are in the Entry, none in the TBE

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_struct_str(self, arch: FlatArchitecture) -> str:
        # In general only the members of that come from the directory should be in here
        #  however there seems to be no way to determine where variables came from
        const_str = "//" + __name__ + self.nl
        body = GenMachineStruct.gen_machine_struct_body_str(self, arch)
        const_str += self.string_repl_keys(self.open_template(GenProxyStruct.template_file),
                                           ["", "Proxy", body]
                                           )
        return const_str + self.nl
