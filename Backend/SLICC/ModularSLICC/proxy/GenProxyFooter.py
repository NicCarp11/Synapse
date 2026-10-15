from Backend.SLICC.ModularSLICC.TemplateClass import TemplateHandler


class GenProxyFooter(TemplateHandler):

    def __init__(self, handler_dir: str):
        TemplateHandler.__init__(self, handler_dir)

    def gen_proxy_footer_str(self):
        return f"}}{self.nl}// EOF<proxy>{self.nl}"
