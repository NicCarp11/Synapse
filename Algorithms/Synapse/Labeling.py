#  Labeling of concrete protocol FSMs (Synapse, Sec. V-B).
#
#  Every input protocol (one Level: cache = client side, directory = manager side) is analysed in
#  isolation. Starting from the read/write statements (`load`, `ifetch`, `store`) and from the
#  communication traces between caches and directory computed by the Level's model checker, the
#  stable states and the messages of the protocol are labelled with S/M<Op, Data, Coh>.
#
#  Accesses   load/ifetch: Rd, store: Wr; another access (MESI-RC's ntload, ntstore) the join of
#             the read/write statements its transactions execute
#
#  States
#    cache      Op    permissions of the accesses that hit in the state (served without a message)
#               Data  NP without permission; Dirty if the line was written (store) or inherited dirty
#                     data and no trace since then wrote it back to the directory; Clean otherwise
#               Coh   nco if, in some reachable system state, the state grants Wr while another cache
#                     holds any permission (SWMR does not hold); co otherwise
#    directory  aggregate of the cache states that can coexist with it in a reachable system state
#               (the most permissive Op, the dirtiest Data): what the children may hold
#
#  Messages (roles are inferred from the traces)
#    request    first message of an access trace, cache -> directory
#               load/ifetch: Rd; store: Wr; evict: Wr if it writes dirty data back, None otherwise
#               Coh nco if no trace sending it ends in a state that serves the access locally:
#               the access is performed at the directory (MESI-RC's GetNT, GetACQ, PutNT)
#    forward    directory -> cache, starts a remote trace of a cache; Op is the permission the cache
#               keeps after serving it (Inv/Fwd-GetM: None, Fwd-GetS: Rd)
#    response   completes an access trace; Op is the permission obtained by the requestor
#    other      acks and data replies of remote traces; Op is the permission kept by the sender,
#               except data written back to the directory (WB), which is a Wr
#    Data of a message is NP without payload, otherwise the data state of the sender (Dirty if
#    the trace wrote the block before sending it, e.g. the bytes of a PutNT).
#    A message playing several roles gets the join (least upper bound) of its labels.

from typing import Dict, List, Optional, Set, Tuple

from Algorithms.Synapse.Labels import Coh, Data, Label, Op
from DataObjects.ClassLevel import Level
from DataObjects.FlowDataTypes.ClassBaseAccess import Access, BaseAccess, Evict
from DataObjects.FlowDataTypes.ClassMessage import BaseMessage, Message
from DataObjects.States.ClassStatev2 import State_v2
from DataObjects.Transitions.ClassTransitionv2 import Transition_v2
from Debug.Monitor.ClassDebug import Debug
from Parser.NetworkxParser.ClassProtoParserBase import ProtoParserBase

READ_ACCESSES = (BaseAccess.k_load, BaseAccess.k_ifetch)
WRITE_ACCESSES = (BaseAccess.k_store,)

# Message roles
REQUEST = "request"
FORWARD = "forward"
RESPONSE = "response"
OTHER = "other"


def access_op(access: str) -> Op:
    if access in READ_ACCESSES:
        return Op.RD
    if access in WRITE_ACCESSES:
        return Op.WR
    return Op.NONE


def statement_accesses(transition: Transition_v2) -> Set[str]:
    """Read/write statements executed by a transition (`load;`, `store;`, `ifetch;`)."""
    found = set()
    for op in transition.operations[1:]:
        if str(op) == ProtoParserBase.k_access:
            found.add(str(op.getChildren()[0]))
        elif str(op) in READ_ACCESSES + WRITE_ACCESSES:
            found.add(str(op))
    return found


def sends_data_to(transition: Transition_v2, dests: Set[str]) -> bool:
    """`dests` are destinations as written in the .pcc file (e.g. `directory`)."""
    return any(msg.has_data() and msg.get_dest() in dests for msg in transition.out_msg)


class ProtocolLabels(Debug):
    """Labels of one protocol (Level): stable states of cache and directory, and messages."""

    def __init__(self, level: Level):
        Debug.__init__(self)
        self.level = level
        self.cache = level.cache
        self.directory = level.directory
        self.state_labels: Dict[State_v2, Label] = {}
        self.msg_labels: Dict[str, Label] = {}
        self.msg_roles: Dict[str, Set[str]] = {}
        # requests a cache sends when it evicts the block (PutS, PutE, PutM): it gives up its copy
        self.eviction_requests: Set[str] = set()
        self.access_ops: Dict[str, Op] = self._access_ops()

        self._label_cache_states()
        self._label_directory_states()
        self._label_messages()

    # ------------------------------------------------------------------ states

    def _access_ops(self) -> Dict[str, Op]:
        ops: Dict[str, Op] = {}
        for trace in self._all_traces(self.cache):
            guard = trace[0].guard
            if not isinstance(guard, Access) or str(guard) in READ_ACCESSES + WRITE_ACCESSES:
                continue
            op = Op.NONE
            for transition in trace:
                for statement in statement_accesses(transition):
                    op = op | access_op(statement)
            ops[str(guard)] = ops[str(guard)] | op if str(guard) in ops else op
        return ops

    def access_op(self, access: str) -> Op:
        return self.access_ops.get(access, access_op(access))

    def _label_cache_states(self):
        ops = {state: self._state_op(state) for state in self.cache.stable_states}
        dirty = self._dirty_cache_states(ops)
        nco = self._incoherent_cache_states(ops)
        for state, op in ops.items():
            if op == Op.NONE:
                data = Data.NP
            else:
                data = Data.DIRTY if state in dirty else Data.CLEAN
            self.state_labels[state] = Label("S", op, data, Coh.NCO if state in nco else Coh.CO)

    def _state_op(self, state: State_v2) -> Op:
        # The model checker also counts as a permission an access whose transaction ends where it
        # started (MESI-RC V + ntload); only the accesses served without a message are. An access
        # other than load/ifetch/store counts only if served in the state itself: a protocol rewritten
        # for a Local policy rule takes M from I on a child's ntstore without a message, which grants I nothing
        missing = {str(transition.guard) for transition in state.getaccessmiss()}
        in_place = {str(transition.guard) for transition in state.getaccesshit()
                    if transition.final_state == state}
        op = Op.NONE
        for access in self.cache.stable_state_access_permission_map.get(state, []):
            access = str(access)
            if access in missing or (access not in READ_ACCESSES + WRITE_ACCESSES and access not in in_place):
                continue
            op = op | self.access_op(access)
        return op

    def _directory_destinations(self) -> Set[str]:
        """The ways a cache addresses the directory: by name, or as the source of a message the
        directory sends as itself (`src` ID), e.g. CXL's `MemWr_S` to `BISnpData.src`. Not the
        source of a forward, which is the requesting cache (MESI `Fwd_GetM.src`)."""
        dests = {self._pcc_name(self.directory)}
        for transition in self.directory.get_architecture_transitions():
            for msg in transition.out_msg:
                if msg.get_src() == ProtoParserBase.k_id:
                    dests.add(self._pcc_msg_name(str(msg)))
        return dests

    def _pcc_msg_name(self, name: str) -> str:
        level_id = str(self.level.level_id)
        return name[:-len(level_id)] if level_id and name.endswith(level_id) else name

    def _dirty_cache_states(self, ops: Dict[State_v2, Op]) -> Set[State_v2]:
        directory = self._directory_destinations()
        traces = self._all_traces(self.cache)
        dirty: Set[State_v2] = set()
        changed = True
        while changed:
            changed = False
            for trace in traces:
                final = trace[-1].final_state
                if final in dirty or ops.get(final, Op.NONE) == Op.NONE:
                    continue
                # Data written back to the directory on the way makes the copy clean again
                if any(sends_data_to(t, directory) for t in trace):
                    continue
                wrote = any(statement_accesses(t) & set(WRITE_ACCESSES) for t in trace)
                if wrote or trace[0].start_state in dirty:
                    dirty.add(final)
                    changed = True
        return dirty

    def _system_states(self) -> List[Tuple[State_v2, ...]]:
        return [tuple(system_state.state_tuple) for system_state in self.level.valid_system_states]

    def _incoherent_cache_states(self, ops: Dict[State_v2, Op]) -> Set[State_v2]:
        nco = set()
        for states in self._system_states():
            caches = [s for s in states if s in ops]
            for i, state in enumerate(caches):
                if Op.WR <= ops[state] and any(ops[other] != Op.NONE
                                               for j, other in enumerate(caches) if j != i):
                    nco.add(state)
        return nco

    def _label_directory_states(self):
        coexisting: Dict[State_v2, Label] = {}
        for states in self._system_states():
            dir_states = [s for s in states if s in self.directory.stable_states]
            cache_labels = [self.state_labels[s] for s in states if s in self.state_labels
                            and s not in self.directory.stable_states]
            for dir_state in dir_states:
                for label in cache_labels:
                    label = Label("S", label.op, label.data, label.coh)
                    coexisting[dir_state] = coexisting[dir_state].join(label) \
                        if dir_state in coexisting else label
        for dir_state in self.directory.stable_states:
            # A directory state that never coexists with a valid cache has no children holding data
            self.state_labels[dir_state] = coexisting.get(dir_state, Label("S", Op.NONE, Data.NP))

    # ---------------------------------------------------------------- messages

    def _pcc_name(self, arch) -> str:
        """Name of an architecture as written in the .pcc file (the Level appends its id)."""
        name, level_id = str(arch), str(self.level.level_id)
        return name[:-len(level_id)] if level_id and name.endswith(level_id) else name

    def _all_traces(self, arch) -> List[List[Transition_v2]]:
        traces = []
        for state in arch.stable_states:
            for tree in arch.state_sub_tree_dict.get(state, []):
                traces += arch.get_trans_traces(tree, state, arch.stable_states)
        return traces

    def _label_messages(self):
        directory = self._pcc_name(self.directory)
        ops: Dict[str, Op] = {}
        forward_ops: Dict[str, Op] = {}
        payloads: Dict[str, Data] = {}

        def add(msg: str, role: str, op: Op):
            self.msg_roles.setdefault(msg, set()).add(role)
            ops[msg] = ops[msg] | op if msg in ops else op
            if role == FORWARD:
                forward_ops[msg] = forward_ops[msg] | op if msg in forward_ops else op

        # Data carried by a message: the data state of the sending cache, clean from the directory
        for arch in (self.cache, self.directory):
            for trace in self._all_traces(arch):
                sender_dirty = arch is self.cache and self.state_labels[trace[0].start_state].data == Data.DIRTY
                for transition in trace:
                    # a request carrying the bytes the access just wrote (PutNT)
                    if arch is self.cache and transition is trace[0] and isinstance(transition.guard, Access) \
                            and statement_accesses(transition) & set(WRITE_ACCESSES):
                        sender_dirty = True
                    for msg in transition.out_msg:
                        data = Data.NP
                        if msg.has_data():
                            data = Data.DIRTY if sender_dirty else Data.CLEAN
                        payloads[str(msg)] = payloads[str(msg)] | data if str(msg) in payloads else data

        # A request is nco if no trace sending it ends in a state that serves its access locally (the
        # access is performed at the directory)
        granted: Dict[str, bool] = {}

        # Operation: what the message asks for or grants, seen from the cache traces
        for trace in self._all_traces(self.cache):
            first = trace[0]
            final_label = self.state_labels.get(trace[-1].final_state)
            final_op = final_label.op if final_label else Op.NONE

            if isinstance(first.guard, (Access, Evict)):
                access = str(first.guard)
                for msg in first.out_msg:
                    if msg.get_dest() != directory:
                        continue
                    if access == BaseAccess.k_evict:
                        writes_back = msg.has_data() and \
                            self.state_labels[first.start_state].data == Data.DIRTY
                        add(str(msg), REQUEST, Op.WR if writes_back else Op.NONE)
                        self.eviction_requests.add(str(msg))
                    else:
                        add(str(msg), REQUEST, self.access_op(access))
                        final_state = trace[-1].final_state
                        grants = final_state in self.cache.stable_states and \
                            access in {str(t.guard) for t in final_state.getaccesshit()}
                        granted[str(msg)] = granted.get(str(msg), False) or grants
                for transition in trace[1:]:
                    if isinstance(transition.guard, BaseMessage):
                        add(str(transition.guard), RESPONSE, final_op)
            elif isinstance(first.guard, BaseMessage):
                add(str(first.guard), FORWARD, final_op)

            # Replies sent while serving a forwarded request (acks, forwarded data, write-backs)
            if isinstance(first.guard, BaseMessage):
                for transition in trace:
                    for msg in transition.out_msg:
                        to_directory = msg.get_dest() == directory and msg.has_data()
                        add(str(msg), OTHER, Op.WR if to_directory else final_op)

        # Messages only the directory sends and no cache trace received (e.g. unused acks)
        for msg in payloads:
            if msg not in ops:
                add(msg, OTHER, Op.NONE)

        # A forward is also handled inside the cache's own transactions when the protocol resolves
        # the race explicitly (CXL: BISnpData during a read, answered with BIConflict); what it asks
        # for is what it leaves in the stable states, not the access of the transaction it races
        for msg, op in ops.items():
            coh = Coh.NCO if granted.get(msg, True) is False else Coh.CO
            self.msg_labels[msg] = Label("M", forward_ops.get(msg, op), payloads.get(msg, Data.NP), coh)

    # ----------------------------------------------------------------- queries

    def label(self, item) -> Optional[Label]:
        if isinstance(item, State_v2):
            return self.state_labels.get(item)
        if isinstance(item, Message):
            item = item.base_msg
        return self.msg_labels.get(str(item))

    def table(self) -> List[List[str]]:
        rows = []
        for arch in (self.cache, self.directory):
            for state in sorted(arch.stable_states, key=str):
                rows.append([str(arch), "state", str(state), str(self.state_labels[state])])
        for msg in sorted(self.msg_labels):
            rows.append(["network", "/".join(sorted(self.msg_roles[msg])), msg, str(self.msg_labels[msg])])
        return rows
