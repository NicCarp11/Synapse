#  Abstract labels of Synapse (MICRO'26, Sec. V-A).
#
#  States and messages of every concrete protocol FSM are labelled with
#      S<Op, Data, Coh>   (abstract state)
#      M<Op, Data, Coh>   (abstract message)
#  Op   in {None, Rd, Wr, RdWr}   operation permission
#  Data in {NP, Clean, Dirty}     data state (NP: not present; "None" is accepted for messages)
#  Coh  in {co, nco}              coherence
#
#  Policies match labels against *patterns* (Policy.py). Pattern semantics:
#  - `_` matches anything.
#  - Op: `None` matches only None; `Rd`, `Wr`, `RdWr` match every label granting *at least* that
#    permission (RdWr matches Rd), so that S(Rd,P,_) is satisfied both by F<Rd> and E<RdWr> as in
#    the paper's example. Alternatives can be listed with `|` (`Rd|None`).
#  - Data: `NP`, `Clean`, `Dirty`, `P` (present = Clean|Dirty); `None` is an alias of NP.
#  - Coh: `co`, `nco`.

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable


class Op(Enum):
    NONE = "None"
    RD = "Rd"
    WR = "Wr"
    RDWR = "RdWr"

    @property
    def perms(self) -> FrozenSet[str]:
        return {Op.NONE: frozenset(), Op.RD: frozenset("r"), Op.WR: frozenset("w"),
                Op.RDWR: frozenset("rw")}[self]

    @staticmethod
    def from_perms(perms: Iterable[str]) -> "Op":
        perms = frozenset(perms)
        return {frozenset(): Op.NONE, frozenset("r"): Op.RD, frozenset("w"): Op.WR,
                frozenset("rw"): Op.RDWR}[perms]

    def __or__(self, other: "Op") -> "Op":
        return Op.from_perms(self.perms | other.perms)

    def __le__(self, other: "Op") -> bool:
        return self.perms <= other.perms

    def __lt__(self, other: "Op") -> bool:
        return self.perms < other.perms

    def __str__(self):
        return self.value


class Data(Enum):
    NP = "NP"
    CLEAN = "Clean"
    DIRTY = "Dirty"

    @property
    def rank(self) -> int:
        return {Data.NP: 0, Data.CLEAN: 1, Data.DIRTY: 2}[self]

    def __or__(self, other: "Data") -> "Data":
        return self if self.rank >= other.rank else other

    def __str__(self):
        return self.value


class Coh(Enum):
    CO = "co"
    NCO = "nco"

    def __or__(self, other: "Coh") -> "Coh":
        return Coh.NCO if Coh.NCO in (self, other) else Coh.CO

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Label:
    kind: str  # 'S' (state) or 'M' (message)
    op: Op
    data: Data
    coh: Coh = Coh.CO

    def __post_init__(self):
        assert self.kind in ("S", "M"), self.kind

    def join(self, other: "Label") -> "Label":
        """Least upper bound, used when one message plays several roles."""
        assert self.kind == other.kind
        return Label(self.kind, self.op | other.op, self.data | other.data, self.coh | other.coh)

    def __str__(self):
        data = "None" if self.kind == "M" and self.data == Data.NP else str(self.data)
        return f"{self.kind}<{self.op}, {data}, {self.coh}>"


ANY = "_"


@dataclass(frozen=True)
class LabelPattern:
    kind: str
    ops: FrozenSet[Op] | None      # None: wildcard; otherwise "at least" one of these (exact for Op.NONE)
    datas: FrozenSet[Data] | None  # None: wildcard
    cohs: FrozenSet[Coh] | None    # None: wildcard

    def matches(self, label: Label) -> bool:
        if label.kind != self.kind:
            return False
        if self.ops is not None and not any(self._op_matches(p, label.op) for p in self.ops):
            return False
        if self.datas is not None and label.data not in self.datas:
            return False
        if self.cohs is not None and label.coh not in self.cohs:
            return False
        return True

    @staticmethod
    def _op_matches(pattern: Op, op: Op) -> bool:
        if pattern == Op.NONE:
            return op == Op.NONE
        return pattern <= op

    def __str__(self):
        def fmt(values, order):
            if values is None:
                return ANY
            return "|".join(str(v) for v in order if v in values)
        datas = fmt(self.datas, list(Data))
        if self.datas == frozenset({Data.CLEAN, Data.DIRTY}):
            datas = "P"
        elif self.kind == "M" and self.datas == frozenset({Data.NP}):
            datas = "None"
        return f"{self.kind}({fmt(self.ops, list(Op))},{datas},{fmt(self.cohs, list(Coh))})"


_OP_ATOMS = {"None": Op.NONE, "Rd": Op.RD, "Wr": Op.WR, "RdWr": Op.RDWR}
_DATA_ATOMS = {"NP": {Data.NP}, "None": {Data.NP}, "Clean": {Data.CLEAN}, "Dirty": {Data.DIRTY},
               "P": {Data.CLEAN, Data.DIRTY}}
_COH_ATOMS = {"co": Coh.CO, "nco": Coh.NCO}


def parse_pattern(kind: str, op: str, data: str, coh: str) -> LabelPattern:
    """Builds a pattern from the three textual fields of S(...)/M(...)."""
    def alternatives(text: str, atoms: dict, what: str):
        text = text.strip()
        if text == ANY:
            return None
        values = set()
        for atom in text.split("|"):
            atom = atom.strip()
            if atom not in atoms:
                raise ValueError(f"unknown {what} '{atom}' (expected one of {sorted(atoms)} or {ANY})")
            value = atoms[atom]
            values |= value if isinstance(value, set) else {value}
        return frozenset(values)

    return LabelPattern(kind, alternatives(op, _OP_ATOMS, "operation"),
                        alternatives(data, _DATA_ATOMS, "data state"),
                        alternatives(coh, _COH_ATOMS, "coherence"))
