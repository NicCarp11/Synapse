from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineHeader import GenMachineHeader
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyHeader(TemplateHandler):

    template_file = "proxy_header.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_header_str(self, arch: FlatArchitecture, machine_id: str):
        const_str = "//" + __name__ + self.nl
        const_str += GenMachineHeader.gen_machine_header_str(self, arch, machine_id, GenProxyHeader.template_file, False)
        return const_str + self.nl
