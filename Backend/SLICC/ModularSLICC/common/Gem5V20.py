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
