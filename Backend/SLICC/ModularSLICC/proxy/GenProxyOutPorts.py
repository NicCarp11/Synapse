from collections import OrderedDict
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common.GenMachineOutPorts import GenMachineOutPorts


class GenProxyOutPorts(TemplateHandler):
    template_file = "out_port.sm"

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_out_ports_str(self, out_ports: 'OrderedDict[str, str]') -> str:
        const_str = "//" + __name__ + self.nl

        const_str += GenMachineOutPorts.gen_machine_out_ports(self, out_ports)
        return const_str + self.nl
