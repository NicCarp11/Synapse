from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineStateDecl import GenMachineStateDecl
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture

class GenProxyStateDecl(TemplateHandler):
    template_file = "state_declaration.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_state_decl_str(self, arch: FlatArchitecture, machine_id: str) -> str:
        const_str = "//" + __name__ + self.nl
        state_declaration_body = GenMachineStateDecl.gen_machine_state_decl_body_str(self, arch, True)
        init_state = str(arch.init_state)
        const_str += self.string_repl_keys(self.open_template(GenProxyStateDecl.template_file),
                                           [machine_id, init_state, state_declaration_body]
                                           )
        return const_str + self.nl
