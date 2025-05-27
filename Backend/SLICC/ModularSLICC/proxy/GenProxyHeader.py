from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineHeader import GenMachineHeader
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyHeader(TemplateHandler):

    template_file = "proxy_header.sm"

    template_file_2 = "proxy_header_L2private.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_header_str(self, arch: FlatArchitecture, id_mapping: dict[str, str]):
        const_str = "//" + __name__ + self.nl
        list(id_mapping.keys()).index(arch.arch_name)
        keys = list(id_mapping.keys())
        index = keys.index(arch.arch_name)
        if index < len(keys) - 2:
            const_str += GenMachineHeader.gen_machine_header_str(self, arch, id_mapping, GenProxyHeader.template_file_2, False)
        else:
            const_str += GenMachineHeader.gen_machine_header_str(self, arch, id_mapping, GenProxyHeader.template_file, False)

        return const_str + self.nl
