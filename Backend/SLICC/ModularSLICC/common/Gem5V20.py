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

#  SLICC syntax of gem5 v20 (alloy-gem5, Synapse S4 artifact), for BackendOptions.gem5 == GEM5_V20.
#
#  The templates that differ in meaning (memory interface, sequencer, request types, functional
#  accesses, the message types alloy needs) have their own v20 copy in TempSLICC/<dir>_v20. What is
#  left is syntax that SLICC v20 does not accept and that is rewritten in the generated text:
#    is_valid(<cache>.lookup(<addr>))   ->  <cache>.isTagPresent(<addr>)
#    is_valid(getEntry(<addr>))         ->  hasEntry(<addr>)   (TempSLICC/machines_v20/*_static_functions.sm)
#  since `is_valid`/`is_invalid` only take a variable in SLICC v20 (an expression in v23). Both
#  forms test the same thing: CacheMemory::lookup returns NULL when the tag is not present.

import re
from pathlib import Path

_LOOKUP = re.compile(r"is_(in)?valid\((\w+)\.lookup\((\w+)\)\)")
_GET_ENTRY = re.compile(r"is_(in)?valid\(getEntry\((\w+)\)\)")


def _negate(match: re.Match, positive: str) -> str:
    return f"({positive} == false)" if match.group(1) else positive


def to_v20(text: str) -> str:
    text = _LOOKUP.sub(lambda m: _negate(m, f"{m.group(2)}.isTagPresent({m.group(3)})"), text)
    return _GET_ENTRY.sub(lambda m: _negate(m, f"hasEntry({m.group(2)})"), text)


def rewrite_files(paths) -> None:
    for path in map(Path, paths):
        path.write_text(to_v20(path.read_text()))
