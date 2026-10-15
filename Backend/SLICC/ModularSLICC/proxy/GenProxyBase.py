from Backend.SLICC.ModularSLICC.proxy.GenProxyActions import GenProxyActions
from Backend.SLICC.ModularSLICC.proxy.GenProxyEvents import GenProxyEvents
from Backend.SLICC.ModularSLICC.proxy.GenProxyFooter import GenProxyFooter
from Backend.SLICC.ModularSLICC.proxy.GenProxyHeader import GenProxyHeader
from Backend.SLICC.ModularSLICC.proxy.GenProxyInPorts import GenProxyInPorts
from Backend.SLICC.ModularSLICC.proxy.GenProxyOutPorts import GenProxyOutPorts
from Backend.SLICC.ModularSLICC.proxy.GenProxyStateDecl import GenProxyStateDecl
from Backend.SLICC.ModularSLICC.proxy.GenProxyStaticFns import GenProxyStaticFns
from Backend.SLICC.ModularSLICC.proxy.GenProxyStruct import GenProxyStruct
from Backend.SLICC.ModularSLICC.proxy.GenProxyTBE import GenProxyTBE
from Backend.SLICC.ModularSLICC.proxy.GenProxyTransitions import GenProxyTransitions
from Debug.Monitor.ClassDebug import Debug


class GenProxyBase(
        Debug,
        GenProxyHeader,
        GenProxyFooter,
        GenProxyStateDecl,
        GenProxyActions,
        GenProxyEvents,
        GenProxyInPorts,
        GenProxyOutPorts,
        GenProxyStaticFns,
        GenProxyStruct,
        GenProxyTBE,
        GenProxyTransitions):

    def __init__(self, template_dir):
        Debug.__init__(self, debug_enabled=True)
        GenProxyHeader.__init__(self, template_dir)
        GenProxyFooter.__init__(self, template_dir)
        GenProxyStateDecl.__init__(self, template_dir)
        GenProxyActions.__init__(self, template_dir)
        GenProxyOutPorts.__init__(self, template_dir)
        GenProxyStaticFns.__init__(self, template_dir)
        GenProxyStruct.__init__(self, template_dir)
        GenProxyTBE.__init__(self, template_dir)
        GenProxyTransitions.__init__(self, template_dir)
