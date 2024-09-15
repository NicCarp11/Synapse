from Backend.SLICC.ModularSLICC.proxy.GenProxyFooter import GenProxyFooter
from Backend.SLICC.ModularSLICC.proxy.GenProxyHeader import GenProxyHeader
from Debug.Monitor.ClassDebug import Debug


class GenProxyBase(
        Debug,
        GenProxyHeader,
        GenProxyFooter):

    def __init__(self, template_dir):
        Debug.__init__(self, debug_enabled=True)
        GenProxyHeader.__init__(self, template_dir)
        GenProxyFooter.__init__(self, template_dir)