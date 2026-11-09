"""Local rules of a policy: a controller that takes write permission itself, without its parent.

`Local( S(..), M(..), S(..) )` (Policy.py) lets a controller serve a child's write (e.g. a MESI-RC
non-temporal store) by taking the dirty writable state of its parent's protocol on its own. The
parent's protocol is rewritten for it before the synthesis:

  cache side      the child's access takes the dirty writable state (M) in every stable state,
                  without a message, and the eviction from that state also accepts the answer the
                  directory gives a sharer's write-back;
  directory side  a dirty write-back from a cache the directory does not know as the owner writes
                  the block: in the state without copies it is answered as the owner's write-back,
                  from a sharer as that sharer's write-back. The clean evictions keep their answer.

This is sound only if every block has a single cache at the controller's level, which the caller
checks on the topology.
"""

import re
from typing import List, Optional, Tuple

from Algorithms.Synapse.Labeling import ProtocolLabels
from Algorithms.Synapse.Labels import Data, Op
from DataObjects.ClassLevel import Level
from DataObjects.FlowDataTypes.ClassBaseAccess import BaseAccess


class LocalWriteError(Exception):
    """The parent's protocol does not have the shape the rewriting needs."""


_PROCESS = re.compile(r"Process\(\s*(\w+)\s*,\s*(\w+)\s*(?:,\s*(\w+)\s*)?\)\s*\{")


def _closing(text: str, opening: int) -> int:
    """Index just after the brace that closes the one at `opening`."""
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index + 1
    raise LocalWriteError("unbalanced braces")


def _architecture(text: str, name: str) -> Tuple[int, int]:
    match = re.search(rf"Architecture\s+{name}\s*\{{", text)
    if not match:
        raise LocalWriteError(f"no Architecture {name}")
    return match.end(), _closing(text, match.end() - 1) - 1


def _blocks(text: str, span: Tuple[int, int]) -> List[Tuple[int, int, str, str, Optional[str]]]:
    """(start of line, end, state, guard, final state) of every Process block in `span`."""
    blocks = []
    position = span[0]
    while True:
        match = _PROCESS.search(text, position, span[1])
        if not match:
            return blocks
        end = _closing(text, match.end() - 1)
        blocks.append((text.rfind("\n", 0, match.start()) + 1, end, *match.groups()))
        position = end


def _find(blocks, state: str, guard: str):
    return next((block for block in blocks if block[2] == state and block[3] == guard), None)


def _on_path(text: str, start: int, end: int) -> bool:
    """Whether a statement at `start` encloses `end` (no block closes in between)."""
    depth = 0
    for char in text[start:end]:
        depth += {"{": 1, "}": -1}.get(char, 0)
        if depth < 0:
            return False
    return True


def _answers(text: str, block, message: str, before: Optional[int] = None, top_level: bool = False) -> List[str]:
    """The `msg = ...(..., <message>.src ...); net.send(msg);` statements of a block, those on the
    way to `before` or, with `top_level`, those outside any branch."""
    start, end = block[0], block[1]
    body = text.index("{", start) + 1
    statements = []
    for match in re.finditer(rf"msg\s*=\s*\w+\([^;]*\b{message}\.src\b[^;]*\)\s*;\s*\w+\.send\(msg\)\s*;", text[body:end]):
        position = body + match.start()
        if before is not None and (position > before or not _on_path(text, position, before)):
            continue
        if top_level and text[body:position].count("{") != text[body:position].count("}"):
            continue
        statements.append(re.sub(r";\s*", ";\n", match.group(0)).strip())
    return statements


def derive(text: str, level: Level, accesses: List[str]) -> str:
    """The parent's protocol `text` (parsed as `level`) with the child's write `accesses` taken
    locally (module docstring)."""
    labels = ProtocolLabels(level)
    base = lambda name: re.sub(r"L\d+$", "", str(name))
    cache_labels = {str(s): labels.state_labels[s] for s in level.cache.stable_states}
    dir_labels = {str(s): labels.state_labels[s] for s in level.directory.stable_states}
    dirty = [s for s, label in cache_labels.items() if Op.WR <= label.op and label.data == Data.DIRTY]
    if len(dirty) != 1:
        raise LocalWriteError(f"the cache needs one dirty writable state, it has {dirty or 'none'}")
    owned = dirty[0]
    evictions = {}
    for transition in level.cache.get_architecture_transitions():
        if isinstance(transition.guard, BaseAccess.Evict) and transition.start_state.stable and transition.out_msg:
            evictions[str(transition.start_state)] = base(transition.out_msg[0])
    if owned not in evictions:
        raise LocalWriteError(f"no eviction from {owned}")
    write_back = evictions[owned]
    clean = list(dict.fromkeys(evictions[s] for s, label in cache_labels.items()
                               if label.data == Data.CLEAN and s in evictions))

    # --- directory
    span = _architecture(text, "directory")
    blocks = _blocks(text, span)
    data_write = re.compile(rf"\w+\s*=\s*{write_back}\.\w+\s*;")
    owners = [b for b in blocks if b[3] == write_back and data_write.search(text, b[0], b[1])]
    if not owners:
        raise LocalWriteError(f"the directory never writes the data of {write_back}")
    owner = owners[0]
    write = data_write.search(text, owner[0], owner[1])
    owner_answer = _answers(text, owner, write_back, before=write.start()) + [write.group(0)]
    empty = [s for s, label in dir_labels.items() if label.op == Op.NONE]
    if len(empty) != 1:
        raise LocalWriteError("the directory needs one state without copies")
    empty = empty[0]
    sharers = [s for s in dir_labels if s != empty and s not in {b[2] for b in owners}]

    edits: List[Tuple[int, int, str]] = []      # (start, end, replacement) on the original text
    added: List[str] = []                       # blocks appended to the directory
    indent = "    "

    def block_text(header: str, statements: List[str]) -> str:
        body = "".join(f"{indent}   {line}\n" for statement in statements for line in statement.split("\n"))
        return f"{indent}{header}{{\n{body}{indent}}}\n"

    old = _find(blocks, empty, write_back)
    for message in clean:
        if _find(blocks, empty, message):
            continue
        if old:                                 # it was derived from the old handler: keep it
            copy = re.sub(rf"\b{write_back}\b", message, text[old[0]:old[1]])
            added.append(copy + "\n")
        else:
            reference = next((_find(blocks, s, message) for s in sharers if _find(blocks, s, message)), None)
            answer = _answers(text, reference, message, top_level=True) if reference else []
            added.append(block_text(f"Process({empty}, {message}, {empty})", answer))
    added.append(block_text(f"Process({empty}, {write_back}, {empty})",
                            [re.sub(rf"\b{owner[3]}\b", write_back, line) for line in owner_answer]))
    if old:
        edits.append((old[0], old[1] + (1 if text[old[1]:old[1] + 1] == "\n" else 0), ""))

    sharer_answers = set()
    for state in sharers:
        handler = _find(blocks, state, write_back)
        if handler:
            branch = re.search(rf"if\s+cache\.contains\(\s*{write_back}\.src\s*\)\s*\{{", text[handler[0]:handler[1]])
            if not branch:
                raise LocalWriteError(f"{state} + {write_back}: no branch for a sharer")
            opening = handler[0] + branch.end() - 1
            inner = (opening, _closing(text, opening))
            send = re.search(r"\w+\.send\(msg\)\s*;", text[inner[0]:inner[1]])
            position = inner[0] + send.end()
            edits.append((position, position, f"\n{indent * 3}{write.group(0)}"))
            sharer_answers |= set(re.findall(r"\(\s*(\w+)\s*,", " ".join(
                _answers(text, (inner[0], inner[1]), write_back, top_level=False))))
        else:
            reference = next((_find(blocks, state, m) for m in clean if _find(blocks, state, m)), None)
            if reference is None:
                continue
            copy = re.sub(rf"\b{reference[3]}\b", write_back, text[reference[0]:reference[1]])
            delete = re.search(r"cache\.del\(", copy)
            guard = f"if cache.contains({write_back}.src){{\n{indent * 3}{write.group(0)}\n{indent}   }}\n{indent}   "
            copy = copy[:delete.start()] + guard + copy[delete.start():] if delete else copy
            added.append(copy + "\n")
            sharer_answers |= set(re.findall(r"\(\s*(\w+)\s*,", " ".join(
                _answers(copy + " ", (0, len(copy)), write_back, top_level=True))))

    # --- cache
    cache_span = _architecture(text, "cache")
    cache_blocks = _blocks(text, cache_span)
    evict = _find(cache_blocks, owned, "evict")
    awaits = re.search(r"await\s*\{", text[evict[0]:evict[1]])
    if awaits:
        opening = evict[0] + awaits.end() - 1
        closing = _closing(text, opening) - 1
        arms = text[opening:closing]
        owner_acks = re.findall(r"\(\s*(\w+)\s*,", " ".join(owner_answer))
        final = next((m.group(1) for ack in owner_acks for m in
                      [re.search(rf"when\s+{ack}\s*:[^}}]*?State\s*=\s*(\w+)", arms)] if m), None)
        missing = [a for a in sorted(sharer_answers) if not re.search(rf"when\s+{a}\s*:", arms)]
        if missing and final:
            arm = "".join(f"\n{indent * 3}when {a}:\n{indent * 4}State = {final};\n{indent * 4}break;\n"
                          for a in missing)
            edits.append((closing, closing, arm + indent * 2))
    cache_added = []
    for state in cache_labels:
        for access in accesses:
            if _find(cache_blocks, state, access):
                continue
            header = f"Process({state}, {access})" if state == owned else f"Process({state}, {access}, {owned})"
            cache_added.append(f"{indent}{header}{{\n{indent * 2}store;\n{indent}}}\n")

    edits.append((cache_span[1], cache_span[1], "\n" + "".join(cache_added)))
    edits.append((span[1], span[1], "\n" + "".join(added)))
    for start, end, replacement in sorted(edits, key=lambda edit: edit[0], reverse=True):
        text = text[:start] + replacement + text[end:]
    return text
