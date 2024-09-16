from collections import OrderedDict

from typing import Dict

from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.common.GenMachineInPorts import GenMachineInPorts
from Backend.SLICC.ModularSLICC.common.GenPCCToSLICC import GenPCCToSLICC
from Backend.SLICC.ModularSLICC.common.GenSLICCTree import GenSLICCTree
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassMultiDict import MultiDict


class GenProxyInPorts(TemplateHandler):

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)
        self.all_message_names = set()

    def gen_proxy_in_ports_str(
            self,
            cluster: Cluster,
            arch: FlatArchitecture,
            in_ports: 'OrderedDict[str, str]',
            out_ports: 'OrderedDict[str, str]'
    ) -> str:

        return "//" + __name__ + self.nl \
               + GenMachineInPorts.gen_machine_in_ports(
                    self, cluster, arch, True, "Cache", in_ports, out_ports) \
               + self.nl
