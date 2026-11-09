#  Copyright (c) 2022.  Nicolai Oswald
#  Copyright (c) 2022.  University of Edinburgh
#  Copyright (c) 2026.  Systems Research Group @ TUM
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met: redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer;
#  redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution;
#  neither the name of the copyright holders nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
