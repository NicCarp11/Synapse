#  Synthesis of an intermediate coherence controller (Synapse, Alg. 1).
#
#  The controller fuses
#    manager  the directory of the on-core protocol (lower level), extended with HieraGen's
#             proxy cache (ProxyDirArchitecture) so that it can serve virtual requests
#    client   the cache of the off-core protocol (higher level)
#    policy   the caching policy (Policy.py)
#  into one FSM over compound states (manager state, client state).
#
#  For every compound state (m, c):
#  * request from a child (Alg. 1, lines 2-9): the policy gives the abstract state the client must
#    reach. If c already satisfies it, only the manager transaction runs. Otherwise the client
#    transaction that repeats the requestor's access (same access, or the access with the same Op)
#    and ends in a matching state runs first, and the manager transaction is chained to it; the
#    request is deferred into proxy_msg<level> (HieraGen's encapsulation, NestTreeNetworkx).
#  * request from the parent (Alg. 1, lines 10-16): the client transaction gives the client's final
#    state. If the children may hold more than it allows, the manager first runs the virtual request
#    of the proxy cache that downgrades them (store: to None, load: to Rd), then the client serves
#    the request.
#  * eviction of the client: the cache is inclusive, so the children are invalidated first.
#  Allocation and deallocation of the cache block (Alg. 1, lines 4 and 8) are left to the back end,
#  which allocates the entry in states without data (Backend/SLICC).
#  * exclusive policy (`Data( ... )`, Policy.py): in the compound states where the children hold the
#    block the controller keeps no data (keeps_data), the back end keeps those entries as tags; a
#    client that must answer the parent with data it does not hold takes it from the children first
#    (the manager's virtual load or store, as for a downgrade).
#
#  Concurrency: ProtoGen runs on both levels before the composition (race transitions of the
#  client and of the on-core caches). Client transactions are chained with the manager without
#  their race paths (_is_racing); requests reaching the controller in a transient state are
#  stalled by the back end and served once it is stable (HieraGen's stalling variant).

import re
from typing import Dict, List, Optional, Set, Tuple

import networkx as nx

from networkx import MultiDiGraph

from Algorithms.ControllerGeneration.General.ChainTransitions import ChainTransitions
from Algorithms.General.AuxStateHandler import AuxStateHandler
from Algorithms.ControllerGeneration.NetworkxGeneral.CompoundStateGenNetworkx import CompoundStateGenNetworkx
from Algorithms.ControllerGeneration.NetworkxGeneral.MergeGraphsNetworkx import MergeGraphsNetworkx
from Algorithms.ControllerGeneration.NetworkxGeneral.NestTreeNetworkx import NestTreeNetworkx
from Algorithms.ControllerGeneration.ProxyDirController.ClassProxyDirArchitecture import ProxyDirArchitecture
from Algorithms.HeteroGen.ArchTupleStateOrdering import ArchTupleStateOrdering
from Algorithms.HeteroGen.ClassHHDirArchitecture import HHDirArchitecture
from Algorithms.ProtoAlgoNetworkx.ProtoNetworkxBase import ProtoNetworkxBase
from Algorithms.Synapse.Labeling import FORWARD, READ_ACCESSES, REQUEST, ProtocolLabels
from Algorithms.Synapse.Labels import Data, Label, LabelPattern, Op
from Algorithms.Synapse.Policy import Policy
from DataObjects.Architecture.ClassFlatArchitecture import FlatArchitecture
from DataObjects.ClassLevel import Level
from DataObjects.FlowDataTypes.ClassBaseAccess import Access, BaseAccess, Evict
from DataObjects.FlowDataTypes.ClassEvent import Event
from DataObjects.FlowDataTypes.ClassMessage import BaseMessage, Message
from DataObjects.States.ClassCompoundState import CompoundState
from DataObjects.States.ClassStatev2 import State_v2
from DataObjects.Transitions.ClassTransitionv2 import Transition_v2
from Debug.Monitor.ClassDebug import Debug
from Debug.Monitor.ProtoCCTable import ProtoCCTablePrinter
from Parser.ProtoCCcomTreeFct import toStringList


class SynthesisError(Exception):
    """The policy and the protocols are incompatible (Sec. VI-B)."""


class SynapseDirArchitecture(HHDirArchitecture):

    def __init__(self, lower_level: Level, higher_level: Level, policy: Policy, gdbg: bool = False):
        # HHDirArchitecture.__init__ runs HeteroGen; only its helper methods are reused here.
        self.gdbg = gdbg
        self.policy = policy
        self.lower_level = lower_level
        self.higher_level = higher_level

        # Labels are computed on the input protocols (Sec. V-B)
        self.manager_labels = ProtocolLabels(lower_level)
        self.client_labels = ProtocolLabels(higher_level)

        # Manager: on-core directory with HieraGen's proxy cache; concurrency of both levels (ProtoGen)
        ProxyDirArchitecture(lower_level)
        ProtoNetworkxBase(lower_level)
        ProtoNetworkxBase(higher_level)
        self.manager: FlatArchitecture = lower_level.directory
        self.client: FlatArchitecture = higher_level.cache
        self.manager.level = lower_level
        self.client.level = higher_level
        self.stored_returns: List[str] = []
        self._keep_returned_data()

        ArchTupleStateOrdering.__init__(self, (self.manager, self.client))
        NestTreeNetworkx.__init__(self, self.manager, (self.manager, self.client))
        self.graph_state_to_heterogen_state_map: Dict = {}

        # (compound state, guard) of the handlers in which the client fetches the block
        self.fetching_requests: Set[Tuple[str, str]] = set()
        self.warnings: List[str] = []
        # race transitions continued in the compound state of the downgraded manager, with the
        # compound state they would otherwise end in (_nest_races, _check_race_redirects)
        self._race_redirects: List[Tuple[Transition_v2, CompoundState]] = []
        # name of a race state nested by _nest_races -> prefix (child request) of its transaction
        self._race_state_owners: Dict[str, str] = {}

        compound_states = self.gen_theoretical_state_space((self.manager, self.client))
        fsm_transitions = self.gen_synapse_transitions(compound_states)

        fsm_stable_states = self.get_valid_stable_states(compound_states, fsm_transitions)
        fsm_init_state = self.gen_initial_state((self.manager, self.client))

        FlatArchitecture.__init__(self, self.manager, self.gdbg)
        self.update_base_fsm(fsm_init_state, fsm_stable_states, set(fsm_transitions))
        lower_level.directory = self

        merged_arch = self.merge_base_architectures_and_machines()
        self.update_remote_archs(merged_arch, [lower_level, higher_level])

        if self.stored_returns:
            Debug.pwarning(f"exclusive: the block given back by a child is kept in {', '.join(self.stored_returns)}")
        Debug.psection(f"Synapse controller {lower_level.parser.filename} x {higher_level.parser.filename} "
                       f"({policy.name})")
        ProtoCCTablePrinter().ptransitiontable(list(self.get_architecture_transitions()))
        for warning in self.warnings:
            Debug.pwarning(warning)

    # ------------------------------------------------------------------ labels

    def manager_label(self, state: State_v2) -> Label:
        for labelled, label in self.manager_labels.state_labels.items():
            if str(labelled) == str(state) and labelled in self.manager_labels.directory.stable_states:
                return label
        raise KeyError(f"no label for manager state {state}")

    def client_label(self, state: State_v2) -> Label:
        return self.client_labels.state_labels[state]

    def request_label(self, guard) -> Optional[Label]:
        return self.manager_labels.label(guard)

    def keeps_data(self, manager_state: State_v2) -> bool:
        """Data( ... ) of the policy: whether the controller holds the block's data while the
        manager is in `manager_state` (always, for an inclusive policy)."""
        if not self.policy.exclusive or manager_state not in self.manager.stable_states:
            return True
        return self.policy.keeps_data(self.manager_label(manager_state))

    def keeps_data_in(self, compound_state) -> bool:
        """keeps_data() of the manager part of a compound state (the back end's placement)."""
        if isinstance(compound_state, CompoundState):
            manager_state, _ = self.sort_states_by_architecture(compound_state.base_states)
            return self.keeps_data(manager_state)
        return True

    def _keep_returned_data(self):
        """Exclusive policy: a child that leaves with the data in its message (e.g. a clean PutS of
        the last sharer) hands the block back; the manager transaction that ends where the
        controller keeps the data stores it, as a write-back does (Alg. 1, line 4: the block is
        allocated, here with the child's data)."""
        if not self.policy.exclusive:
            return
        templates = [op for t in self.manager.get_architecture_transitions() for op in t.operations
                     if self._data_assignment_source(op) is not None]
        if not templates:
            return
        transitions = {id(t): t for t in self.manager.get_architecture_transitions()}
        for trees in self.manager.state_sub_tree_dict.values():
            for tree in trees:
                for _, _, d in tree.edges(data=True):
                    transitions.setdefault(id(d['transition']), d['transition'])
        for transition in transitions.values():
            guard = transition.guard
            if not isinstance(guard, (BaseMessage, Message)) or not self._carries_data(guard):
                continue
            start, final = transition.start_state, transition.final_state
            if start not in self.manager.stable_states or final not in self.manager.stable_states:
                continue
            if self.keeps_data(start) or not self.keeps_data(final):
                continue
            if any(self._data_assignment_source(op) == str(guard) for op in transition.operations):
                continue
            template = templates[0]
            store = AuxStateHandler.cond_rename_operation(template, self._data_assignment_source(template),
                                                          str(guard))
            transition.operations.append(store)
            self.stored_returns.append(f"{start}+{guard}")

    def _carries_data(self, guard) -> bool:
        base = guard.base_msg if isinstance(guard, Message) else guard
        return base.has_data()

    @staticmethod
    def _data_assignment_source(op) -> Optional[str]:
        """X for an operation `<data> = X.<data>` (a block written from a message), else None."""
        if str(op) != "ASSIGN_":
            return None
        tokens = toStringList(op)
        if len(tokens) == 6 and tokens[2] == "=" and tokens[4] == "." and tokens[1] == tokens[5]:
            return tokens[3]
        return None

    @staticmethod
    def _sends_data(tree: MultiDiGraph) -> bool:
        return any(msg.has_data() for _, _, d in tree.edges(data=True) for msg in d['transition'].out_msg)

    # -------------------------------------------------------------- synthesis

    def gen_synapse_transitions(self, compound_states: List[CompoundState]) -> List[Transition_v2]:
        """Runs Alg. 1 on the compound states reachable from the initial state, so that a policy is
        only required to cover the combinations the protocols can actually produce."""
        by_bases = {tuple(state.base_states): state for state in compound_states}
        init = self.gen_initial_state((self.manager, self.client))
        worklist = [by_bases[tuple(init.base_states)]]
        visited = set()
        transitions: List[Transition_v2] = []
        while worklist:
            compound_state = worklist.pop(0)
            if compound_state in visited:
                continue
            visited.add(compound_state)
            manager_state, client_state = self.sort_states_by_architecture(compound_state.base_states)
            new = self.gen_child_request_transitions(manager_state, client_state) \
                + self.gen_parent_request_transitions(manager_state, client_state)
            transitions += new
            for transition in new:
                final = by_bases.get(tuple(transition.final_state.base_states)) \
                    if isinstance(transition.final_state, CompoundState) else None
                if final is not None and final not in visited:
                    worklist.append(final)

        self._check_race_redirects(transitions)
        fsm_graph = self.gen_graph(transitions)
        self.prune_non_reachable_states_graph(fsm_graph)
        return self.get_transitions_from_graph(fsm_graph)

    def _trees(self, arch: FlatArchitecture, state: State_v2):
        """(guard, tree) for every transaction tree of `arch` starting in the stable `state`."""
        for tree in arch.state_sub_tree_dict.get(state, []):
            roots = self.get_transitions_by_start_state(tree, state)
            if roots:
                yield roots[0].guard, tree

    def _in_compound(self, tree: MultiDiGraph, fixed_state: State_v2, guard) -> List[Transition_v2]:
        """A transaction of one component while the other one stays in `fixed_state`. Transient
        states are prefixed with the guard, as the nested transactions are (CompoundGraphsNetworkx)."""
        graph = CompoundStateGenNetworkx(str(guard)).gen_compound_states_graph(tree, [fixed_state])
        return self.det_sort_state_graph(graph)

    # Request from a child client (Alg. 1, lines 2-9)
    def gen_child_request_transitions(self, manager_state: State_v2, client_state: State_v2) -> List[Transition_v2]:
        transitions = []
        client_label = self.client_label(client_state)
        for guard, manager_tree in self._trees(self.manager, manager_state):
            if isinstance(guard, (Access, Evict)):
                continue  # virtual requests of the proxy cache, used for parent requests
            if isinstance(guard, Event):
                transitions += self._in_compound(manager_tree, client_state, guard)
                continue
            request = self.request_label(guard)
            if request is None:
                self.warnings.append(f"no label for request {guard}, served locally")
                transitions += self._in_compound(manager_tree, client_state, guard)
                continue

            if not self.keeps_data(manager_state) and self._sends_data(manager_tree):
                raise SynthesisError(
                    f"the policy keeps no data in this controller while its children are in "
                    f"{manager_state}, but the manager's protocol answers {guard} with the block there: "
                    f"the policy needs a protocol in which the children supply the block (a forwarder)")
            rule = self.policy.match_rule(client_label, request)
            if rule is None:
                raise SynthesisError(f"no policy rule for client {client_state} {client_label} "
                                     f"+ {guard} {request} (manager {manager_state})")
            candidates = self._manager_candidates(manager_state, guard, manager_tree, request)

            # The client already holds what the policy asks: the manager serves the request with
            # the first equivalent transaction that grants the children no more than the client
            # holds (Fig. 4a: with the client in S, I+GetS is answered with S, not E).
            if rule.final.matches(client_label):
                choice = self._choose(candidates, client_state)
                if choice is not None and rule.final.matches(self.client_label(choice[2])):
                    chosen, silent, _ = choice
                    if not silent:
                        if client_label.data == Data.NP:
                            chosen = self._assume_initial_variables(chosen)
                        transitions += self._in_compound(chosen, client_state, guard)
                    else:
                        transitions += self.det_sort_state_graph(
                            self.nest_graphs(self._client_graph(client_state, [silent]), chosen))
                    continue

            plan = self.client_process(client_state, guard, request, rule.final, candidates)
            if plan is None:
                raise SynthesisError(
                    f"incompatible policy: {rule} requires the client to go from {client_state} "
                    f"{client_label} to {rule.final} on {guard} {request}, but no client transaction "
                    f"has only outcomes that match it and that the manager can serve")
            self.fetching_requests.add((str(CompoundState((manager_state, client_state))), str(guard)))
            for client_graph, chosen in plan:
                nested = self.nest_graphs(client_graph, chosen)
                self._nest_races(nested, manager_state, client_state)
                transitions += self.det_sort_state_graph(nested)
        return transitions

    def _nest_races(self, nested: MultiDiGraph, manager_state: State_v2, client_state: State_v2):
        """A forward of the parent that reaches the client in the middle of its transaction (race
        path) must downgrade the children like any request from the parent (Alg. 1, line 13): the
        race transition is replaced by the manager's virtual request nested with it (as HeteroGen
        does; HieraGen's concurrency step). The client's transaction then continues in the compound
        state of the downgraded manager (e.g. S -> I after recalling the children), i.e. in the plan
        of that manager state for the same request: a second forward in the same transaction must
        not be served as if the children still held the block.
        Exclusive policy: a race in which the client answers the parent with data the controller
        does not hold (e.g. Fwd_GetS while the client upgrades S -> M, the children hold the block)
        takes the data from the children first, as in a stable state (gen_parent_request_transitions)."""
        children = self.manager_label(manager_state)
        for transition in list(self.get_transitions_from_graph(nested)):
            guard = transition.guard
            if transition.start_state.stable or not isinstance(guard, (BaseMessage, Message)) or \
                    FORWARD not in self.client_labels.msg_roles.get(str(guard), set()):
                continue
            target = self._downgrade_target(guard, client_state, self.client_labels.label(guard).op)
            needs_data = self._children_data_needed(manager_state, children) and \
                any(msg.has_data() for msg in transition.out_msg)
            if children.op <= target and not (target == Op.NONE and children.data != Data.NP) \
                    and not needs_data:
                continue
            proxy_access = BaseAccess.k_store if target == Op.NONE else BaseAccess.k_load
            proxy_graph = self.manager_process(manager_state, proxy_access)
            if proxy_graph is None:
                raise SynthesisError(f"manager {manager_state} cannot downgrade its children for the "
                                     f"race {guard} in {transition.start_state}")
            # the race transition at the client level (the nested graph holds compound states)
            component = transition.deepcopy_trans()
            client_start = self._client_part(transition.start_state)
            client_final = self._client_part(transition.final_state)
            component.start_state, component.final_state = client_start, client_final
            race = self.gen_graph([component])
            self.set_root_node_attribute(race, client_start)
            self.set_terminal_nodes_attribute(race, [client_final])
            sub_graph = self.nest_graphs(proxy_graph, race)
            root = self.get_root_node_by_attribute(sub_graph)
            terminals = self.get_terminal_nodes_by_attribute(sub_graph)
            owned = self._own_race_states(transition.start_state)
            spliced = []
            for sub_transition in self.get_transitions_from_graph(sub_graph):
                if sub_transition.start_state == root:
                    sub_transition.start_state = transition.start_state
                else:
                    sub_transition.start_state = owned(sub_transition.start_state)
                if sub_transition.final_state not in terminals:
                    sub_transition.final_state = owned(sub_transition.final_state)
                if sub_transition.final_state in terminals:
                    downgraded = self._manager_part(sub_transition.final_state)
                    sub_transition.final_state = self._with_manager_state(transition.final_state, downgraded)
                    self._race_redirects.append((sub_transition, transition.final_state))
                spliced.append(sub_transition)
            for u, v, k, d in list(nested.edges(data=True, keys=True)):
                if d['transition'] is transition:
                    nested.remove_edge(u, v, key=k)
            self.add_transition_to_graph(nested, spliced)

    def _own_race_states(self, start_state):
        """The states nested for a race are named after the race and the client's transaction only
        (e.g. InvL2dM_x_pI_store_GetM_Ack_AD__C__S_store). Two requests of the children whose client
        transactions coincide (MESI-RC PutNT and GetM, both a client store from S__C__S) would share
        them although they continue differently: the second one gets them prefixed with its request."""
        prefix = getattr(start_state, "prefix", "") or ""
        renamed: Dict[State_v2, State_v2] = {}

        def owned(state):
            if not isinstance(state, CompoundState):
                return state
            if state not in renamed:
                owner = self._race_state_owners.setdefault(str(state), prefix)
                renamed[state] = state if owner == prefix else \
                    CompoundState(state.base_states, prefix + (state.prefix or ""))
            return renamed[state]
        return owned

    _COND_CONTAINS = re.compile(r"^SETFUNC_\w+\.contains\(.*\)$")
    _COND_COUNT = re.compile(r"^SETFUNC_\w+\.count\(\)(==|!=|>|<=)0$")
    _COND_COMPARE = re.compile(r"^(\w+)(==|!=)(.+)$")

    def _assume_initial_variables(self, manager_tree: MultiDiGraph) -> MultiDiGraph:
        """Specializes a manager transaction for a compound state in which the client holds no data.
        With inclusion the children hold nothing either, and the manager variables have their initial
        values (they live in the cache entry, which does not exist): sets are empty and identifiers
        undefined. Branches whose condition is then false are dropped, true conditions and no-op set
        updates are removed. A late PutS/PutE/PutM is then answered without allocating an entry."""
        variables = self.manager.machine.variables
        sets = {name for name, tree in variables.items() if "SET_" in str(tree.toStringTree())}
        ids = {name for name, tree in variables.items() if str(tree) == "ID_" and name not in sets}

        def evaluate(op) -> Optional[bool]:
            text = "".join(toStringList(op)[1:]) if str(op) in ("COND_", "NCOND_") else None
            if text is None:
                return None
            value = None
            if self._COND_CONTAINS.match(text):
                value = False
            elif (m := self._COND_COUNT.match(text)):
                value = {"==": True, "!=": False, ">": False, "<=": True}[m.group(1)]
            elif (m := self._COND_COMPARE.match(text)) and m.group(1) in ids:
                value = m.group(2) == "!="  # an undefined identifier equals nothing
            if value is None:
                return None
            return value if str(op) == "COND_" else not value

        tree = self.copy_graph(manager_tree)
        root = self.get_root_node_by_attribute(tree)
        for transition in list(self.get_transitions_from_graph(tree)):
            values = [evaluate(op) for op in transition.operations[1:]]
            if any(v is False for v in values):
                for u, v, k, d in list(tree.edges(data=True, keys=True)):
                    if d['transition'] is transition:
                        tree.remove_edge(u, v, key=k)
                continue
            kept = [transition.operations[0]]
            for op, value in zip(transition.operations[1:], values):
                if value is True:
                    continue
                text = "".join(toStringList(op))
                if str(op) == "SETFUNC_" and any(text.startswith(f"SETFUNC_{name}.") for name in sets) \
                        and (".del(" in text or ".clear(" in text):
                    continue
                kept.append(op)
            transition.operations = kept
        # drop what is no longer reachable from the root
        reachable = {root} | set(nx.descendants(tree, root)) if root in tree else set()
        tree.remove_nodes_from([n for n in list(tree.nodes) if n not in reachable])
        return tree

    def _manager_candidates(self, manager_state: State_v2, guard, manager_tree: MultiDiGraph,
                            request: Label) -> List[Tuple[MultiDiGraph, Optional[Label]]]:
        """manager.process() candidates: the manager's transaction for the request first, then the
        transactions of the semantically equivalent requests (same label), renamed to the request.
        Each comes with what it newly grants to the children."""
        candidates = [(manager_tree, self._children_grant(manager_tree, manager_state))]
        # An equivalent request is one transaction, possibly stored as several trees (one per branch
        # of its Process, e.g. MESIF I+GetSIfetch: `if forwarder != src`): its branches are merged,
        # otherwise only the first branch would be chosen and the others lost.
        slots: List[List[MultiDiGraph]] = []   # in the order of the trees; equivalent requests grouped
        groups: Dict[str, List[MultiDiGraph]] = {}
        for other_guard, other_tree in self._trees(self.manager, manager_state):
            if other_tree is manager_tree or not isinstance(other_guard, (BaseMessage, Message)):
                continue
            if self.request_label(other_guard) != request:
                continue
            renamed = self._rename_request(other_tree, other_guard, guard)
            if str(other_guard) == str(guard):
                slots.append([renamed])
            elif str(other_guard) in groups:
                groups[str(other_guard)].append(renamed)
            else:
                groups[str(other_guard)] = [renamed]
                slots.append(groups[str(other_guard)])
        for trees in slots:
            merged = trees[0] if len(trees) == 1 else MergeGraphsNetworkx().merge_identical_start_state_graphs(trees)
            candidates.append((merged, self._children_grant(merged, manager_state)))
        return candidates

    def _rename_request(self, tree: MultiDiGraph, old_guard, new_guard) -> MultiDiGraph:
        tree = self.copy_graph(tree)
        for transition in self.get_transitions_from_graph(tree):
            if transition.guard == old_guard:
                transition.guard = new_guard
            transition.rename_operation(str(old_guard), str(new_guard))
        return tree

    def _children_grant(self, manager_tree: MultiDiGraph, manager_state: State_v2) -> Optional[Label]:
        """What the manager transaction newly grants to the children: the join of the labels of its
        final states that exceed the current one (None if it only keeps or revokes)."""
        before = self.manager_label(manager_state)
        grant = None
        for trace in self.get_trans_traces(manager_tree, manager_state, self.manager.stable_states):
            final_state = trace[-1].final_state
            if final_state in self.manager.stable_states:
                after = self.manager_label(final_state)
                if not (after.op <= before.op and after.data.rank <= before.data.rank):
                    grant = after if grant is None else grant.join(after)
        return grant

    @staticmethod
    def _covers(client: Label, grant: Optional[Label]) -> bool:
        """Inclusion: the children may hold no more than the client, in permissions and in data
        (a child that can silently dirty the block, e.g. MESI E, needs a client that can hold it
        dirty, otherwise the data recalled from it would be dropped by a clean eviction)."""
        return grant is None or (grant.op <= client.op and grant.data.rank <= client.data.rank)

    def _silent_moves(self, client_state: State_v2) -> List[Transition_v2]:
        """Client transitions that change state without any message (e.g. MESI E --store--> M)."""
        moves = []
        for tree_guard, tree in self._trees(self.client, client_state):
            if not isinstance(tree_guard, Access):
                continue
            for trace in self.get_trans_traces(tree, client_state, self.client.stable_states):
                if len(trace) == 1 and not trace[0].out_msg and trace[0].final_state != client_state \
                        and trace[0].final_state in self.client.stable_states:
                    moves.append(trace[0])
        return moves

    def _choose(self, candidates, client_state: State_v2):
        """First manager candidate the client covers, in its state or after a silent move.
        Returns (manager transaction, silent move or None, final client state)."""
        for tree, grant in candidates:
            if self._covers(self.client_label(client_state), grant):
                return tree, None, client_state
            for move in self._silent_moves(client_state):
                if self._covers(self.client_label(move.final_state), grant):
                    return tree, move, move.final_state
        return None

    def _client_graph(self, client_state: State_v2, transitions: List[Transition_v2]) -> MultiDiGraph:
        graph = self.gen_graph(transitions)
        self.set_root_node_attribute(graph, client_state)
        self.set_terminal_nodes_attribute(graph, [transitions[-1].final_state])
        return graph

    def client_process(self, client_state: State_v2, guard, request: Label, final: LabelPattern,
                       candidates: List[Tuple[MultiDiGraph, Op]]) \
            -> Optional[List[Tuple[MultiDiGraph, MultiDiGraph]]]:
        """client.process(): the client transaction repeating the request's access. The parent
        decides its outcome, so every outcome (race paths aside) must match the policy and have a
        compatible manager transaction; otherwise the next, stronger access is tried (a store).
        Returns one (client graph, manager transaction) per outcome."""
        for access in self._equivalent_accesses(guard, request):
            outcomes: Dict[State_v2, List[List[Transition_v2]]] = {}
            racing: Dict[State_v2, List[List[Transition_v2]]] = {}
            for tree_guard, tree in self._trees(self.client, client_state):
                if not isinstance(tree_guard, Access) or str(tree_guard) != access:
                    continue
                for trace in self.get_trans_traces(tree, client_state, self.client.stable_states):
                    final_state = trace[-1].final_state
                    if final_state not in self.client.stable_states:
                        continue
                    target = racing if self._is_racing(trace) else outcomes
                    target.setdefault(final_state, []).append(trace)
            if not outcomes:
                continue
            for trace in self._race_traces([t for traces in outcomes.values() for trace in traces for t in trace]):
                racing.setdefault(trace[-1].final_state, []).append(trace)
            # Race paths (a forward of the parent overtaking the client's own transaction) are kept
            # when they end where the normal paths do; the downgrade of the children is nested into
            # them (_nest_races). Others are left to the back end, which stalls the forward.
            for final_state, traces in racing.items():
                if final_state in outcomes:
                    outcomes[final_state] += traces
                else:
                    self.warnings.append(f"race paths of {access} from {client_state} ending in "
                                         f"{final_state} are stalled")
            plan = []
            for final_state in sorted(outcomes, key=str):
                choice = self._choose(candidates, final_state)
                if choice is None or not final.matches(self.client_label(choice[2])):
                    plan = None
                    break
                chosen, silent, end_state = choice
                transitions = []
                for trace in outcomes[final_state]:
                    if silent is None:
                        transitions += trace
                    else:
                        # the silent move is folded into the transition that completes the access
                        transitions += trace[:-1] + [ChainTransitions.chain_transitions(trace[-1], silent)]
                graph = self.gen_graph(transitions)
                self.set_root_node_attribute(graph, client_state)
                self.set_terminal_nodes_attribute(graph, [end_state])
                plan.append((graph, chosen))
            if plan:
                return plan
        return None

    def _check_race_redirects(self, transitions: List[Transition_v2]):
        """A race continued in the compound state of the downgraded manager (_nest_races) needs a
        plan that goes on from there. Where there is none, it ends in the compound state of the
        original manager state instead, as before the downgrade."""
        starts = {transition.start_state for transition in transitions}
        for sub_transition, original in self._race_redirects:
            final = sub_transition.final_state
            if final.stable or final in starts:
                continue
            fallback = self.gen_new_sort_compound_state(original)
            self.warnings.append(f"race {sub_transition.guard} in {sub_transition.start_state}: nothing "
                                 f"continues from {final}, the transaction goes on in {fallback}")
            sub_transition.final_state = fallback

    def _manager_part(self, state):
        if isinstance(state, CompoundState):
            for base in state.base_states:
                if self.get_arch_by_state(base) is self.manager:
                    return base
        return state

    def _with_manager_state(self, state: CompoundState, manager_state: State_v2) -> CompoundState:
        bases = tuple(manager_state if self.get_arch_by_state(base) is self.manager else base
                      for base in state.base_states)
        return CompoundState(bases, state.prefix)

    def _client_part(self, state):
        if isinstance(state, CompoundState):
            for base in state.base_states:
                if self.get_arch_by_state(base) is self.client:
                    return base
        return state

    def _race_traces(self, transitions: List[Transition_v2]) -> List[List[Transition_v2]]:
        """Race paths of a client transaction: from every transient state it goes through, the
        forwards of the parent the client serves there (ProtoGen's concurrency, kept among the
        architecture transitions rather than in the transaction trees), followed by the rest of the
        transaction up to a stable state. Each path starts at the client's stable start state."""
        arch_transitions = list(self.client.get_architecture_transitions())
        by_start: Dict[State_v2, List[Transition_v2]] = {}
        for transition in arch_transitions:
            by_start.setdefault(transition.start_state, []).append(transition)
        is_forward = lambda t: isinstance(t.guard, (BaseMessage, Message)) and \
            FORWARD in self.client_labels.msg_roles.get(str(t.guard), set())

        prefixes: Dict[State_v2, List[Transition_v2]] = {}
        root = transitions[0].start_state if transitions else None
        for transition in transitions:  # shortest prefix reaching each transient state
            if not transition.final_state.stable and transition.final_state not in prefixes:
                prefix = prefixes.get(transition.start_state, []) if transition.start_state != root else []
                prefixes[transition.final_state] = prefix + [transition]

        traces = []
        for state, prefix in prefixes.items():
            for race in by_start.get(state, []):
                if not is_forward(race):
                    continue
                # continue the transaction (no further races) until a stable state
                stack = [[race]]
                while stack:
                    path = stack.pop()
                    last = path[-1].final_state
                    if last.stable:
                        traces.append(prefix + path)
                        continue
                    for nxt in by_start.get(last, []):
                        if not is_forward(nxt) and nxt not in path and len(path) < 16:
                            stack.append(path + [nxt])
        return traces

    def _is_racing(self, trace: List[Transition_v2]) -> bool:
        """A trace in which a forwarded request of the parent reaches the client while it waits for
        its own transaction (race transitions added by ProtoGen). These are not chained with the
        manager: the forward is stalled until the client is stable again and then served by the
        parent-request handler, which first downgrades the children (HieraGen's stalling variant).
        Chaining them would complete the child's request after the client lost the block."""
        for transition in trace[1:]:
            guard = transition.guard
            if isinstance(guard, (BaseMessage, Message)) and \
                    FORWARD in self.client_labels.msg_roles.get(str(guard), set()):
                return True
        return False

    def _equivalent_accesses(self, guard, request: Label) -> List[str]:
        """Client accesses to try for a child's request, in order: the requestor's own access if the
        client protocol has it, then the access with the same Op, then a store (a write gives the
        client the most permissions, e.g. when the manager can only grant E)."""
        if Op.WR <= request.op:
            client_accesses = {str(t.guard) for t in self.client.get_architecture_transitions()
                               if isinstance(t.guard, Access)}
            candidates = [a for a in self._requestor_accesses(guard) if a in client_accesses
                          and a not in READ_ACCESSES] + [BaseAccess.k_store]
        elif Op.RD <= request.op:
            candidates = [a for a in self._requestor_accesses(guard) if a in READ_ACCESSES] + \
                [BaseAccess.k_load, BaseAccess.k_store]
        else:
            candidates = []
        return list(dict.fromkeys(candidates))

    def _requestor_accesses(self, guard) -> List[str]:
        cache = self.lower_level.cache
        found = []
        for transition in cache.get_architecture_transitions():
            if isinstance(transition.guard, Access) and any(str(m) == str(guard) for m in transition.out_msg):
                found.append(str(transition.guard))
        return found

    # Request from the parent manager, and eviction of the client (Alg. 1, lines 10-16)
    def gen_parent_request_transitions(self, manager_state: State_v2, client_state: State_v2) -> List[Transition_v2]:
        transitions = []
        children = self.manager_label(manager_state)
        for guard, client_tree in self._trees(self.client, client_state):
            if isinstance(guard, Access):
                continue  # client accesses only run on behalf of child requests
            if isinstance(guard, Evict):
                target = Op.NONE  # inclusive: evicting the block requires the children to drop it
            elif isinstance(guard, (BaseMessage, Message)):
                target = self._downgrade_target(guard, client_state,
                                                self._client_final_op(client_tree, client_state))
            else:
                transitions += self._in_compound(client_tree, manager_state, guard)
                continue

            # the client answers with data the controller does not hold up to date (exclusive policy,
            # or a dirty child such as a MOESI O owner); the children give it back first (with a
            # virtual load they may keep a shared copy)
            needs_data = self._children_data_needed(manager_state, children) and self._sends_data(client_tree)
            if children.op <= target and not (target == Op.NONE and children.data != Data.NP) \
                    and not needs_data:
                transitions += self._in_compound(client_tree, manager_state, guard)
                continue

            proxy_access = BaseAccess.k_store if target == Op.NONE else BaseAccess.k_load
            proxy_graph = self.manager_process(manager_state, proxy_access)
            if proxy_graph is None:
                raise SynthesisError(f"manager {manager_state} has no virtual {proxy_access} to "
                                     f"{'take the data from' if needs_data else 'downgrade'} its children "
                                     f"(to {target}) before the client serves {guard}")
            nested = self.nest_graphs(proxy_graph, client_tree)
            transitions += self.det_sort_state_graph(nested)
        return transitions

    def _children_data_needed(self, manager_state: State_v2, children: Label) -> bool:
        """Whether the block's up-to-date data is in the children, not here: always with an exclusive
        policy where the controller keeps no data, and whenever a child may hold it dirty (e.g. a
        MOESI owner in O, whose Fwd_GetS answer does not write back)."""
        return not self.keeps_data(manager_state) or children.data == Data.DIRTY

    def _downgrade_target(self, guard, client_state: State_v2, client_op: Op) -> Op:
        """Permissions the children may keep on a request from the parent: what the client keeps
        (Alg. 1, line 12), or less if a Downgrade rule of the policy asks for it."""
        pattern = self.policy.children_target(self.client_label(client_state),
                                              self.client_labels.label(guard))
        if pattern is None or pattern.ops is None:
            return client_op
        for op in sorted(pattern.ops, key=lambda o: len(o.perms)):
            if op <= client_op:
                return op
        return client_op

    def _client_final_op(self, client_tree: MultiDiGraph, client_state: State_v2) -> Op:
        """client.simulate(): the most permissive state the client can end in after the request."""
        op = Op.NONE
        for trace in self.get_trans_traces(client_tree, client_state, self.client.stable_states):
            final_state = trace[-1].final_state
            if final_state in self.client.stable_states:
                op = op | self.client_label(final_state).op
        return op

    def manager_process(self, manager_state: State_v2, proxy_access: str) -> Optional[MultiDiGraph]:
        """manager.process() of a virtual request of the proxy cache (HieraGen's proxy-cache-L)."""
        trees = [tree for guard, tree in self._trees(self.manager, manager_state)
                 if isinstance(guard, Access) and str(guard) == proxy_access]
        if not trees:
            return None
        if len(trees) > 1:
            return MergeGraphsNetworkx().merge_identical_start_state_graphs(trees)
        return trees[0]

    # ------------------------------------------------------------- back end

    def entry_alloc(self, transition: Transition_v2) -> Tuple[bool, bool]:
        """(allocate, refresh_mru) for the SLICC back end (Backend/SLICC/ModularSLICC/common/Util.py).
        Alg. 1, line 4: the block is allocated when the client has to fetch it for a child. A handler
        that reads or writes the manager's variables in a state without data also needs the entry,
        since they live in it."""
        _, client_state = self.sort_states_by_architecture(transition.start_state.base_states)
        if client_state not in self.client_labels.state_labels:
            return False, False
        present = self.client_label(client_state).data != Data.NP
        if present:
            return False, self._acquire_request(transition.guard)
        fetches = (str(transition.start_state), str(transition.guard)) in self.fetching_requests
        return fetches or self._uses_machine_variables(transition), False

    def _acquire_request(self, guard) -> bool:
        """A child's request for a copy of the block (not an eviction, not a response)."""
        if not isinstance(guard, (BaseMessage, Message)):
            return False
        name = str(guard.base_msg if isinstance(guard, Message) else guard)
        return REQUEST in self.manager_labels.msg_roles.get(name, set()) and \
            name not in self.manager_labels.eviction_requests

    def exclusive_placement(self) -> Optional[Tuple[List[str], List[str], Set[Tuple[str, str]]]]:
        """For the back end of an exclusive controller: the stable compound states where it keeps only
        the coherence state (a tag, the children hold the data), those where it keeps the data, and
        the (state, request) handlers that bring a block back from the tags to the data (e.g. the
        last child's PutS), before which a victim may have to be evicted. None if inclusive."""
        if not self.policy.exclusive:
            return None
        tags, data = [], []
        for state in self.stable_states:
            if str(state) == str(self.init_state):
                continue  # no entry at all (the back end deallocates it)
            (data if self.keeps_data_in(state) else tags).append(str(state))
        # only the requests of the children (e.g. the last child's PutS) make room first: a request
        # from the parent must not wait for a victim (it may be what the victim waits for); there the
        # block stays in the tags if no way is free
        promoting = set()
        for transition in self.get_architecture_transitions():
            if str(transition.start_state) in tags and str(transition.final_state) in data \
                    and isinstance(transition.guard, (BaseMessage, Message)) \
                    and self.request_label(transition.guard) is not None:
                promoting.add((str(transition.start_state), str(transition.guard)))
        return sorted(tags), sorted(data), promoting

    def _uses_machine_variables(self, transition: Transition_v2) -> bool:
        def tokens(node) -> List[str]:
            return [str(node)] + [t for child in (node.getChildren() or []) for t in tokens(child)]

        variables = set(self.machine.variables.keys())
        return any(token in variables for op in transition.operations[1:] for token in tokens(op))

    # ------------------------------------------------------- HHDirArchitecture

    def get_arch_list(self):
        return [self, self.manager, self.client]
