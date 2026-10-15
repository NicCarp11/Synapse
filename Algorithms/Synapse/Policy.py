#  Caching policies (Synapse, Sec. V-A, VI-A).
#
#  A policy is an ordered list of rules
#      Rule( S(op,data,coh), M(op,data,coh), S(op,data,coh) );
#  read as  initialState + Message -> finalState  (pattern semantics in Labels.py). For a request
#  received from a child, the first rule whose initial-state pattern matches the label of the current
#  client state and whose message pattern matches the label of the request gives the abstract state
#  the client must reach before the manager serves the request (Alg. 1, line 3).
#
#  Policy files reuse the SSP comment syntax:
#      // write-back, inclusive
#      Policy WB_INCL {
#          Rule( S(_,NP,_), M(Rd,None,_), S(Rd,P,_) );   // read miss
#      }
#  A file may contain several policies; `load_policy(path, name)` selects one by name.
#
#  A rule written `Local( ... )` instead of `Rule( ... )` is served by the controller on its own: it
#  takes the final state without asking its parent (e.g. the bytes of a child's non-temporal store
#  written into an LLC that owns the block's address range). The parent's protocol is rewritten for
#  it (LocalWrite.py); every block must have a single cache at the controller's level.
#
#  Requests from the parent are steered by the client (Alg. 1, line 11): by default the children
#  are downgraded only as far as the client's final state requires. A policy can ask for more with
#      Downgrade( S(op,data,coh), M(op,data,coh), S(op,data,coh) );
#  read as: on a request from the parent matching M, received in a client state matching the first
#  S, downgrade the children to at most the second S (e.g. an inclusive LLC that recalls the block
#  from its children on every forward that takes write permission away from it). The short form
#      Downgrade( M(op,data,coh), S(op,data,coh) );
#  applies in any client state.
#
#  Where the controller keeps the data (inclusion, Alg. 1 lines 4 and 8):
#      Data( S(op,data,coh) );
#  the controller holds a copy of the block only while its children's abstract state (the label of
#  the manager state) matches the pattern; elsewhere the block's data lives in the children and the
#  controller keeps the coherence state only (a tag). Without it the controller always holds the
#  data (inclusive). `Data( S(None,NP,_) )` is an exclusive controller.
#
#  A child that drops its copy must then hand the data back with the message it sends (the
#  protocol's evictions carry the block, e.g. MESIF PutS/PutE); the controller keeps it where the
#  policy places the data (Synthesis._keep_returned_data).

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from Algorithms.Synapse.Labels import Label, LabelPattern, parse_pattern

_FIELD = r"\s*([^,()]+?)\s*"
_TERM = r"\s*([SM])\s*\(" + _FIELD + "," + _FIELD + "," + _FIELD + r"\)\s*"
_RULE_RE = re.compile(r"(Rule|Local)\s*\(" + _TERM + "," + _TERM + "," + _TERM + r"\)\s*;?")
_DOWNGRADE_RE = re.compile(r"Downgrade\s*\(" + _TERM + "," + _TERM + r"\)\s*;?")
_DOWNGRADE3_RE = re.compile(r"Downgrade\s*\(" + _TERM + "," + _TERM + "," + _TERM + r"\)\s*;?")
_DATA_RE = re.compile(r"Data\s*\(" + _TERM + r"\)\s*;?")
_POLICY_RE = re.compile(r"Policy\s+(\w+)\s*\{(.*?)\}", re.S)


@dataclass(frozen=True)
class Rule:
    start: LabelPattern
    msg: LabelPattern
    final: LabelPattern
    text: str = ""
    local: bool = False     # Local( ... ): reached without the parent

    def __post_init__(self):
        if (self.start.kind, self.msg.kind, self.final.kind) != ("S", "M", "S"):
            raise ValueError(f"a rule must be Rule(S(..), M(..), S(..)): {self.text}")

    def matches(self, state: Label, msg: Label) -> bool:
        return self.start.matches(state) and self.msg.matches(msg)

    def __str__(self):
        return f"{'Local' if self.local else 'Rule'}( {self.start}, {self.msg}, {self.final} )"


@dataclass(frozen=True)
class Downgrade:
    client: LabelPattern
    msg: LabelPattern
    children: LabelPattern
    text: str = ""

    def __post_init__(self):
        if (self.client.kind, self.msg.kind, self.children.kind) != ("S", "M", "S"):
            raise ValueError(f"a downgrade must be Downgrade(S(..), M(..), S(..)): {self.text}")

    def matches(self, client: Label, msg: Label) -> bool:
        return self.client.matches(client) and self.msg.matches(msg)

    def __str__(self):
        return f"Downgrade( {self.client}, {self.msg}, {self.children} )"


class Policy:
    def __init__(self, name: str, rules: List[Rule], downgrades: List[Downgrade] = None,
                 data: Optional[LabelPattern] = None):
        self.name = name
        self.rules = rules
        self.downgrades = downgrades or []
        self.data = data

    @property
    def local_rules(self) -> List[Rule]:
        return [rule for rule in self.rules if rule.local]

    @property
    def exclusive(self) -> bool:
        return self.data is not None

    def keeps_data(self, children: Label) -> bool:
        """Data( ... ): whether the controller holds the block's data while its children are in the
        abstract state `children` (always, without the directive)."""
        return self.data is None or self.data.matches(children)

    def children_target(self, client: Label, msg: Label) -> Optional[LabelPattern]:
        """State the children must be downgraded to on a request from the parent received in the
        client state labelled `client`, if the policy asks for more than the client's final state
        (first matching Downgrade rule)."""
        for downgrade in self.downgrades:
            if downgrade.matches(client, msg):
                return downgrade.children
        return None

    def match_rule(self, state: Label, msg: Label) -> Optional[Rule]:
        """policy.match-rule() of Alg. 1: the first rule matching (client state, request)."""
        for rule in self.rules:
            if rule.matches(state, msg):
                return rule
        return None

    def __str__(self):
        extra = [f"Data( {self.data} )"] if self.data is not None else []
        return f"Policy {self.name} {{\n" + "".join(f"    {rule};\n" for rule in self.rules + self.downgrades) \
            + "".join(f"    {line};\n" for line in extra) + "}"


def _strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def parse_rules(text: str) -> Tuple[List[Rule], List[Downgrade], Optional[LabelPattern]]:
    remainder = _DATA_RE.sub("", text)
    remainder = _DOWNGRADE_RE.sub("", _DOWNGRADE3_RE.sub("", _RULE_RE.sub("", remainder)))
    if remainder.strip():
        raise ValueError(f"cannot parse policy text: {remainder.strip()[:80]!r}")
    rules = []
    for m in _RULE_RE.finditer(text):
        g = m.groups()[1:]
        rules.append(Rule(parse_pattern(g[0], *g[1:4]), parse_pattern(g[4], *g[5:8]),
                          parse_pattern(g[8], *g[9:12]), m.group(0).strip(), m.group(1) == "Local"))
    downgrades = []
    for m in sorted(list(_DOWNGRADE3_RE.finditer(text)) + list(_DOWNGRADE_RE.finditer(text)),
                    key=lambda m: m.start()):
        g = m.groups()
        if len(g) == 12:
            client, msg, children = g[0:4], g[4:8], g[8:12]
        else:
            client, msg, children = ("S", "_", "_", "_"), g[0:4], g[4:8]
        downgrades.append(Downgrade(parse_pattern(*client), parse_pattern(*msg),
                                    parse_pattern(*children), m.group(0).strip()))
    data_matches = list(_DATA_RE.finditer(text))
    if len(data_matches) > 1:
        raise ValueError("a policy has at most one Data( ... )")
    data = parse_pattern(*data_matches[0].groups()) if data_matches else None
    return rules, downgrades, data


def parse_policies(text: str) -> List[Policy]:
    text = _strip_comments(text)
    policies = [Policy(m.group(1), *parse_rules(m.group(2))) for m in _POLICY_RE.finditer(text)]
    if not policies:
        raise ValueError("no `Policy <name> { ... }` block found")
    return policies


def load_policy(path: Path, name: Optional[str] = None) -> Policy:
    """Loads the policy `name` of a file (the only one of the file if no name is given)."""
    policies = parse_policies(Path(path).read_text())
    if name is None:
        if len(policies) != 1:
            raise ValueError(f"{path} defines {[p.name for p in policies]}, select one by name")
        return policies[0]
    for policy in policies:
        if policy.name == name:
            return policy
    raise ValueError(f"policy {name} not found in {path}")
