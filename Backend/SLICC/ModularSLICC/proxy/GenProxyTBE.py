from Backend.SLICC.ModularSLICC import SLICCTokens
from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler
from Backend.SLICC.ModularSLICC.common import Util
from Backend.SLICC.ModularSLICC.common.GenMachineStruct import GenMachineStruct
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture


class GenProxyTBE(TemplateHandler,):
    template_file = "placeholder_tbe_structure.sm"

    """
        TODO for now this is basically just a placeholder.
        When the time comes to handle DMA properly, this may need to be extended
        (depending on what extra fields the TBE may need).
    """

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_tbe_str(self, arch: FlatArchitecture, machine_id: str) -> str:
        const_str = "//" + __name__ + self.nl
        const_str += self.string_repl_keys(self.open_template(GenProxyTBE.template_file),
                                           [machine_id, ""])
        return const_str + self.nl

