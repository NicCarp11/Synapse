# $ANTLR 3.5.2 Parser/ProtoCC.g 2026-10-08 08:16:13

import sys
from antlr3 import *

from antlr3.tree import *




# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
T__99=99
T__100=100
T__101=101
T__102=102
T__103=103
T__104=104
T__105=105
T__106=106
T__107=107
T__108=108
T__109=109
T__110=110
T__111=111
T__112=112
T__113=113
T__114=114
T__115=115
T__116=116
T__117=117
T__118=118
T__119=119
T__120=120
T__121=121
ACCESS=4
ACCESS_=5
ARCH=6
ARCH_=7
ARRAY=8
ARRAY_=9
ASSIGN_=10
AWAIT=11
AWAIT_=12
BCAST_=13
BOOL=14
BOOLID=15
BOOL_=16
BREAK=17
BREAK_=18
CACHE=19
CACHE_=20
CBRACE=21
CCBRACE=22
CEBRACE=23
COMMA=24
COMMENT=25
COND_=26
CONSTANT=27
CONSTANT_=28
DATA=29
DATA_=30
DDOT=31
DIR=32
DIR_=33
DOT=34
ELEMENT_=35
ELSE=36
ENDIFELSE_=37
ENDIF_=38
ENDPROC_=39
ENDWHEN_=40
EQUALSIGN=41
EVENT_=42
EVENT_ACK_=43
EVICT=44
FIFO=45
FIFO_=46
GUARD_=47
ID=48
ID_=49
IF=50
IFELSE_=51
IF_=52
INITSTATE_=53
INITVAL_=54
INT=55
INTID=56
INT_=57
LINE_COMMENT=58
MACHN_=59
MCAST_=60
MEM=61
MEM_=62
MINUS=63
MSG=64
MSGCSTR_=65
MSG_=66
MULT=67
NCOND_=68
NEG=69
NETWORK=70
NETWORK_=71
NEXT=72
NEXT_=73
NID=74
OBJSET_=75
OBRACE=76
OCBRACE=77
OEBRACE=78
PLUS=79
PROC=80
PROC_=81
RANGE_=82
SEMICOLON=83
SEND_=84
SET=85
SETFUNC_=86
SET_=87
STABLE=88
STABLE_=89
STALL=90
STALL_=91
STATE=92
TRANS_=93
UNDEF=94
UNDEF_=95
WHEN=96
WHEN_=97
WS=98

# token names
tokenNamesMap = {
    0: "<invalid>", 1: "<EOR>", 2: "<DOWN>", 3: "<UP>",
    -1: "EOF", 99: "T__99", 100: "T__100", 101: "T__101", 102: "T__102", 
    103: "T__103", 104: "T__104", 105: "T__105", 106: "T__106", 107: "T__107", 
    108: "T__108", 109: "T__109", 110: "T__110", 111: "T__111", 112: "T__112", 
    113: "T__113", 114: "T__114", 115: "T__115", 116: "T__116", 117: "T__117", 
    118: "T__118", 119: "T__119", 120: "T__120", 121: "T__121", 4: "ACCESS", 
    5: "ACCESS_", 6: "ARCH", 7: "ARCH_", 8: "ARRAY", 9: "ARRAY_", 10: "ASSIGN_", 
    11: "AWAIT", 12: "AWAIT_", 13: "BCAST_", 14: "BOOL", 15: "BOOLID", 16: "BOOL_", 
    17: "BREAK", 18: "BREAK_", 19: "CACHE", 20: "CACHE_", 21: "CBRACE", 
    22: "CCBRACE", 23: "CEBRACE", 24: "COMMA", 25: "COMMENT", 26: "COND_", 
    27: "CONSTANT", 28: "CONSTANT_", 29: "DATA", 30: "DATA_", 31: "DDOT", 
    32: "DIR", 33: "DIR_", 34: "DOT", 35: "ELEMENT_", 36: "ELSE", 37: "ENDIFELSE_", 
    38: "ENDIF_", 39: "ENDPROC_", 40: "ENDWHEN_", 41: "EQUALSIGN", 42: "EVENT_", 
    43: "EVENT_ACK_", 44: "EVICT", 45: "FIFO", 46: "FIFO_", 47: "GUARD_", 
    48: "ID", 49: "ID_", 50: "IF", 51: "IFELSE_", 52: "IF_", 53: "INITSTATE_", 
    54: "INITVAL_", 55: "INT", 56: "INTID", 57: "INT_", 58: "LINE_COMMENT", 
    59: "MACHN_", 60: "MCAST_", 61: "MEM", 62: "MEM_", 63: "MINUS", 64: "MSG", 
    65: "MSGCSTR_", 66: "MSG_", 67: "MULT", 68: "NCOND_", 69: "NEG", 70: "NETWORK", 
    71: "NETWORK_", 72: "NEXT", 73: "NEXT_", 74: "NID", 75: "OBJSET_", 76: "OBRACE", 
    77: "OCBRACE", 78: "OEBRACE", 79: "PLUS", 80: "PROC", 81: "PROC_", 82: "RANGE_", 
    83: "SEMICOLON", 84: "SEND_", 85: "SET", 86: "SETFUNC_", 87: "SET_", 
    88: "STABLE", 89: "STABLE_", 90: "STALL", 91: "STALL_", 92: "STATE", 
    93: "TRANS_", 94: "UNDEF", 95: "UNDEF_", 96: "WHEN", 97: "WHEN_", 98: "WS"
}
Token.registerTokenNamesMap(tokenNamesMap)

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "ACCESS", "ACCESS_", "ARCH", "ARCH_", "ARRAY", "ARRAY_", "ASSIGN_", 
    "AWAIT", "AWAIT_", "BCAST_", "BOOL", "BOOLID", "BOOL_", "BREAK", "BREAK_", 
    "CACHE", "CACHE_", "CBRACE", "CCBRACE", "CEBRACE", "COMMA", "COMMENT", 
    "COND_", "CONSTANT", "CONSTANT_", "DATA", "DATA_", "DDOT", "DIR", "DIR_", 
    "DOT", "ELEMENT_", "ELSE", "ENDIFELSE_", "ENDIF_", "ENDPROC_", "ENDWHEN_", 
    "EQUALSIGN", "EVENT_", "EVENT_ACK_", "EVICT", "FIFO", "FIFO_", "GUARD_", 
    "ID", "ID_", "IF", "IFELSE_", "IF_", "INITSTATE_", "INITVAL_", "INT", 
    "INTID", "INT_", "LINE_COMMENT", "MACHN_", "MCAST_", "MEM", "MEM_", 
    "MINUS", "MSG", "MSGCSTR_", "MSG_", "MULT", "NCOND_", "NEG", "NETWORK", 
    "NETWORK_", "NEXT", "NEXT_", "NID", "OBJSET_", "OBRACE", "OCBRACE", 
    "OEBRACE", "PLUS", "PROC", "PROC_", "RANGE_", "SEMICOLON", "SEND_", 
    "SET", "SETFUNC_", "SET_", "STABLE", "STABLE_", "STALL", "STALL_", "STATE", 
    "TRANS_", "UNDEF", "UNDEF_", "WHEN", "WHEN_", "WS", "'!='", "'&'", "'<'", 
    "'<='", "'=='", "'>'", "'>='", "'Bcast'", "'Event'", "'Mcast'", "'Ordered'", 
    "'Send'", "'Unordered'", "'add'", "'bcast'", "'clear'", "'contains'", 
    "'count'", "'del'", "'mcast'", "'send'", "'smallest'", "'|'"
]



class ProtoCCParser(Parser):
    grammarFileName = "Parser/ProtoCC.g"
    api_version = 1
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super().__init__(input, state, *args, **kwargs)




        self.delegates = []

        self._adaptor = None
        self.adaptor = CommonTreeAdaptor()



    def getTreeAdaptor(self):
        return self._adaptor

    def setTreeAdaptor(self, adaptor):
        self._adaptor = adaptor

    adaptor = property(getTreeAdaptor, setTreeAdaptor)


    class send_function_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "send_function"
    # Parser/ProtoCC.g:128:1: send_function : ( 'send' | 'Send' );
    def send_function(self, ):
        retval = self.send_function_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set1 = None

        set1_tree = None

        try:
            try:
                # Parser/ProtoCC.g:129:2: ( 'send' | 'Send' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set1 = self.input.LT(1)

                if self.input.LA(1) in {110, 119}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set1))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "send_function"


    class mcast_function_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "mcast_function"
    # Parser/ProtoCC.g:133:1: mcast_function : ( 'mcast' | 'Mcast' );
    def mcast_function(self, ):
        retval = self.mcast_function_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set2 = None

        set2_tree = None

        try:
            try:
                # Parser/ProtoCC.g:134:2: ( 'mcast' | 'Mcast' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set2 = self.input.LT(1)

                if self.input.LA(1) in {108, 118}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set2))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "mcast_function"


    class bcast_function_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "bcast_function"
    # Parser/ProtoCC.g:138:1: bcast_function : ( 'bcast' | 'Bcast' );
    def bcast_function(self, ):
        retval = self.bcast_function_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set3 = None

        set3_tree = None

        try:
            try:
                # Parser/ProtoCC.g:139:2: ( 'bcast' | 'Bcast' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set3 = self.input.LT(1)

                if self.input.LA(1) in {106, 113}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set3))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "bcast_function"


    class internal_event_function_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "internal_event_function"
    # Parser/ProtoCC.g:143:1: internal_event_function : 'Event' ;
    def internal_event_function(self, ):
        retval = self.internal_event_function_return()
        retval.start = self.input.LT(1)


        root_0 = None

        string_literal4 = None

        string_literal4_tree = None

        try:
            try:
                # Parser/ProtoCC.g:144:2: ( 'Event' )
                # Parser/ProtoCC.g:144:4: 'Event'
                pass 
                root_0 = self._adaptor.nil()


                string_literal4 = self.match(self.input, 107, self.FOLLOW_107_in_internal_event_function705)
                string_literal4_tree = self._adaptor.createWithPayload(string_literal4)
                self._adaptor.addChild(root_0, string_literal4_tree)





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "internal_event_function"


    class set_function_types_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "set_function_types"
    # Parser/ProtoCC.g:147:1: set_function_types : ( 'add' | 'count' | 'contains' | 'del' | 'clear' | 'smallest' );
    def set_function_types(self, ):
        retval = self.set_function_types_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set5 = None

        set5_tree = None

        try:
            try:
                # Parser/ProtoCC.g:148:2: ( 'add' | 'count' | 'contains' | 'del' | 'clear' | 'smallest' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set5 = self.input.LT(1)

                if self.input.LA(1) in {112, 114, 115, 116, 117, 120}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set5))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "set_function_types"


    class relational_operator_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "relational_operator"
    # Parser/ProtoCC.g:156:1: relational_operator : ( '==' | '!=' | '<=' | '>=' | '<' | '>' );
    def relational_operator(self, ):
        retval = self.relational_operator_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set6 = None

        set6_tree = None

        try:
            try:
                # Parser/ProtoCC.g:157:2: ( '==' | '!=' | '<=' | '>=' | '<' | '>' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set6 = self.input.LT(1)

                if (101 <= self.input.LA(1) <= 105) or self.input.LA(1) in {99}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set6))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "relational_operator"


    class combinatorial_operator_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "combinatorial_operator"
    # Parser/ProtoCC.g:165:1: combinatorial_operator : ( '&' | '|' );
    def combinatorial_operator(self, ):
        retval = self.combinatorial_operator_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set7 = None

        set7_tree = None

        try:
            try:
                # Parser/ProtoCC.g:166:5: ( '&' | '|' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set7 = self.input.LT(1)

                if self.input.LA(1) in {100, 121}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set7))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "combinatorial_operator"


    class document_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "document"
    # Parser/ProtoCC.g:196:1: document : ( const_decl | init_hw | arch_block | expressions )* ;
    def document(self, ):
        retval = self.document_return()
        retval.start = self.input.LT(1)


        root_0 = None

        const_decl8 = None
        init_hw9 = None
        arch_block10 = None
        expressions11 = None


        try:
            try:
                # Parser/ProtoCC.g:197:2: ( ( const_decl | init_hw | arch_block | expressions )* )
                # Parser/ProtoCC.g:197:4: ( const_decl | init_hw | arch_block | expressions )*
                pass 
                root_0 = self._adaptor.nil()


                # Parser/ProtoCC.g:197:4: ( const_decl | init_hw | arch_block | expressions )*
                while True: #loop1
                    alt1 = 5
                    LA1 = self.input.LA(1)
                    if LA1 in {CONSTANT}:
                        alt1 = 1
                    elif LA1 in {CACHE, DIR, MEM, MSG, NETWORK}:
                        alt1 = 2
                    elif LA1 in {ARCH}:
                        alt1 = 3
                    elif LA1 in {ACCESS, ID, IF, STALL, STATE, UNDEF, 107}:
                        alt1 = 4

                    if alt1 == 1:
                        # Parser/ProtoCC.g:197:5: const_decl
                        pass 
                        self._state.following.append(self.FOLLOW_const_decl_in_document1033)
                        const_decl8 = self.const_decl()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, const_decl8.tree)



                    elif alt1 == 2:
                        # Parser/ProtoCC.g:197:18: init_hw
                        pass 
                        self._state.following.append(self.FOLLOW_init_hw_in_document1037)
                        init_hw9 = self.init_hw()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, init_hw9.tree)



                    elif alt1 == 3:
                        # Parser/ProtoCC.g:197:28: arch_block
                        pass 
                        self._state.following.append(self.FOLLOW_arch_block_in_document1041)
                        arch_block10 = self.arch_block()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, arch_block10.tree)



                    elif alt1 == 4:
                        # Parser/ProtoCC.g:197:41: expressions
                        pass 
                        self._state.following.append(self.FOLLOW_expressions_in_document1045)
                        expressions11 = self.expressions()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, expressions11.tree)



                    else:
                        break #loop1




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "document"


    class declarations_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "declarations"
    # Parser/ProtoCC.g:201:1: declarations : ( int_decl | bool_decl | state_decl | data_decl | id_decl );
    def declarations(self, ):
        retval = self.declarations_return()
        retval.start = self.input.LT(1)


        root_0 = None

        int_decl12 = None
        bool_decl13 = None
        state_decl14 = None
        data_decl15 = None
        id_decl16 = None


        try:
            try:
                # Parser/ProtoCC.g:201:14: ( int_decl | bool_decl | state_decl | data_decl | id_decl )
                alt2 = 5
                LA2 = self.input.LA(1)
                if LA2 in {INTID}:
                    alt2 = 1
                elif LA2 in {BOOLID}:
                    alt2 = 2
                elif LA2 in {STATE}:
                    alt2 = 3
                elif LA2 in {DATA}:
                    alt2 = 4
                elif LA2 in {NID, SET}:
                    alt2 = 5
                else:
                    nvae = NoViableAltException("", 2, 0, self.input)

                    raise nvae


                if alt2 == 1:
                    # Parser/ProtoCC.g:201:16: int_decl
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_int_decl_in_declarations1058)
                    int_decl12 = self.int_decl()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, int_decl12.tree)



                elif alt2 == 2:
                    # Parser/ProtoCC.g:201:27: bool_decl
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_bool_decl_in_declarations1062)
                    bool_decl13 = self.bool_decl()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, bool_decl13.tree)



                elif alt2 == 3:
                    # Parser/ProtoCC.g:201:39: state_decl
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_state_decl_in_declarations1066)
                    state_decl14 = self.state_decl()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, state_decl14.tree)



                elif alt2 == 4:
                    # Parser/ProtoCC.g:201:52: data_decl
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_data_decl_in_declarations1070)
                    data_decl15 = self.data_decl()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, data_decl15.tree)



                elif alt2 == 5:
                    # Parser/ProtoCC.g:201:64: id_decl
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_id_decl_in_declarations1074)
                    id_decl16 = self.id_decl()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, id_decl16.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "declarations"


    class const_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "const_decl"
    # Parser/ProtoCC.g:203:5: const_decl : CONSTANT ID INT -> ^( CONSTANT_ ID INT ) ;
    def const_decl(self, ):
        retval = self.const_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        CONSTANT17 = None
        ID18 = None
        INT19 = None

        CONSTANT17_tree = None
        ID18_tree = None
        INT19_tree = None
        stream_CONSTANT = RewriteRuleTokenStream(self._adaptor, "token CONSTANT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_INT = RewriteRuleTokenStream(self._adaptor, "token INT")

        try:
            try:
                # Parser/ProtoCC.g:203:16: ( CONSTANT ID INT -> ^( CONSTANT_ ID INT ) )
                # Parser/ProtoCC.g:203:18: CONSTANT ID INT
                pass 
                CONSTANT17 = self.match(self.input, CONSTANT, self.FOLLOW_CONSTANT_in_const_decl1086) 
                stream_CONSTANT.add(CONSTANT17)


                ID18 = self.match(self.input, ID, self.FOLLOW_ID_in_const_decl1088) 
                stream_ID.add(ID18)


                INT19 = self.match(self.input, INT, self.FOLLOW_INT_in_const_decl1090) 
                stream_INT.add(INT19)


                # AST Rewrite
                # elements: ID, INT
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 203:34: -> ^( CONSTANT_ ID INT )
                # Parser/ProtoCC.g:203:37: ^( CONSTANT_ ID INT )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(CONSTANT_, "CONSTANT_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_INT.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "const_decl"


    class int_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "int_decl"
    # Parser/ProtoCC.g:205:5: int_decl : INTID range ID ( EQUALSIGN INT )* SEMICOLON -> ^( INT_ ID range ( ^( INITVAL_ INT ) )* ) ;
    def int_decl(self, ):
        retval = self.int_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        INTID20 = None
        ID22 = None
        EQUALSIGN23 = None
        INT24 = None
        SEMICOLON25 = None
        range21 = None

        INTID20_tree = None
        ID22_tree = None
        EQUALSIGN23_tree = None
        INT24_tree = None
        SEMICOLON25_tree = None
        stream_EQUALSIGN = RewriteRuleTokenStream(self._adaptor, "token EQUALSIGN")
        stream_INTID = RewriteRuleTokenStream(self._adaptor, "token INTID")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_INT = RewriteRuleTokenStream(self._adaptor, "token INT")
        stream_range = RewriteRuleSubtreeStream(self._adaptor, "rule range")
        try:
            try:
                # Parser/ProtoCC.g:205:14: ( INTID range ID ( EQUALSIGN INT )* SEMICOLON -> ^( INT_ ID range ( ^( INITVAL_ INT ) )* ) )
                # Parser/ProtoCC.g:205:16: INTID range ID ( EQUALSIGN INT )* SEMICOLON
                pass 
                INTID20 = self.match(self.input, INTID, self.FOLLOW_INTID_in_int_decl1112) 
                stream_INTID.add(INTID20)


                self._state.following.append(self.FOLLOW_range_in_int_decl1114)
                range21 = self.range()

                self._state.following.pop()
                stream_range.add(range21.tree)


                ID22 = self.match(self.input, ID, self.FOLLOW_ID_in_int_decl1116) 
                stream_ID.add(ID22)


                # Parser/ProtoCC.g:205:31: ( EQUALSIGN INT )*
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == EQUALSIGN) :
                        alt3 = 1


                    if alt3 == 1:
                        # Parser/ProtoCC.g:205:32: EQUALSIGN INT
                        pass 
                        EQUALSIGN23 = self.match(self.input, EQUALSIGN, self.FOLLOW_EQUALSIGN_in_int_decl1119) 
                        stream_EQUALSIGN.add(EQUALSIGN23)


                        INT24 = self.match(self.input, INT, self.FOLLOW_INT_in_int_decl1121) 
                        stream_INT.add(INT24)



                    else:
                        break #loop3


                SEMICOLON25 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_int_decl1125) 
                stream_SEMICOLON.add(SEMICOLON25)


                # AST Rewrite
                # elements: ID, range, INT
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 205:58: -> ^( INT_ ID range ( ^( INITVAL_ INT ) )* )
                # Parser/ProtoCC.g:205:61: ^( INT_ ID range ( ^( INITVAL_ INT ) )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(INT_, "INT_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, stream_range.nextTree())

                # Parser/ProtoCC.g:205:77: ( ^( INITVAL_ INT ) )*
                while stream_INT.hasNext():
                    # Parser/ProtoCC.g:205:77: ^( INITVAL_ INT )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(INITVAL_, "INITVAL_")
                    , root_2)

                    self._adaptor.addChild(root_2, 
                    stream_INT.nextNode()
                    )

                    self._adaptor.addChild(root_1, root_2)


                stream_INT.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "int_decl"


    class bool_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "bool_decl"
    # Parser/ProtoCC.g:206:5: bool_decl : BOOLID ID ( EQUALSIGN BOOL )* SEMICOLON -> ^( BOOL_ ID ( ^( INITVAL_ BOOL ) )* ) ;
    def bool_decl(self, ):
        retval = self.bool_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        BOOLID26 = None
        ID27 = None
        EQUALSIGN28 = None
        BOOL29 = None
        SEMICOLON30 = None

        BOOLID26_tree = None
        ID27_tree = None
        EQUALSIGN28_tree = None
        BOOL29_tree = None
        SEMICOLON30_tree = None
        stream_EQUALSIGN = RewriteRuleTokenStream(self._adaptor, "token EQUALSIGN")
        stream_BOOL = RewriteRuleTokenStream(self._adaptor, "token BOOL")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_BOOLID = RewriteRuleTokenStream(self._adaptor, "token BOOLID")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")

        try:
            try:
                # Parser/ProtoCC.g:206:15: ( BOOLID ID ( EQUALSIGN BOOL )* SEMICOLON -> ^( BOOL_ ID ( ^( INITVAL_ BOOL ) )* ) )
                # Parser/ProtoCC.g:206:17: BOOLID ID ( EQUALSIGN BOOL )* SEMICOLON
                pass 
                BOOLID26 = self.match(self.input, BOOLID, self.FOLLOW_BOOLID_in_bool_decl1153) 
                stream_BOOLID.add(BOOLID26)


                ID27 = self.match(self.input, ID, self.FOLLOW_ID_in_bool_decl1155) 
                stream_ID.add(ID27)


                # Parser/ProtoCC.g:206:27: ( EQUALSIGN BOOL )*
                while True: #loop4
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == EQUALSIGN) :
                        alt4 = 1


                    if alt4 == 1:
                        # Parser/ProtoCC.g:206:28: EQUALSIGN BOOL
                        pass 
                        EQUALSIGN28 = self.match(self.input, EQUALSIGN, self.FOLLOW_EQUALSIGN_in_bool_decl1158) 
                        stream_EQUALSIGN.add(EQUALSIGN28)


                        BOOL29 = self.match(self.input, BOOL, self.FOLLOW_BOOL_in_bool_decl1160) 
                        stream_BOOL.add(BOOL29)



                    else:
                        break #loop4


                SEMICOLON30 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_bool_decl1164) 
                stream_SEMICOLON.add(SEMICOLON30)


                # AST Rewrite
                # elements: ID, BOOL
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 206:55: -> ^( BOOL_ ID ( ^( INITVAL_ BOOL ) )* )
                # Parser/ProtoCC.g:206:58: ^( BOOL_ ID ( ^( INITVAL_ BOOL ) )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(BOOL_, "BOOL_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:206:69: ( ^( INITVAL_ BOOL ) )*
                while stream_BOOL.hasNext():
                    # Parser/ProtoCC.g:206:69: ^( INITVAL_ BOOL )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(INITVAL_, "INITVAL_")
                    , root_2)

                    self._adaptor.addChild(root_2, 
                    stream_BOOL.nextNode()
                    )

                    self._adaptor.addChild(root_1, root_2)


                stream_BOOL.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "bool_decl"


    class state_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "state_decl"
    # Parser/ProtoCC.g:208:5: state_decl : STATE ID SEMICOLON -> ^( INITSTATE_ ID ) ;
    def state_decl(self, ):
        retval = self.state_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        STATE31 = None
        ID32 = None
        SEMICOLON33 = None

        STATE31_tree = None
        ID32_tree = None
        SEMICOLON33_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_STATE = RewriteRuleTokenStream(self._adaptor, "token STATE")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")

        try:
            try:
                # Parser/ProtoCC.g:208:16: ( STATE ID SEMICOLON -> ^( INITSTATE_ ID ) )
                # Parser/ProtoCC.g:208:18: STATE ID SEMICOLON
                pass 
                STATE31 = self.match(self.input, STATE, self.FOLLOW_STATE_in_state_decl1191) 
                stream_STATE.add(STATE31)


                ID32 = self.match(self.input, ID, self.FOLLOW_ID_in_state_decl1193) 
                stream_ID.add(ID32)


                SEMICOLON33 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_state_decl1195) 
                stream_SEMICOLON.add(SEMICOLON33)


                # AST Rewrite
                # elements: ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 208:37: -> ^( INITSTATE_ ID )
                # Parser/ProtoCC.g:208:40: ^( INITSTATE_ ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(INITSTATE_, "INITSTATE_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "state_decl"


    class data_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "data_decl"
    # Parser/ProtoCC.g:209:5: data_decl : DATA ID SEMICOLON -> ^( DATA_ ID ) ;
    def data_decl(self, ):
        retval = self.data_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        DATA34 = None
        ID35 = None
        SEMICOLON36 = None

        DATA34_tree = None
        ID35_tree = None
        SEMICOLON36_tree = None
        stream_DATA = RewriteRuleTokenStream(self._adaptor, "token DATA")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")

        try:
            try:
                # Parser/ProtoCC.g:209:15: ( DATA ID SEMICOLON -> ^( DATA_ ID ) )
                # Parser/ProtoCC.g:209:17: DATA ID SEMICOLON
                pass 
                DATA34 = self.match(self.input, DATA, self.FOLLOW_DATA_in_data_decl1214) 
                stream_DATA.add(DATA34)


                ID35 = self.match(self.input, ID, self.FOLLOW_ID_in_data_decl1216) 
                stream_ID.add(ID35)


                SEMICOLON36 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_data_decl1218) 
                stream_SEMICOLON.add(SEMICOLON36)


                # AST Rewrite
                # elements: ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 209:35: -> ^( DATA_ ID )
                # Parser/ProtoCC.g:209:38: ^( DATA_ ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(DATA_, "DATA_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "data_decl"


    class id_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "id_decl"
    # Parser/ProtoCC.g:210:5: id_decl : ( set_decl )* NID ID ( EQUALSIGN ( set_decl )* ID )* SEMICOLON -> ^( ID_ ID ( set_decl )* ( ^( INITVAL_ ( set_decl )* ID ) )* ) ;
    def id_decl(self, ):
        retval = self.id_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        NID38 = None
        ID39 = None
        EQUALSIGN40 = None
        ID42 = None
        SEMICOLON43 = None
        set_decl37 = None
        set_decl41 = None

        NID38_tree = None
        ID39_tree = None
        EQUALSIGN40_tree = None
        ID42_tree = None
        SEMICOLON43_tree = None
        stream_EQUALSIGN = RewriteRuleTokenStream(self._adaptor, "token EQUALSIGN")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_NID = RewriteRuleTokenStream(self._adaptor, "token NID")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_set_decl = RewriteRuleSubtreeStream(self._adaptor, "rule set_decl")
        try:
            try:
                # Parser/ProtoCC.g:210:13: ( ( set_decl )* NID ID ( EQUALSIGN ( set_decl )* ID )* SEMICOLON -> ^( ID_ ID ( set_decl )* ( ^( INITVAL_ ( set_decl )* ID ) )* ) )
                # Parser/ProtoCC.g:210:15: ( set_decl )* NID ID ( EQUALSIGN ( set_decl )* ID )* SEMICOLON
                pass 
                # Parser/ProtoCC.g:210:15: ( set_decl )*
                while True: #loop5
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == SET) :
                        alt5 = 1


                    if alt5 == 1:
                        # Parser/ProtoCC.g:210:15: set_decl
                        pass 
                        self._state.following.append(self.FOLLOW_set_decl_in_id_decl1237)
                        set_decl37 = self.set_decl()

                        self._state.following.pop()
                        stream_set_decl.add(set_decl37.tree)



                    else:
                        break #loop5


                NID38 = self.match(self.input, NID, self.FOLLOW_NID_in_id_decl1240) 
                stream_NID.add(NID38)


                ID39 = self.match(self.input, ID, self.FOLLOW_ID_in_id_decl1242) 
                stream_ID.add(ID39)


                # Parser/ProtoCC.g:210:32: ( EQUALSIGN ( set_decl )* ID )*
                while True: #loop7
                    alt7 = 2
                    LA7_0 = self.input.LA(1)

                    if (LA7_0 == EQUALSIGN) :
                        alt7 = 1


                    if alt7 == 1:
                        # Parser/ProtoCC.g:210:33: EQUALSIGN ( set_decl )* ID
                        pass 
                        EQUALSIGN40 = self.match(self.input, EQUALSIGN, self.FOLLOW_EQUALSIGN_in_id_decl1245) 
                        stream_EQUALSIGN.add(EQUALSIGN40)


                        # Parser/ProtoCC.g:210:43: ( set_decl )*
                        while True: #loop6
                            alt6 = 2
                            LA6_0 = self.input.LA(1)

                            if (LA6_0 == SET) :
                                alt6 = 1


                            if alt6 == 1:
                                # Parser/ProtoCC.g:210:43: set_decl
                                pass 
                                self._state.following.append(self.FOLLOW_set_decl_in_id_decl1247)
                                set_decl41 = self.set_decl()

                                self._state.following.pop()
                                stream_set_decl.add(set_decl41.tree)



                            else:
                                break #loop6


                        ID42 = self.match(self.input, ID, self.FOLLOW_ID_in_id_decl1250) 
                        stream_ID.add(ID42)



                    else:
                        break #loop7


                SEMICOLON43 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_id_decl1254) 
                stream_SEMICOLON.add(SEMICOLON43)


                # AST Rewrite
                # elements: ID, set_decl, set_decl, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 210:68: -> ^( ID_ ID ( set_decl )* ( ^( INITVAL_ ( set_decl )* ID ) )* )
                # Parser/ProtoCC.g:210:71: ^( ID_ ID ( set_decl )* ( ^( INITVAL_ ( set_decl )* ID ) )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(ID_, "ID_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:210:80: ( set_decl )*
                while stream_set_decl.hasNext():
                    self._adaptor.addChild(root_1, stream_set_decl.nextTree())


                stream_set_decl.reset();

                # Parser/ProtoCC.g:210:90: ( ^( INITVAL_ ( set_decl )* ID ) )*
                while stream_ID.hasNext():
                    # Parser/ProtoCC.g:210:90: ^( INITVAL_ ( set_decl )* ID )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(INITVAL_, "INITVAL_")
                    , root_2)

                    # Parser/ProtoCC.g:210:101: ( set_decl )*
                    while stream_set_decl.hasNext():
                        self._adaptor.addChild(root_2, stream_set_decl.nextTree())


                    stream_set_decl.reset();

                    self._adaptor.addChild(root_2, 
                    stream_ID.nextNode()
                    )

                    self._adaptor.addChild(root_1, root_2)


                stream_ID.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "id_decl"


    class set_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "set_decl"
    # Parser/ProtoCC.g:212:9: set_decl : SET OEBRACE val_range CEBRACE -> ^( SET_ val_range ) ;
    def set_decl(self, ):
        retval = self.set_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        SET44 = None
        OEBRACE45 = None
        CEBRACE47 = None
        val_range46 = None

        SET44_tree = None
        OEBRACE45_tree = None
        CEBRACE47_tree = None
        stream_SET = RewriteRuleTokenStream(self._adaptor, "token SET")
        stream_CEBRACE = RewriteRuleTokenStream(self._adaptor, "token CEBRACE")
        stream_OEBRACE = RewriteRuleTokenStream(self._adaptor, "token OEBRACE")
        stream_val_range = RewriteRuleSubtreeStream(self._adaptor, "rule val_range")
        try:
            try:
                # Parser/ProtoCC.g:212:18: ( SET OEBRACE val_range CEBRACE -> ^( SET_ val_range ) )
                # Parser/ProtoCC.g:212:20: SET OEBRACE val_range CEBRACE
                pass 
                SET44 = self.match(self.input, SET, self.FOLLOW_SET_in_set_decl1291) 
                stream_SET.add(SET44)


                OEBRACE45 = self.match(self.input, OEBRACE, self.FOLLOW_OEBRACE_in_set_decl1293) 
                stream_OEBRACE.add(OEBRACE45)


                self._state.following.append(self.FOLLOW_val_range_in_set_decl1295)
                val_range46 = self.val_range()

                self._state.following.pop()
                stream_val_range.add(val_range46.tree)


                CEBRACE47 = self.match(self.input, CEBRACE, self.FOLLOW_CEBRACE_in_set_decl1297) 
                stream_CEBRACE.add(CEBRACE47)


                # AST Rewrite
                # elements: val_range
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 212:50: -> ^( SET_ val_range )
                # Parser/ProtoCC.g:212:53: ^( SET_ val_range )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(SET_, "SET_")
                , root_1)

                self._adaptor.addChild(root_1, stream_val_range.nextTree())

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "set_decl"


    class range_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "range"
    # Parser/ProtoCC.g:213:9: range : OEBRACE val_range DOT DOT val_range CEBRACE -> ^( RANGE_ OEBRACE val_range DOT DOT val_range CEBRACE ) ;
    def range(self, ):
        retval = self.range_return()
        retval.start = self.input.LT(1)


        root_0 = None

        OEBRACE48 = None
        DOT50 = None
        DOT51 = None
        CEBRACE53 = None
        val_range49 = None
        val_range52 = None

        OEBRACE48_tree = None
        DOT50_tree = None
        DOT51_tree = None
        CEBRACE53_tree = None
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_CEBRACE = RewriteRuleTokenStream(self._adaptor, "token CEBRACE")
        stream_OEBRACE = RewriteRuleTokenStream(self._adaptor, "token OEBRACE")
        stream_val_range = RewriteRuleSubtreeStream(self._adaptor, "rule val_range")
        try:
            try:
                # Parser/ProtoCC.g:213:15: ( OEBRACE val_range DOT DOT val_range CEBRACE -> ^( RANGE_ OEBRACE val_range DOT DOT val_range CEBRACE ) )
                # Parser/ProtoCC.g:213:17: OEBRACE val_range DOT DOT val_range CEBRACE
                pass 
                OEBRACE48 = self.match(self.input, OEBRACE, self.FOLLOW_OEBRACE_in_range1320) 
                stream_OEBRACE.add(OEBRACE48)


                self._state.following.append(self.FOLLOW_val_range_in_range1322)
                val_range49 = self.val_range()

                self._state.following.pop()
                stream_val_range.add(val_range49.tree)


                DOT50 = self.match(self.input, DOT, self.FOLLOW_DOT_in_range1324) 
                stream_DOT.add(DOT50)


                DOT51 = self.match(self.input, DOT, self.FOLLOW_DOT_in_range1326) 
                stream_DOT.add(DOT51)


                self._state.following.append(self.FOLLOW_val_range_in_range1328)
                val_range52 = self.val_range()

                self._state.following.pop()
                stream_val_range.add(val_range52.tree)


                CEBRACE53 = self.match(self.input, CEBRACE, self.FOLLOW_CEBRACE_in_range1330) 
                stream_CEBRACE.add(CEBRACE53)


                # AST Rewrite
                # elements: OEBRACE, val_range, DOT, DOT, val_range, CEBRACE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 213:61: -> ^( RANGE_ OEBRACE val_range DOT DOT val_range CEBRACE )
                # Parser/ProtoCC.g:213:64: ^( RANGE_ OEBRACE val_range DOT DOT val_range CEBRACE )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(RANGE_, "RANGE_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_OEBRACE.nextNode()
                )

                self._adaptor.addChild(root_1, stream_val_range.nextTree())

                self._adaptor.addChild(root_1, 
                stream_DOT.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_DOT.nextNode()
                )

                self._adaptor.addChild(root_1, stream_val_range.nextTree())

                self._adaptor.addChild(root_1, 
                stream_CEBRACE.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "range"


    class val_range_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "val_range"
    # Parser/ProtoCC.g:214:9: val_range : ( INT | ID );
    def val_range(self, ):
        retval = self.val_range_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set54 = None

        set54_tree = None

        try:
            try:
                # Parser/ProtoCC.g:214:19: ( INT | ID )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set54 = self.input.LT(1)

                if self.input.LA(1) in {ID, INT}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set54))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "val_range"


    class array_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "array_decl"
    # Parser/ProtoCC.g:216:5: array_decl : ARRAY range ;
    def array_decl(self, ):
        retval = self.array_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ARRAY55 = None
        range56 = None

        ARRAY55_tree = None

        try:
            try:
                # Parser/ProtoCC.g:216:16: ( ARRAY range )
                # Parser/ProtoCC.g:216:18: ARRAY range
                pass 
                root_0 = self._adaptor.nil()


                ARRAY55 = self.match(self.input, ARRAY, self.FOLLOW_ARRAY_in_array_decl1379)
                ARRAY55_tree = self._adaptor.createWithPayload(ARRAY55)
                self._adaptor.addChild(root_0, ARRAY55_tree)



                self._state.following.append(self.FOLLOW_range_in_array_decl1381)
                range56 = self.range()

                self._state.following.pop()
                self._adaptor.addChild(root_0, range56.tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "array_decl"


    class fifo_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "fifo_decl"
    # Parser/ProtoCC.g:217:5: fifo_decl : FIFO range ;
    def fifo_decl(self, ):
        retval = self.fifo_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        FIFO57 = None
        range58 = None

        FIFO57_tree = None

        try:
            try:
                # Parser/ProtoCC.g:217:14: ( FIFO range )
                # Parser/ProtoCC.g:217:16: FIFO range
                pass 
                root_0 = self._adaptor.nil()


                FIFO57 = self.match(self.input, FIFO, self.FOLLOW_FIFO_in_fifo_decl1391)
                FIFO57_tree = self._adaptor.createWithPayload(FIFO57)
                self._adaptor.addChild(root_0, FIFO57_tree)



                self._state.following.append(self.FOLLOW_range_in_fifo_decl1393)
                range58 = self.range()

                self._state.following.pop()
                self._adaptor.addChild(root_0, range58.tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "fifo_decl"


    class init_hw_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "init_hw"
    # Parser/ProtoCC.g:220:1: init_hw : ( network_block | machines | message_block );
    def init_hw(self, ):
        retval = self.init_hw_return()
        retval.start = self.input.LT(1)


        root_0 = None

        network_block59 = None
        machines60 = None
        message_block61 = None


        try:
            try:
                # Parser/ProtoCC.g:220:9: ( network_block | machines | message_block )
                alt8 = 3
                LA8 = self.input.LA(1)
                if LA8 in {NETWORK}:
                    alt8 = 1
                elif LA8 in {CACHE, DIR, MEM}:
                    alt8 = 2
                elif LA8 in {MSG}:
                    alt8 = 3
                else:
                    nvae = NoViableAltException("", 8, 0, self.input)

                    raise nvae


                if alt8 == 1:
                    # Parser/ProtoCC.g:220:11: network_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_block_in_init_hw1403)
                    network_block59 = self.network_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_block59.tree)



                elif alt8 == 2:
                    # Parser/ProtoCC.g:220:27: machines
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_machines_in_init_hw1407)
                    machines60 = self.machines()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, machines60.tree)



                elif alt8 == 3:
                    # Parser/ProtoCC.g:220:38: message_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_message_block_in_init_hw1411)
                    message_block61 = self.message_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, message_block61.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "init_hw"


    class object_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "object_block"
    # Parser/ProtoCC.g:221:5: object_block : object_expr SEMICOLON -> object_expr ;
    def object_block(self, ):
        retval = self.object_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        SEMICOLON63 = None
        object_expr62 = None

        SEMICOLON63_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_object_expr = RewriteRuleSubtreeStream(self._adaptor, "rule object_expr")
        try:
            try:
                # Parser/ProtoCC.g:221:18: ( object_expr SEMICOLON -> object_expr )
                # Parser/ProtoCC.g:221:20: object_expr SEMICOLON
                pass 
                self._state.following.append(self.FOLLOW_object_expr_in_object_block1422)
                object_expr62 = self.object_expr()

                self._state.following.pop()
                stream_object_expr.add(object_expr62.tree)


                SEMICOLON63 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_object_block1424) 
                stream_SEMICOLON.add(SEMICOLON63)


                # AST Rewrite
                # elements: object_expr
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 221:42: -> object_expr
                self._adaptor.addChild(root_0, stream_object_expr.nextTree())




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "object_block"


    class object_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "object_expr"
    # Parser/ProtoCC.g:222:5: object_expr : ( object_id | object_func );
    def object_expr(self, ):
        retval = self.object_expr_return()
        retval.start = self.input.LT(1)


        root_0 = None

        object_id64 = None
        object_func65 = None


        try:
            try:
                # Parser/ProtoCC.g:222:17: ( object_id | object_func )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == ID) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == DOT) :
                        alt9 = 2
                    elif ((99 <= LA9_1 <= 105) or LA9_1 in {BOOL, CBRACE, COMMA, ID, INT, MINUS, MULT, NID, OCBRACE, PLUS, SEMICOLON, 121}) :
                        alt9 = 1
                    else:
                        nvae = NoViableAltException("", 9, 1, self.input)

                        raise nvae


                else:
                    nvae = NoViableAltException("", 9, 0, self.input)

                    raise nvae


                if alt9 == 1:
                    # Parser/ProtoCC.g:222:19: object_id
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_id_in_object_expr1439)
                    object_id64 = self.object_id()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_id64.tree)



                elif alt9 == 2:
                    # Parser/ProtoCC.g:222:31: object_func
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_func_in_object_expr1443)
                    object_func65 = self.object_func()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_func65.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "object_expr"


    class object_id_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "object_id"
    # Parser/ProtoCC.g:223:5: object_id : ID -> ^( ID ) ;
    def object_id(self, ):
        retval = self.object_id_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID66 = None

        ID66_tree = None
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")

        try:
            try:
                # Parser/ProtoCC.g:223:14: ( ID -> ^( ID ) )
                # Parser/ProtoCC.g:223:17: ID
                pass 
                ID66 = self.match(self.input, ID, self.FOLLOW_ID_in_object_id1454) 
                stream_ID.add(ID66)


                # AST Rewrite
                # elements: ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 223:20: -> ^( ID )
                # Parser/ProtoCC.g:223:23: ^( ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                stream_ID.nextNode()
                , root_1)

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "object_id"


    class object_func_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "object_func"
    # Parser/ProtoCC.g:224:5: object_func : ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )* -> ^( ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )* ) ;
    def object_func(self, ):
        retval = self.object_func_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID67 = None
        DOT68 = None
        OBRACE70 = None
        COMMA72 = None
        CBRACE74 = None
        object_idres69 = None
        object_expr71 = None
        object_expr73 = None

        ID67_tree = None
        DOT68_tree = None
        OBRACE70_tree = None
        COMMA72_tree = None
        CBRACE74_tree = None
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_object_idres = RewriteRuleSubtreeStream(self._adaptor, "rule object_idres")
        stream_object_expr = RewriteRuleSubtreeStream(self._adaptor, "rule object_expr")
        try:
            try:
                # Parser/ProtoCC.g:224:17: ( ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )* -> ^( ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )* ) )
                # Parser/ProtoCC.g:224:19: ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )*
                pass 
                ID67 = self.match(self.input, ID, self.FOLLOW_ID_in_object_func1471) 
                stream_ID.add(ID67)


                DOT68 = self.match(self.input, DOT, self.FOLLOW_DOT_in_object_func1473) 
                stream_DOT.add(DOT68)


                self._state.following.append(self.FOLLOW_object_idres_in_object_func1475)
                object_idres69 = self.object_idres()

                self._state.following.pop()
                stream_object_idres.add(object_idres69.tree)


                # Parser/ProtoCC.g:224:39: ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )*
                while True: #loop12
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if (LA12_0 == OBRACE) :
                        alt12 = 1


                    if alt12 == 1:
                        # Parser/ProtoCC.g:224:40: OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE
                        pass 
                        OBRACE70 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_object_func1478) 
                        stream_OBRACE.add(OBRACE70)


                        # Parser/ProtoCC.g:224:47: ( object_expr )*
                        while True: #loop10
                            alt10 = 2
                            LA10_0 = self.input.LA(1)

                            if (LA10_0 == ID) :
                                alt10 = 1


                            if alt10 == 1:
                                # Parser/ProtoCC.g:224:47: object_expr
                                pass 
                                self._state.following.append(self.FOLLOW_object_expr_in_object_func1480)
                                object_expr71 = self.object_expr()

                                self._state.following.pop()
                                stream_object_expr.add(object_expr71.tree)



                            else:
                                break #loop10


                        # Parser/ProtoCC.g:224:60: ( COMMA object_expr )*
                        while True: #loop11
                            alt11 = 2
                            LA11_0 = self.input.LA(1)

                            if (LA11_0 == COMMA) :
                                alt11 = 1


                            if alt11 == 1:
                                # Parser/ProtoCC.g:224:61: COMMA object_expr
                                pass 
                                COMMA72 = self.match(self.input, COMMA, self.FOLLOW_COMMA_in_object_func1484) 
                                stream_COMMA.add(COMMA72)


                                self._state.following.append(self.FOLLOW_object_expr_in_object_func1486)
                                object_expr73 = self.object_expr()

                                self._state.following.pop()
                                stream_object_expr.add(object_expr73.tree)



                            else:
                                break #loop11


                        CBRACE74 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_object_func1490) 
                        stream_CBRACE.add(CBRACE74)



                    else:
                        break #loop12


                # AST Rewrite
                # elements: ID, DOT, object_idres, OBRACE, object_expr, COMMA, object_expr, CBRACE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 224:90: -> ^( ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )* )
                # Parser/ProtoCC.g:225:9: ^( ID DOT object_idres ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                stream_ID.nextNode()
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_DOT.nextNode()
                )

                self._adaptor.addChild(root_1, stream_object_idres.nextTree())

                # Parser/ProtoCC.g:225:31: ( OBRACE ( object_expr )* ( COMMA object_expr )* CBRACE )*
                while stream_OBRACE.hasNext() or stream_CBRACE.hasNext():
                    self._adaptor.addChild(root_1, 
                    stream_OBRACE.nextNode()
                    )

                    # Parser/ProtoCC.g:225:39: ( object_expr )*
                    while stream_object_expr.hasNext():
                        self._adaptor.addChild(root_1, stream_object_expr.nextTree())


                    stream_object_expr.reset();

                    # Parser/ProtoCC.g:225:52: ( COMMA object_expr )*
                    while stream_COMMA.hasNext() or stream_object_expr.hasNext():
                        self._adaptor.addChild(root_1, 
                        stream_COMMA.nextNode()
                        )

                        self._adaptor.addChild(root_1, stream_object_expr.nextTree())


                    stream_COMMA.reset();
                    stream_object_expr.reset();

                    self._adaptor.addChild(root_1, 
                    stream_CBRACE.nextNode()
                    )


                stream_OBRACE.reset();
                stream_CBRACE.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "object_func"


    class object_idres_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "object_idres"
    # Parser/ProtoCC.g:226:5: object_idres : ( ID | NID );
    def object_idres(self, ):
        retval = self.object_idres_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set75 = None

        set75_tree = None

        try:
            try:
                # Parser/ProtoCC.g:226:17: ( ID | NID )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set75 = self.input.LT(1)

                if self.input.LA(1) in {ID, NID}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set75))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "object_idres"


    class machines_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "machines"
    # Parser/ProtoCC.g:229:5: machines : ( cache_block | dir_block | mem_block );
    def machines(self, ):
        retval = self.machines_return()
        retval.start = self.input.LT(1)


        root_0 = None

        cache_block76 = None
        dir_block77 = None
        mem_block78 = None


        try:
            try:
                # Parser/ProtoCC.g:229:14: ( cache_block | dir_block | mem_block )
                alt13 = 3
                LA13 = self.input.LA(1)
                if LA13 in {CACHE}:
                    alt13 = 1
                elif LA13 in {DIR}:
                    alt13 = 2
                elif LA13 in {MEM}:
                    alt13 = 3
                else:
                    nvae = NoViableAltException("", 13, 0, self.input)

                    raise nvae


                if alt13 == 1:
                    # Parser/ProtoCC.g:229:16: cache_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_cache_block_in_machines1559)
                    cache_block76 = self.cache_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, cache_block76.tree)



                elif alt13 == 2:
                    # Parser/ProtoCC.g:229:30: dir_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_dir_block_in_machines1563)
                    dir_block77 = self.dir_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, dir_block77.tree)



                elif alt13 == 3:
                    # Parser/ProtoCC.g:229:42: mem_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_mem_block_in_machines1567)
                    mem_block78 = self.mem_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, mem_block78.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "machines"


    class cache_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "cache_block"
    # Parser/ProtoCC.g:230:9: cache_block : CACHE OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON -> ^( CACHE_ ID ( objset_decl )* ( declarations )* ) ;
    def cache_block(self, ):
        retval = self.cache_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        CACHE79 = None
        OCBRACE80 = None
        CCBRACE82 = None
        ID84 = None
        SEMICOLON85 = None
        declarations81 = None
        objset_decl83 = None

        CACHE79_tree = None
        OCBRACE80_tree = None
        CCBRACE82_tree = None
        ID84_tree = None
        SEMICOLON85_tree = None
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CACHE = RewriteRuleTokenStream(self._adaptor, "token CACHE")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_objset_decl = RewriteRuleSubtreeStream(self._adaptor, "rule objset_decl")
        stream_declarations = RewriteRuleSubtreeStream(self._adaptor, "rule declarations")
        try:
            try:
                # Parser/ProtoCC.g:230:21: ( CACHE OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON -> ^( CACHE_ ID ( objset_decl )* ( declarations )* ) )
                # Parser/ProtoCC.g:230:23: CACHE OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON
                pass 
                CACHE79 = self.match(self.input, CACHE, self.FOLLOW_CACHE_in_cache_block1582) 
                stream_CACHE.add(CACHE79)


                OCBRACE80 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_cache_block1584) 
                stream_OCBRACE.add(OCBRACE80)


                # Parser/ProtoCC.g:230:37: ( declarations )*
                while True: #loop14
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 in {BOOLID, DATA, INTID, NID, SET, STATE}) :
                        alt14 = 1


                    if alt14 == 1:
                        # Parser/ProtoCC.g:230:37: declarations
                        pass 
                        self._state.following.append(self.FOLLOW_declarations_in_cache_block1586)
                        declarations81 = self.declarations()

                        self._state.following.pop()
                        stream_declarations.add(declarations81.tree)



                    else:
                        break #loop14


                CCBRACE82 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_cache_block1589) 
                stream_CCBRACE.add(CCBRACE82)


                # Parser/ProtoCC.g:230:59: ( objset_decl )*
                while True: #loop15
                    alt15 = 2
                    LA15_0 = self.input.LA(1)

                    if (LA15_0 == SET) :
                        alt15 = 1


                    if alt15 == 1:
                        # Parser/ProtoCC.g:230:59: objset_decl
                        pass 
                        self._state.following.append(self.FOLLOW_objset_decl_in_cache_block1591)
                        objset_decl83 = self.objset_decl()

                        self._state.following.pop()
                        stream_objset_decl.add(objset_decl83.tree)



                    else:
                        break #loop15


                ID84 = self.match(self.input, ID, self.FOLLOW_ID_in_cache_block1594) 
                stream_ID.add(ID84)


                SEMICOLON85 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_cache_block1596) 
                stream_SEMICOLON.add(SEMICOLON85)


                # AST Rewrite
                # elements: ID, objset_decl, declarations
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 230:85: -> ^( CACHE_ ID ( objset_decl )* ( declarations )* )
                # Parser/ProtoCC.g:231:13: ^( CACHE_ ID ( objset_decl )* ( declarations )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(CACHE_, "CACHE_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:231:25: ( objset_decl )*
                while stream_objset_decl.hasNext():
                    self._adaptor.addChild(root_1, stream_objset_decl.nextTree())


                stream_objset_decl.reset();

                # Parser/ProtoCC.g:231:38: ( declarations )*
                while stream_declarations.hasNext():
                    self._adaptor.addChild(root_1, stream_declarations.nextTree())


                stream_declarations.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "cache_block"


    class dir_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "dir_block"
    # Parser/ProtoCC.g:232:9: dir_block : DIR OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON -> ^( DIR_ ID ( objset_decl )* ( declarations )* ) ;
    def dir_block(self, ):
        retval = self.dir_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        DIR86 = None
        OCBRACE87 = None
        CCBRACE89 = None
        ID91 = None
        SEMICOLON92 = None
        declarations88 = None
        objset_decl90 = None

        DIR86_tree = None
        OCBRACE87_tree = None
        CCBRACE89_tree = None
        ID91_tree = None
        SEMICOLON92_tree = None
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_DIR = RewriteRuleTokenStream(self._adaptor, "token DIR")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_objset_decl = RewriteRuleSubtreeStream(self._adaptor, "rule objset_decl")
        stream_declarations = RewriteRuleSubtreeStream(self._adaptor, "rule declarations")
        try:
            try:
                # Parser/ProtoCC.g:232:19: ( DIR OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON -> ^( DIR_ ID ( objset_decl )* ( declarations )* ) )
                # Parser/ProtoCC.g:232:21: DIR OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON
                pass 
                DIR86 = self.match(self.input, DIR, self.FOLLOW_DIR_in_dir_block1637) 
                stream_DIR.add(DIR86)


                OCBRACE87 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_dir_block1639) 
                stream_OCBRACE.add(OCBRACE87)


                # Parser/ProtoCC.g:232:33: ( declarations )*
                while True: #loop16
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if (LA16_0 in {BOOLID, DATA, INTID, NID, SET, STATE}) :
                        alt16 = 1


                    if alt16 == 1:
                        # Parser/ProtoCC.g:232:33: declarations
                        pass 
                        self._state.following.append(self.FOLLOW_declarations_in_dir_block1641)
                        declarations88 = self.declarations()

                        self._state.following.pop()
                        stream_declarations.add(declarations88.tree)



                    else:
                        break #loop16


                CCBRACE89 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_dir_block1644) 
                stream_CCBRACE.add(CCBRACE89)


                # Parser/ProtoCC.g:232:55: ( objset_decl )*
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if (LA17_0 == SET) :
                        alt17 = 1


                    if alt17 == 1:
                        # Parser/ProtoCC.g:232:55: objset_decl
                        pass 
                        self._state.following.append(self.FOLLOW_objset_decl_in_dir_block1646)
                        objset_decl90 = self.objset_decl()

                        self._state.following.pop()
                        stream_objset_decl.add(objset_decl90.tree)



                    else:
                        break #loop17


                ID91 = self.match(self.input, ID, self.FOLLOW_ID_in_dir_block1649) 
                stream_ID.add(ID91)


                SEMICOLON92 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_dir_block1651) 
                stream_SEMICOLON.add(SEMICOLON92)


                # AST Rewrite
                # elements: ID, objset_decl, declarations
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 232:81: -> ^( DIR_ ID ( objset_decl )* ( declarations )* )
                # Parser/ProtoCC.g:233:13: ^( DIR_ ID ( objset_decl )* ( declarations )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(DIR_, "DIR_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:233:23: ( objset_decl )*
                while stream_objset_decl.hasNext():
                    self._adaptor.addChild(root_1, stream_objset_decl.nextTree())


                stream_objset_decl.reset();

                # Parser/ProtoCC.g:233:36: ( declarations )*
                while stream_declarations.hasNext():
                    self._adaptor.addChild(root_1, stream_declarations.nextTree())


                stream_declarations.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "dir_block"


    class mem_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "mem_block"
    # Parser/ProtoCC.g:234:9: mem_block : MEM OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON -> ^( MEM_ ID ( objset_decl )* ( declarations )* ) ;
    def mem_block(self, ):
        retval = self.mem_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        MEM93 = None
        OCBRACE94 = None
        CCBRACE96 = None
        ID98 = None
        SEMICOLON99 = None
        declarations95 = None
        objset_decl97 = None

        MEM93_tree = None
        OCBRACE94_tree = None
        CCBRACE96_tree = None
        ID98_tree = None
        SEMICOLON99_tree = None
        stream_MEM = RewriteRuleTokenStream(self._adaptor, "token MEM")
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_objset_decl = RewriteRuleSubtreeStream(self._adaptor, "rule objset_decl")
        stream_declarations = RewriteRuleSubtreeStream(self._adaptor, "rule declarations")
        try:
            try:
                # Parser/ProtoCC.g:234:19: ( MEM OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON -> ^( MEM_ ID ( objset_decl )* ( declarations )* ) )
                # Parser/ProtoCC.g:234:21: MEM OCBRACE ( declarations )* CCBRACE ( objset_decl )* ID SEMICOLON
                pass 
                MEM93 = self.match(self.input, MEM, self.FOLLOW_MEM_in_mem_block1692) 
                stream_MEM.add(MEM93)


                OCBRACE94 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_mem_block1694) 
                stream_OCBRACE.add(OCBRACE94)


                # Parser/ProtoCC.g:234:33: ( declarations )*
                while True: #loop18
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 in {BOOLID, DATA, INTID, NID, SET, STATE}) :
                        alt18 = 1


                    if alt18 == 1:
                        # Parser/ProtoCC.g:234:33: declarations
                        pass 
                        self._state.following.append(self.FOLLOW_declarations_in_mem_block1696)
                        declarations95 = self.declarations()

                        self._state.following.pop()
                        stream_declarations.add(declarations95.tree)



                    else:
                        break #loop18


                CCBRACE96 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_mem_block1699) 
                stream_CCBRACE.add(CCBRACE96)


                # Parser/ProtoCC.g:234:55: ( objset_decl )*
                while True: #loop19
                    alt19 = 2
                    LA19_0 = self.input.LA(1)

                    if (LA19_0 == SET) :
                        alt19 = 1


                    if alt19 == 1:
                        # Parser/ProtoCC.g:234:55: objset_decl
                        pass 
                        self._state.following.append(self.FOLLOW_objset_decl_in_mem_block1701)
                        objset_decl97 = self.objset_decl()

                        self._state.following.pop()
                        stream_objset_decl.add(objset_decl97.tree)



                    else:
                        break #loop19


                ID98 = self.match(self.input, ID, self.FOLLOW_ID_in_mem_block1704) 
                stream_ID.add(ID98)


                SEMICOLON99 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_mem_block1706) 
                stream_SEMICOLON.add(SEMICOLON99)


                # AST Rewrite
                # elements: ID, objset_decl, declarations
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 234:81: -> ^( MEM_ ID ( objset_decl )* ( declarations )* )
                # Parser/ProtoCC.g:235:13: ^( MEM_ ID ( objset_decl )* ( declarations )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(MEM_, "MEM_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:235:23: ( objset_decl )*
                while stream_objset_decl.hasNext():
                    self._adaptor.addChild(root_1, stream_objset_decl.nextTree())


                stream_objset_decl.reset();

                # Parser/ProtoCC.g:235:36: ( declarations )*
                while stream_declarations.hasNext():
                    self._adaptor.addChild(root_1, stream_declarations.nextTree())


                stream_declarations.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "mem_block"


    class objset_decl_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "objset_decl"
    # Parser/ProtoCC.g:237:9: objset_decl : SET OEBRACE val_range CEBRACE -> ^( OBJSET_ val_range ) ;
    def objset_decl(self, ):
        retval = self.objset_decl_return()
        retval.start = self.input.LT(1)


        root_0 = None

        SET100 = None
        OEBRACE101 = None
        CEBRACE103 = None
        val_range102 = None

        SET100_tree = None
        OEBRACE101_tree = None
        CEBRACE103_tree = None
        stream_SET = RewriteRuleTokenStream(self._adaptor, "token SET")
        stream_CEBRACE = RewriteRuleTokenStream(self._adaptor, "token CEBRACE")
        stream_OEBRACE = RewriteRuleTokenStream(self._adaptor, "token OEBRACE")
        stream_val_range = RewriteRuleSubtreeStream(self._adaptor, "rule val_range")
        try:
            try:
                # Parser/ProtoCC.g:237:21: ( SET OEBRACE val_range CEBRACE -> ^( OBJSET_ val_range ) )
                # Parser/ProtoCC.g:237:23: SET OEBRACE val_range CEBRACE
                pass 
                SET100 = self.match(self.input, SET, self.FOLLOW_SET_in_objset_decl1748) 
                stream_SET.add(SET100)


                OEBRACE101 = self.match(self.input, OEBRACE, self.FOLLOW_OEBRACE_in_objset_decl1750) 
                stream_OEBRACE.add(OEBRACE101)


                self._state.following.append(self.FOLLOW_val_range_in_objset_decl1752)
                val_range102 = self.val_range()

                self._state.following.pop()
                stream_val_range.add(val_range102.tree)


                CEBRACE103 = self.match(self.input, CEBRACE, self.FOLLOW_CEBRACE_in_objset_decl1754) 
                stream_CEBRACE.add(CEBRACE103)


                # AST Rewrite
                # elements: val_range
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 237:53: -> ^( OBJSET_ val_range )
                # Parser/ProtoCC.g:237:56: ^( OBJSET_ val_range )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(OBJSET_, "OBJSET_")
                , root_1)

                self._adaptor.addChild(root_1, stream_val_range.nextTree())

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "objset_decl"


    class network_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "network_block"
    # Parser/ProtoCC.g:240:5: network_block : NETWORK OCBRACE ( network_element )* CCBRACE SEMICOLON -> ^( NETWORK_ ( network_element )* ) ;
    def network_block(self, ):
        retval = self.network_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        NETWORK104 = None
        OCBRACE105 = None
        CCBRACE107 = None
        SEMICOLON108 = None
        network_element106 = None

        NETWORK104_tree = None
        OCBRACE105_tree = None
        CCBRACE107_tree = None
        SEMICOLON108_tree = None
        stream_NETWORK = RewriteRuleTokenStream(self._adaptor, "token NETWORK")
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_network_element = RewriteRuleSubtreeStream(self._adaptor, "rule network_element")
        try:
            try:
                # Parser/ProtoCC.g:240:19: ( NETWORK OCBRACE ( network_element )* CCBRACE SEMICOLON -> ^( NETWORK_ ( network_element )* ) )
                # Parser/ProtoCC.g:240:21: NETWORK OCBRACE ( network_element )* CCBRACE SEMICOLON
                pass 
                NETWORK104 = self.match(self.input, NETWORK, self.FOLLOW_NETWORK_in_network_block1780) 
                stream_NETWORK.add(NETWORK104)


                OCBRACE105 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_network_block1782) 
                stream_OCBRACE.add(OCBRACE105)


                # Parser/ProtoCC.g:240:37: ( network_element )*
                while True: #loop20
                    alt20 = 2
                    LA20_0 = self.input.LA(1)

                    if (LA20_0 in {109, 111}) :
                        alt20 = 1


                    if alt20 == 1:
                        # Parser/ProtoCC.g:240:37: network_element
                        pass 
                        self._state.following.append(self.FOLLOW_network_element_in_network_block1784)
                        network_element106 = self.network_element()

                        self._state.following.pop()
                        stream_network_element.add(network_element106.tree)



                    else:
                        break #loop20


                CCBRACE107 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_network_block1787) 
                stream_CCBRACE.add(CCBRACE107)


                SEMICOLON108 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_network_block1789) 
                stream_SEMICOLON.add(SEMICOLON108)


                # AST Rewrite
                # elements: network_element
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 240:72: -> ^( NETWORK_ ( network_element )* )
                # Parser/ProtoCC.g:240:75: ^( NETWORK_ ( network_element )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(NETWORK_, "NETWORK_")
                , root_1)

                # Parser/ProtoCC.g:240:86: ( network_element )*
                while stream_network_element.hasNext():
                    self._adaptor.addChild(root_1, stream_network_element.nextTree())


                stream_network_element.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "network_block"


    class element_type_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "element_type"
    # Parser/ProtoCC.g:241:9: element_type : ( 'Ordered' | 'Unordered' );
    def element_type(self, ):
        retval = self.element_type_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set109 = None

        set109_tree = None

        try:
            try:
                # Parser/ProtoCC.g:241:22: ( 'Ordered' | 'Unordered' )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set109 = self.input.LT(1)

                if self.input.LA(1) in {109, 111}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set109))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "element_type"


    class network_element_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "network_element"
    # Parser/ProtoCC.g:242:9: network_element : element_type ID SEMICOLON -> ^( ELEMENT_ element_type ID ) ;
    def network_element(self, ):
        retval = self.network_element_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID111 = None
        SEMICOLON112 = None
        element_type110 = None

        ID111_tree = None
        SEMICOLON112_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_element_type = RewriteRuleSubtreeStream(self._adaptor, "rule element_type")
        try:
            try:
                # Parser/ProtoCC.g:242:25: ( element_type ID SEMICOLON -> ^( ELEMENT_ element_type ID ) )
                # Parser/ProtoCC.g:242:27: element_type ID SEMICOLON
                pass 
                self._state.following.append(self.FOLLOW_element_type_in_network_element1832)
                element_type110 = self.element_type()

                self._state.following.pop()
                stream_element_type.add(element_type110.tree)


                ID111 = self.match(self.input, ID, self.FOLLOW_ID_in_network_element1834) 
                stream_ID.add(ID111)


                SEMICOLON112 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_network_element1836) 
                stream_SEMICOLON.add(SEMICOLON112)


                # AST Rewrite
                # elements: element_type, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 242:53: -> ^( ELEMENT_ element_type ID )
                # Parser/ProtoCC.g:242:56: ^( ELEMENT_ element_type ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(ELEMENT_, "ELEMENT_")
                , root_1)

                self._adaptor.addChild(root_1, stream_element_type.nextTree())

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "network_element"


    class network_send_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "network_send"
    # Parser/ProtoCC.g:243:5: network_send : ID DOT send_function OBRACE ID CBRACE SEMICOLON -> ^( SEND_ ID ID ) ;
    def network_send(self, ):
        retval = self.network_send_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID113 = None
        DOT114 = None
        OBRACE116 = None
        ID117 = None
        CBRACE118 = None
        SEMICOLON119 = None
        send_function115 = None

        ID113_tree = None
        DOT114_tree = None
        OBRACE116_tree = None
        ID117_tree = None
        CBRACE118_tree = None
        SEMICOLON119_tree = None
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_send_function = RewriteRuleSubtreeStream(self._adaptor, "rule send_function")
        try:
            try:
                # Parser/ProtoCC.g:243:18: ( ID DOT send_function OBRACE ID CBRACE SEMICOLON -> ^( SEND_ ID ID ) )
                # Parser/ProtoCC.g:243:20: ID DOT send_function OBRACE ID CBRACE SEMICOLON
                pass 
                ID113 = self.match(self.input, ID, self.FOLLOW_ID_in_network_send1857) 
                stream_ID.add(ID113)


                DOT114 = self.match(self.input, DOT, self.FOLLOW_DOT_in_network_send1859) 
                stream_DOT.add(DOT114)


                self._state.following.append(self.FOLLOW_send_function_in_network_send1861)
                send_function115 = self.send_function()

                self._state.following.pop()
                stream_send_function.add(send_function115.tree)


                OBRACE116 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_network_send1863) 
                stream_OBRACE.add(OBRACE116)


                ID117 = self.match(self.input, ID, self.FOLLOW_ID_in_network_send1865) 
                stream_ID.add(ID117)


                CBRACE118 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_network_send1867) 
                stream_CBRACE.add(CBRACE118)


                SEMICOLON119 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_network_send1869) 
                stream_SEMICOLON.add(SEMICOLON119)


                # AST Rewrite
                # elements: ID, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 243:68: -> ^( SEND_ ID ID )
                # Parser/ProtoCC.g:243:71: ^( SEND_ ID ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(SEND_, "SEND_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "network_send"


    class network_bcast_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "network_bcast"
    # Parser/ProtoCC.g:244:5: network_bcast : ID DOT bcast_function OBRACE ID CBRACE SEMICOLON -> ^( BCAST_ ID ID ) ;
    def network_bcast(self, ):
        retval = self.network_bcast_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID120 = None
        DOT121 = None
        OBRACE123 = None
        ID124 = None
        CBRACE125 = None
        SEMICOLON126 = None
        bcast_function122 = None

        ID120_tree = None
        DOT121_tree = None
        OBRACE123_tree = None
        ID124_tree = None
        CBRACE125_tree = None
        SEMICOLON126_tree = None
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_bcast_function = RewriteRuleSubtreeStream(self._adaptor, "rule bcast_function")
        try:
            try:
                # Parser/ProtoCC.g:244:18: ( ID DOT bcast_function OBRACE ID CBRACE SEMICOLON -> ^( BCAST_ ID ID ) )
                # Parser/ProtoCC.g:244:20: ID DOT bcast_function OBRACE ID CBRACE SEMICOLON
                pass 
                ID120 = self.match(self.input, ID, self.FOLLOW_ID_in_network_bcast1889) 
                stream_ID.add(ID120)


                DOT121 = self.match(self.input, DOT, self.FOLLOW_DOT_in_network_bcast1891) 
                stream_DOT.add(DOT121)


                self._state.following.append(self.FOLLOW_bcast_function_in_network_bcast1893)
                bcast_function122 = self.bcast_function()

                self._state.following.pop()
                stream_bcast_function.add(bcast_function122.tree)


                OBRACE123 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_network_bcast1895) 
                stream_OBRACE.add(OBRACE123)


                ID124 = self.match(self.input, ID, self.FOLLOW_ID_in_network_bcast1897) 
                stream_ID.add(ID124)


                CBRACE125 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_network_bcast1899) 
                stream_CBRACE.add(CBRACE125)


                SEMICOLON126 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_network_bcast1901) 
                stream_SEMICOLON.add(SEMICOLON126)


                # AST Rewrite
                # elements: ID, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 244:69: -> ^( BCAST_ ID ID )
                # Parser/ProtoCC.g:244:72: ^( BCAST_ ID ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(BCAST_, "BCAST_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "network_bcast"


    class network_mcast_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "network_mcast"
    # Parser/ProtoCC.g:245:5: network_mcast : ID DOT mcast_function OBRACE ID COMMA ID CBRACE SEMICOLON -> ^( MCAST_ ID ID ID ) ;
    def network_mcast(self, ):
        retval = self.network_mcast_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID127 = None
        DOT128 = None
        OBRACE130 = None
        ID131 = None
        COMMA132 = None
        ID133 = None
        CBRACE134 = None
        SEMICOLON135 = None
        mcast_function129 = None

        ID127_tree = None
        DOT128_tree = None
        OBRACE130_tree = None
        ID131_tree = None
        COMMA132_tree = None
        ID133_tree = None
        CBRACE134_tree = None
        SEMICOLON135_tree = None
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_mcast_function = RewriteRuleSubtreeStream(self._adaptor, "rule mcast_function")
        try:
            try:
                # Parser/ProtoCC.g:245:18: ( ID DOT mcast_function OBRACE ID COMMA ID CBRACE SEMICOLON -> ^( MCAST_ ID ID ID ) )
                # Parser/ProtoCC.g:245:20: ID DOT mcast_function OBRACE ID COMMA ID CBRACE SEMICOLON
                pass 
                ID127 = self.match(self.input, ID, self.FOLLOW_ID_in_network_mcast1921) 
                stream_ID.add(ID127)


                DOT128 = self.match(self.input, DOT, self.FOLLOW_DOT_in_network_mcast1923) 
                stream_DOT.add(DOT128)


                self._state.following.append(self.FOLLOW_mcast_function_in_network_mcast1925)
                mcast_function129 = self.mcast_function()

                self._state.following.pop()
                stream_mcast_function.add(mcast_function129.tree)


                OBRACE130 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_network_mcast1927) 
                stream_OBRACE.add(OBRACE130)


                ID131 = self.match(self.input, ID, self.FOLLOW_ID_in_network_mcast1929) 
                stream_ID.add(ID131)


                COMMA132 = self.match(self.input, COMMA, self.FOLLOW_COMMA_in_network_mcast1931) 
                stream_COMMA.add(COMMA132)


                ID133 = self.match(self.input, ID, self.FOLLOW_ID_in_network_mcast1933) 
                stream_ID.add(ID133)


                CBRACE134 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_network_mcast1935) 
                stream_CBRACE.add(CBRACE134)


                SEMICOLON135 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_network_mcast1937) 
                stream_SEMICOLON.add(SEMICOLON135)


                # AST Rewrite
                # elements: ID, ID, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 245:78: -> ^( MCAST_ ID ID ID )
                # Parser/ProtoCC.g:245:81: ^( MCAST_ ID ID ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(MCAST_, "MCAST_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "network_mcast"


    class message_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "message_block"
    # Parser/ProtoCC.g:248:5: message_block : MSG ID OCBRACE ( declarations )* CCBRACE SEMICOLON -> ^( MSG_ ID ( declarations )* ) ;
    def message_block(self, ):
        retval = self.message_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        MSG136 = None
        ID137 = None
        OCBRACE138 = None
        CCBRACE140 = None
        SEMICOLON141 = None
        declarations139 = None

        MSG136_tree = None
        ID137_tree = None
        OCBRACE138_tree = None
        CCBRACE140_tree = None
        SEMICOLON141_tree = None
        stream_MSG = RewriteRuleTokenStream(self._adaptor, "token MSG")
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_declarations = RewriteRuleSubtreeStream(self._adaptor, "rule declarations")
        try:
            try:
                # Parser/ProtoCC.g:248:19: ( MSG ID OCBRACE ( declarations )* CCBRACE SEMICOLON -> ^( MSG_ ID ( declarations )* ) )
                # Parser/ProtoCC.g:248:21: MSG ID OCBRACE ( declarations )* CCBRACE SEMICOLON
                pass 
                MSG136 = self.match(self.input, MSG, self.FOLLOW_MSG_in_message_block1967) 
                stream_MSG.add(MSG136)


                ID137 = self.match(self.input, ID, self.FOLLOW_ID_in_message_block1969) 
                stream_ID.add(ID137)


                OCBRACE138 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_message_block1971) 
                stream_OCBRACE.add(OCBRACE138)


                # Parser/ProtoCC.g:248:36: ( declarations )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 in {BOOLID, DATA, INTID, NID, SET, STATE}) :
                        alt21 = 1


                    if alt21 == 1:
                        # Parser/ProtoCC.g:248:36: declarations
                        pass 
                        self._state.following.append(self.FOLLOW_declarations_in_message_block1973)
                        declarations139 = self.declarations()

                        self._state.following.pop()
                        stream_declarations.add(declarations139.tree)



                    else:
                        break #loop21


                CCBRACE140 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_message_block1976) 
                stream_CCBRACE.add(CCBRACE140)


                SEMICOLON141 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_message_block1978) 
                stream_SEMICOLON.add(SEMICOLON141)


                # AST Rewrite
                # elements: ID, declarations
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 248:68: -> ^( MSG_ ID ( declarations )* )
                # Parser/ProtoCC.g:248:71: ^( MSG_ ID ( declarations )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(MSG_, "MSG_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:248:81: ( declarations )*
                while stream_declarations.hasNext():
                    self._adaptor.addChild(root_1, stream_declarations.nextTree())


                stream_declarations.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "message_block"


    class message_constr_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "message_constr"
    # Parser/ProtoCC.g:249:5: message_constr : ID OBRACE ( message_expr )* ( COMMA message_expr )* CBRACE -> ^( MSGCSTR_ ID ( message_expr )* ) ;
    def message_constr(self, ):
        retval = self.message_constr_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID142 = None
        OBRACE143 = None
        COMMA145 = None
        CBRACE147 = None
        message_expr144 = None
        message_expr146 = None

        ID142_tree = None
        OBRACE143_tree = None
        COMMA145_tree = None
        CBRACE147_tree = None
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_message_expr = RewriteRuleSubtreeStream(self._adaptor, "rule message_expr")
        try:
            try:
                # Parser/ProtoCC.g:249:20: ( ID OBRACE ( message_expr )* ( COMMA message_expr )* CBRACE -> ^( MSGCSTR_ ID ( message_expr )* ) )
                # Parser/ProtoCC.g:249:22: ID OBRACE ( message_expr )* ( COMMA message_expr )* CBRACE
                pass 
                ID142 = self.match(self.input, ID, self.FOLLOW_ID_in_message_constr2000) 
                stream_ID.add(ID142)


                OBRACE143 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_message_constr2002) 
                stream_OBRACE.add(OBRACE143)


                # Parser/ProtoCC.g:249:32: ( message_expr )*
                while True: #loop22
                    alt22 = 2
                    LA22_0 = self.input.LA(1)

                    if (LA22_0 in {BOOL, ID, INT, NID}) :
                        alt22 = 1


                    if alt22 == 1:
                        # Parser/ProtoCC.g:249:32: message_expr
                        pass 
                        self._state.following.append(self.FOLLOW_message_expr_in_message_constr2004)
                        message_expr144 = self.message_expr()

                        self._state.following.pop()
                        stream_message_expr.add(message_expr144.tree)



                    else:
                        break #loop22


                # Parser/ProtoCC.g:249:46: ( COMMA message_expr )*
                while True: #loop23
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if (LA23_0 == COMMA) :
                        alt23 = 1


                    if alt23 == 1:
                        # Parser/ProtoCC.g:249:47: COMMA message_expr
                        pass 
                        COMMA145 = self.match(self.input, COMMA, self.FOLLOW_COMMA_in_message_constr2008) 
                        stream_COMMA.add(COMMA145)


                        self._state.following.append(self.FOLLOW_message_expr_in_message_constr2010)
                        message_expr146 = self.message_expr()

                        self._state.following.pop()
                        stream_message_expr.add(message_expr146.tree)



                    else:
                        break #loop23


                CBRACE147 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_message_constr2014) 
                stream_CBRACE.add(CBRACE147)


                # AST Rewrite
                # elements: ID, message_expr
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 249:75: -> ^( MSGCSTR_ ID ( message_expr )* )
                # Parser/ProtoCC.g:249:78: ^( MSGCSTR_ ID ( message_expr )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(MSGCSTR_, "MSGCSTR_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:249:92: ( message_expr )*
                while stream_message_expr.hasNext():
                    self._adaptor.addChild(root_1, stream_message_expr.nextTree())


                stream_message_expr.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "message_constr"


    class message_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "message_expr"
    # Parser/ProtoCC.g:250:5: message_expr : ( object_expr | set_func | INT | BOOL | NID );
    def message_expr(self, ):
        retval = self.message_expr_return()
        retval.start = self.input.LT(1)


        root_0 = None

        INT150 = None
        BOOL151 = None
        NID152 = None
        object_expr148 = None
        set_func149 = None

        INT150_tree = None
        BOOL151_tree = None
        NID152_tree = None

        try:
            try:
                # Parser/ProtoCC.g:250:18: ( object_expr | set_func | INT | BOOL | NID )
                alt24 = 5
                LA24 = self.input.LA(1)
                if LA24 in {ID}:
                    LA24_1 = self.input.LA(2)

                    if (LA24_1 == DOT) :
                        LA24_5 = self.input.LA(3)

                        if (LA24_5 in {ID, NID}) :
                            alt24 = 1
                        elif (LA24_5 in {112, 114, 115, 116, 117, 120}) :
                            alt24 = 2
                        else:
                            nvae = NoViableAltException("", 24, 5, self.input)

                            raise nvae


                    elif (LA24_1 in {BOOL, CBRACE, COMMA, ID, INT, NID}) :
                        alt24 = 1
                    else:
                        nvae = NoViableAltException("", 24, 1, self.input)

                        raise nvae


                elif LA24 in {INT}:
                    alt24 = 3
                elif LA24 in {BOOL}:
                    alt24 = 4
                elif LA24 in {NID}:
                    alt24 = 5
                else:
                    nvae = NoViableAltException("", 24, 0, self.input)

                    raise nvae


                if alt24 == 1:
                    # Parser/ProtoCC.g:250:20: object_expr
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_expr_in_message_expr2036)
                    object_expr148 = self.object_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_expr148.tree)



                elif alt24 == 2:
                    # Parser/ProtoCC.g:250:34: set_func
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_set_func_in_message_expr2040)
                    set_func149 = self.set_func()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_func149.tree)



                elif alt24 == 3:
                    # Parser/ProtoCC.g:250:45: INT
                    pass 
                    root_0 = self._adaptor.nil()


                    INT150 = self.match(self.input, INT, self.FOLLOW_INT_in_message_expr2044)
                    INT150_tree = self._adaptor.createWithPayload(INT150)
                    self._adaptor.addChild(root_0, INT150_tree)




                elif alt24 == 4:
                    # Parser/ProtoCC.g:250:51: BOOL
                    pass 
                    root_0 = self._adaptor.nil()


                    BOOL151 = self.match(self.input, BOOL, self.FOLLOW_BOOL_in_message_expr2048)
                    BOOL151_tree = self._adaptor.createWithPayload(BOOL151)
                    self._adaptor.addChild(root_0, BOOL151_tree)




                elif alt24 == 5:
                    # Parser/ProtoCC.g:250:58: NID
                    pass 
                    root_0 = self._adaptor.nil()


                    NID152 = self.match(self.input, NID, self.FOLLOW_NID_in_message_expr2052)
                    NID152_tree = self._adaptor.createWithPayload(NID152)
                    self._adaptor.addChild(root_0, NID152_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "message_expr"


    class set_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "set_block"
    # Parser/ProtoCC.g:253:5: set_block : set_func SEMICOLON -> set_func ;
    def set_block(self, ):
        retval = self.set_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        SEMICOLON154 = None
        set_func153 = None

        SEMICOLON154_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_set_func = RewriteRuleSubtreeStream(self._adaptor, "rule set_func")
        try:
            try:
                # Parser/ProtoCC.g:253:15: ( set_func SEMICOLON -> set_func )
                # Parser/ProtoCC.g:253:17: set_func SEMICOLON
                pass 
                self._state.following.append(self.FOLLOW_set_func_in_set_block2070)
                set_func153 = self.set_func()

                self._state.following.pop()
                stream_set_func.add(set_func153.tree)


                SEMICOLON154 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_set_block2072) 
                stream_SEMICOLON.add(SEMICOLON154)


                # AST Rewrite
                # elements: set_func
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 253:36: -> set_func
                self._adaptor.addChild(root_0, stream_set_func.nextTree())




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "set_block"


    class set_func_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "set_func"
    # Parser/ProtoCC.g:254:5: set_func : ID DOT set_function_types OBRACE ( set_nest )* CBRACE -> ^( SETFUNC_ ID DOT set_function_types OBRACE ( set_nest )* CBRACE ) ;
    def set_func(self, ):
        retval = self.set_func_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ID155 = None
        DOT156 = None
        OBRACE158 = None
        CBRACE160 = None
        set_function_types157 = None
        set_nest159 = None

        ID155_tree = None
        DOT156_tree = None
        OBRACE158_tree = None
        CBRACE160_tree = None
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_set_function_types = RewriteRuleSubtreeStream(self._adaptor, "rule set_function_types")
        stream_set_nest = RewriteRuleSubtreeStream(self._adaptor, "rule set_nest")
        try:
            try:
                # Parser/ProtoCC.g:254:14: ( ID DOT set_function_types OBRACE ( set_nest )* CBRACE -> ^( SETFUNC_ ID DOT set_function_types OBRACE ( set_nest )* CBRACE ) )
                # Parser/ProtoCC.g:254:16: ID DOT set_function_types OBRACE ( set_nest )* CBRACE
                pass 
                ID155 = self.match(self.input, ID, self.FOLLOW_ID_in_set_func2087) 
                stream_ID.add(ID155)


                DOT156 = self.match(self.input, DOT, self.FOLLOW_DOT_in_set_func2089) 
                stream_DOT.add(DOT156)


                self._state.following.append(self.FOLLOW_set_function_types_in_set_func2091)
                set_function_types157 = self.set_function_types()

                self._state.following.pop()
                stream_set_function_types.add(set_function_types157.tree)


                OBRACE158 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_set_func2093) 
                stream_OBRACE.add(OBRACE158)


                # Parser/ProtoCC.g:254:49: ( set_nest )*
                while True: #loop25
                    alt25 = 2
                    LA25_0 = self.input.LA(1)

                    if (LA25_0 == ID) :
                        alt25 = 1


                    if alt25 == 1:
                        # Parser/ProtoCC.g:254:49: set_nest
                        pass 
                        self._state.following.append(self.FOLLOW_set_nest_in_set_func2095)
                        set_nest159 = self.set_nest()

                        self._state.following.pop()
                        stream_set_nest.add(set_nest159.tree)



                    else:
                        break #loop25


                CBRACE160 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_set_func2098) 
                stream_CBRACE.add(CBRACE160)


                # AST Rewrite
                # elements: ID, DOT, set_function_types, OBRACE, set_nest, CBRACE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 254:66: -> ^( SETFUNC_ ID DOT set_function_types OBRACE ( set_nest )* CBRACE )
                # Parser/ProtoCC.g:255:9: ^( SETFUNC_ ID DOT set_function_types OBRACE ( set_nest )* CBRACE )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(SETFUNC_, "SETFUNC_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, 
                stream_DOT.nextNode()
                )

                self._adaptor.addChild(root_1, stream_set_function_types.nextTree())

                self._adaptor.addChild(root_1, 
                stream_OBRACE.nextNode()
                )

                # Parser/ProtoCC.g:255:53: ( set_nest )*
                while stream_set_nest.hasNext():
                    self._adaptor.addChild(root_1, stream_set_nest.nextTree())


                stream_set_nest.reset();

                self._adaptor.addChild(root_1, 
                stream_CBRACE.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "set_func"


    class set_nest_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "set_nest"
    # Parser/ProtoCC.g:256:5: set_nest : ( set_func | object_expr );
    def set_nest(self, ):
        retval = self.set_nest_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set_func161 = None
        object_expr162 = None


        try:
            try:
                # Parser/ProtoCC.g:256:14: ( set_func | object_expr )
                alt26 = 2
                LA26_0 = self.input.LA(1)

                if (LA26_0 == ID) :
                    LA26_1 = self.input.LA(2)

                    if (LA26_1 == DOT) :
                        LA26_2 = self.input.LA(3)

                        if (LA26_2 in {112, 114, 115, 116, 117, 120}) :
                            alt26 = 1
                        elif (LA26_2 in {ID, NID}) :
                            alt26 = 2
                        else:
                            nvae = NoViableAltException("", 26, 2, self.input)

                            raise nvae


                    elif (LA26_1 in {CBRACE, ID}) :
                        alt26 = 2
                    else:
                        nvae = NoViableAltException("", 26, 1, self.input)

                        raise nvae


                else:
                    nvae = NoViableAltException("", 26, 0, self.input)

                    raise nvae


                if alt26 == 1:
                    # Parser/ProtoCC.g:256:16: set_func
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_set_func_in_set_nest2136)
                    set_func161 = self.set_func()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_func161.tree)



                elif alt26 == 2:
                    # Parser/ProtoCC.g:256:27: object_expr
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_expr_in_set_nest2140)
                    object_expr162 = self.object_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_expr162.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "set_nest"


    class internal_event_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "internal_event_block"
    # Parser/ProtoCC.g:260:5: internal_event_block : internal_event_func SEMICOLON -> internal_event_func ;
    def internal_event_block(self, ):
        retval = self.internal_event_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        SEMICOLON164 = None
        internal_event_func163 = None

        SEMICOLON164_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_internal_event_func = RewriteRuleSubtreeStream(self._adaptor, "rule internal_event_func")
        try:
            try:
                # Parser/ProtoCC.g:260:25: ( internal_event_func SEMICOLON -> internal_event_func )
                # Parser/ProtoCC.g:260:27: internal_event_func SEMICOLON
                pass 
                self._state.following.append(self.FOLLOW_internal_event_func_in_internal_event_block2158)
                internal_event_func163 = self.internal_event_func()

                self._state.following.pop()
                stream_internal_event_func.add(internal_event_func163.tree)


                SEMICOLON164 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_internal_event_block2160) 
                stream_SEMICOLON.add(SEMICOLON164)


                # AST Rewrite
                # elements: internal_event_func
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 260:57: -> internal_event_func
                self._adaptor.addChild(root_0, stream_internal_event_func.nextTree())




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "internal_event_block"


    class internal_event_func_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "internal_event_func"
    # Parser/ProtoCC.g:261:5: internal_event_func : internal_event_function OBRACE ID CBRACE -> ^( EVENT_ ID ) ^( EVENT_ACK_ ID ) ;
    def internal_event_func(self, ):
        retval = self.internal_event_func_return()
        retval.start = self.input.LT(1)


        root_0 = None

        OBRACE166 = None
        ID167 = None
        CBRACE168 = None
        internal_event_function165 = None

        OBRACE166_tree = None
        ID167_tree = None
        CBRACE168_tree = None
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_internal_event_function = RewriteRuleSubtreeStream(self._adaptor, "rule internal_event_function")
        try:
            try:
                # Parser/ProtoCC.g:261:24: ( internal_event_function OBRACE ID CBRACE -> ^( EVENT_ ID ) ^( EVENT_ACK_ ID ) )
                # Parser/ProtoCC.g:261:26: internal_event_function OBRACE ID CBRACE
                pass 
                self._state.following.append(self.FOLLOW_internal_event_function_in_internal_event_func2174)
                internal_event_function165 = self.internal_event_function()

                self._state.following.pop()
                stream_internal_event_function.add(internal_event_function165.tree)


                OBRACE166 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_internal_event_func2176) 
                stream_OBRACE.add(OBRACE166)


                ID167 = self.match(self.input, ID, self.FOLLOW_ID_in_internal_event_func2178) 
                stream_ID.add(ID167)


                CBRACE168 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_internal_event_func2180) 
                stream_CBRACE.add(CBRACE168)


                # AST Rewrite
                # elements: ID, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 261:67: -> ^( EVENT_ ID ) ^( EVENT_ACK_ ID )
                # Parser/ProtoCC.g:261:70: ^( EVENT_ ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(EVENT_, "EVENT_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)

                # Parser/ProtoCC.g:261:83: ^( EVENT_ACK_ ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(EVENT_ACK_, "EVENT_ACK_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "internal_event_func"


    class arch_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "arch_block"
    # Parser/ProtoCC.g:264:1: arch_block : ARCH ID OCBRACE arch_body CCBRACE -> ^( ARCH_ ^( MACHN_ ID ) arch_body ) ;
    def arch_block(self, ):
        retval = self.arch_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ARCH169 = None
        ID170 = None
        OCBRACE171 = None
        CCBRACE173 = None
        arch_body172 = None

        ARCH169_tree = None
        ID170_tree = None
        OCBRACE171_tree = None
        CCBRACE173_tree = None
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_ARCH = RewriteRuleTokenStream(self._adaptor, "token ARCH")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_arch_body = RewriteRuleSubtreeStream(self._adaptor, "rule arch_body")
        try:
            try:
                # Parser/ProtoCC.g:264:12: ( ARCH ID OCBRACE arch_body CCBRACE -> ^( ARCH_ ^( MACHN_ ID ) arch_body ) )
                # Parser/ProtoCC.g:264:14: ARCH ID OCBRACE arch_body CCBRACE
                pass 
                ARCH169 = self.match(self.input, ARCH, self.FOLLOW_ARCH_in_arch_block2204) 
                stream_ARCH.add(ARCH169)


                ID170 = self.match(self.input, ID, self.FOLLOW_ID_in_arch_block2206) 
                stream_ID.add(ID170)


                OCBRACE171 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_arch_block2208) 
                stream_OCBRACE.add(OCBRACE171)


                self._state.following.append(self.FOLLOW_arch_body_in_arch_block2210)
                arch_body172 = self.arch_body()

                self._state.following.pop()
                stream_arch_body.add(arch_body172.tree)


                CCBRACE173 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_arch_block2212) 
                stream_CCBRACE.add(CCBRACE173)


                # AST Rewrite
                # elements: ID, arch_body
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 264:48: -> ^( ARCH_ ^( MACHN_ ID ) arch_body )
                # Parser/ProtoCC.g:264:51: ^( ARCH_ ^( MACHN_ ID ) arch_body )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(ARCH_, "ARCH_")
                , root_1)

                # Parser/ProtoCC.g:264:59: ^( MACHN_ ID )
                root_2 = self._adaptor.nil()
                root_2 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(MACHN_, "MACHN_")
                , root_2)

                self._adaptor.addChild(root_2, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, root_2)

                self._adaptor.addChild(root_1, stream_arch_body.nextTree())

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "arch_block"


    class arch_body_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "arch_body"
    # Parser/ProtoCC.g:266:1: arch_body : ( stable_def | process_block )* ;
    def arch_body(self, ):
        retval = self.arch_body_return()
        retval.start = self.input.LT(1)


        root_0 = None

        stable_def174 = None
        process_block175 = None


        try:
            try:
                # Parser/ProtoCC.g:266:10: ( ( stable_def | process_block )* )
                # Parser/ProtoCC.g:266:12: ( stable_def | process_block )*
                pass 
                root_0 = self._adaptor.nil()


                # Parser/ProtoCC.g:266:12: ( stable_def | process_block )*
                while True: #loop27
                    alt27 = 3
                    LA27_0 = self.input.LA(1)

                    if (LA27_0 == STABLE) :
                        alt27 = 1
                    elif (LA27_0 == PROC) :
                        alt27 = 2


                    if alt27 == 1:
                        # Parser/ProtoCC.g:266:13: stable_def
                        pass 
                        self._state.following.append(self.FOLLOW_stable_def_in_arch_body2234)
                        stable_def174 = self.stable_def()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, stable_def174.tree)



                    elif alt27 == 2:
                        # Parser/ProtoCC.g:266:26: process_block
                        pass 
                        self._state.following.append(self.FOLLOW_process_block_in_arch_body2238)
                        process_block175 = self.process_block()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, process_block175.tree)



                    else:
                        break #loop27




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "arch_body"


    class stable_def_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "stable_def"
    # Parser/ProtoCC.g:268:1: stable_def : STABLE OCBRACE ID ( COMMA ID )* CCBRACE -> ^( STABLE_ ID ( ID )* ) ;
    def stable_def(self, ):
        retval = self.stable_def_return()
        retval.start = self.input.LT(1)


        root_0 = None

        STABLE176 = None
        OCBRACE177 = None
        ID178 = None
        COMMA179 = None
        ID180 = None
        CCBRACE181 = None

        STABLE176_tree = None
        OCBRACE177_tree = None
        ID178_tree = None
        COMMA179_tree = None
        ID180_tree = None
        CCBRACE181_tree = None
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_STABLE = RewriteRuleTokenStream(self._adaptor, "token STABLE")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")

        try:
            try:
                # Parser/ProtoCC.g:268:12: ( STABLE OCBRACE ID ( COMMA ID )* CCBRACE -> ^( STABLE_ ID ( ID )* ) )
                # Parser/ProtoCC.g:268:14: STABLE OCBRACE ID ( COMMA ID )* CCBRACE
                pass 
                STABLE176 = self.match(self.input, STABLE, self.FOLLOW_STABLE_in_stable_def2248) 
                stream_STABLE.add(STABLE176)


                OCBRACE177 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_stable_def2250) 
                stream_OCBRACE.add(OCBRACE177)


                ID178 = self.match(self.input, ID, self.FOLLOW_ID_in_stable_def2252) 
                stream_ID.add(ID178)


                # Parser/ProtoCC.g:268:32: ( COMMA ID )*
                while True: #loop28
                    alt28 = 2
                    LA28_0 = self.input.LA(1)

                    if (LA28_0 == COMMA) :
                        alt28 = 1


                    if alt28 == 1:
                        # Parser/ProtoCC.g:268:33: COMMA ID
                        pass 
                        COMMA179 = self.match(self.input, COMMA, self.FOLLOW_COMMA_in_stable_def2255) 
                        stream_COMMA.add(COMMA179)


                        ID180 = self.match(self.input, ID, self.FOLLOW_ID_in_stable_def2257) 
                        stream_ID.add(ID180)



                    else:
                        break #loop28


                CCBRACE181 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_stable_def2261) 
                stream_CCBRACE.add(CCBRACE181)


                # AST Rewrite
                # elements: ID, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 268:52: -> ^( STABLE_ ID ( ID )* )
                # Parser/ProtoCC.g:268:55: ^( STABLE_ ID ( ID )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(STABLE_, "STABLE_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                # Parser/ProtoCC.g:268:68: ( ID )*
                while stream_ID.hasNext():
                    self._adaptor.addChild(root_1, 
                    stream_ID.nextNode()
                    )


                stream_ID.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "stable_def"


    class process_block_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "process_block"
    # Parser/ProtoCC.g:270:1: process_block : PROC process_trans OCBRACE ( process_expr )* CCBRACE -> ^( PROC_ process_trans ( process_expr )* ^( ENDPROC_ ) ) ;
    def process_block(self, ):
        retval = self.process_block_return()
        retval.start = self.input.LT(1)


        root_0 = None

        PROC182 = None
        OCBRACE184 = None
        CCBRACE186 = None
        process_trans183 = None
        process_expr185 = None

        PROC182_tree = None
        OCBRACE184_tree = None
        CCBRACE186_tree = None
        stream_PROC = RewriteRuleTokenStream(self._adaptor, "token PROC")
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_process_trans = RewriteRuleSubtreeStream(self._adaptor, "rule process_trans")
        stream_process_expr = RewriteRuleSubtreeStream(self._adaptor, "rule process_expr")
        try:
            try:
                # Parser/ProtoCC.g:270:15: ( PROC process_trans OCBRACE ( process_expr )* CCBRACE -> ^( PROC_ process_trans ( process_expr )* ^( ENDPROC_ ) ) )
                # Parser/ProtoCC.g:270:17: PROC process_trans OCBRACE ( process_expr )* CCBRACE
                pass 
                PROC182 = self.match(self.input, PROC, self.FOLLOW_PROC_in_process_block2280) 
                stream_PROC.add(PROC182)


                self._state.following.append(self.FOLLOW_process_trans_in_process_block2282)
                process_trans183 = self.process_trans()

                self._state.following.pop()
                stream_process_trans.add(process_trans183.tree)


                OCBRACE184 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_process_block2284) 
                stream_OCBRACE.add(OCBRACE184)


                # Parser/ProtoCC.g:270:44: ( process_expr )*
                while True: #loop29
                    alt29 = 2
                    LA29_0 = self.input.LA(1)

                    if (LA29_0 in {ACCESS, AWAIT, ID, IF, STALL, STATE, UNDEF, 107}) :
                        alt29 = 1


                    if alt29 == 1:
                        # Parser/ProtoCC.g:270:44: process_expr
                        pass 
                        self._state.following.append(self.FOLLOW_process_expr_in_process_block2286)
                        process_expr185 = self.process_expr()

                        self._state.following.pop()
                        stream_process_expr.add(process_expr185.tree)



                    else:
                        break #loop29


                CCBRACE186 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_process_block2289) 
                stream_CCBRACE.add(CCBRACE186)


                # AST Rewrite
                # elements: process_trans, process_expr
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 270:66: -> ^( PROC_ process_trans ( process_expr )* ^( ENDPROC_ ) )
                # Parser/ProtoCC.g:270:69: ^( PROC_ process_trans ( process_expr )* ^( ENDPROC_ ) )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(PROC_, "PROC_")
                , root_1)

                self._adaptor.addChild(root_1, stream_process_trans.nextTree())

                # Parser/ProtoCC.g:270:91: ( process_expr )*
                while stream_process_expr.hasNext():
                    self._adaptor.addChild(root_1, stream_process_expr.nextTree())


                stream_process_expr.reset();

                # Parser/ProtoCC.g:270:105: ^( ENDPROC_ )
                root_2 = self._adaptor.nil()
                root_2 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(ENDPROC_, "ENDPROC_")
                , root_2)

                self._adaptor.addChild(root_1, root_2)

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "process_block"


    class process_trans_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "process_trans"
    # Parser/ProtoCC.g:271:5: process_trans : OBRACE ID COMMA process_events ( process_finalstate )* CBRACE -> ^( TRANS_ ID process_events ( process_finalstate )* ) ;
    def process_trans(self, ):
        retval = self.process_trans_return()
        retval.start = self.input.LT(1)


        root_0 = None

        OBRACE187 = None
        ID188 = None
        COMMA189 = None
        CBRACE192 = None
        process_events190 = None
        process_finalstate191 = None

        OBRACE187_tree = None
        ID188_tree = None
        COMMA189_tree = None
        CBRACE192_tree = None
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_process_events = RewriteRuleSubtreeStream(self._adaptor, "rule process_events")
        stream_process_finalstate = RewriteRuleSubtreeStream(self._adaptor, "rule process_finalstate")
        try:
            try:
                # Parser/ProtoCC.g:271:19: ( OBRACE ID COMMA process_events ( process_finalstate )* CBRACE -> ^( TRANS_ ID process_events ( process_finalstate )* ) )
                # Parser/ProtoCC.g:271:21: OBRACE ID COMMA process_events ( process_finalstate )* CBRACE
                pass 
                OBRACE187 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_process_trans2315) 
                stream_OBRACE.add(OBRACE187)


                ID188 = self.match(self.input, ID, self.FOLLOW_ID_in_process_trans2317) 
                stream_ID.add(ID188)


                COMMA189 = self.match(self.input, COMMA, self.FOLLOW_COMMA_in_process_trans2319) 
                stream_COMMA.add(COMMA189)


                self._state.following.append(self.FOLLOW_process_events_in_process_trans2321)
                process_events190 = self.process_events()

                self._state.following.pop()
                stream_process_events.add(process_events190.tree)


                # Parser/ProtoCC.g:271:52: ( process_finalstate )*
                while True: #loop30
                    alt30 = 2
                    LA30_0 = self.input.LA(1)

                    if (LA30_0 == COMMA) :
                        alt30 = 1


                    if alt30 == 1:
                        # Parser/ProtoCC.g:271:52: process_finalstate
                        pass 
                        self._state.following.append(self.FOLLOW_process_finalstate_in_process_trans2323)
                        process_finalstate191 = self.process_finalstate()

                        self._state.following.pop()
                        stream_process_finalstate.add(process_finalstate191.tree)



                    else:
                        break #loop30


                CBRACE192 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_process_trans2326) 
                stream_CBRACE.add(CBRACE192)


                # AST Rewrite
                # elements: ID, process_events, process_finalstate
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 271:79: -> ^( TRANS_ ID process_events ( process_finalstate )* )
                # Parser/ProtoCC.g:271:82: ^( TRANS_ ID process_events ( process_finalstate )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(TRANS_, "TRANS_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, stream_process_events.nextTree())

                # Parser/ProtoCC.g:271:109: ( process_finalstate )*
                while stream_process_finalstate.hasNext():
                    self._adaptor.addChild(root_1, stream_process_finalstate.nextTree())


                stream_process_finalstate.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "process_trans"


    class process_finalstate_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "process_finalstate"
    # Parser/ProtoCC.g:272:5: process_finalstate : COMMA process_finalident -> ^( process_finalident ) ;
    def process_finalstate(self, ):
        retval = self.process_finalstate_return()
        retval.start = self.input.LT(1)


        root_0 = None

        COMMA193 = None
        process_finalident194 = None

        COMMA193_tree = None
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_process_finalident = RewriteRuleSubtreeStream(self._adaptor, "rule process_finalident")
        try:
            try:
                # Parser/ProtoCC.g:272:23: ( COMMA process_finalident -> ^( process_finalident ) )
                # Parser/ProtoCC.g:272:25: COMMA process_finalident
                pass 
                COMMA193 = self.match(self.input, COMMA, self.FOLLOW_COMMA_in_process_finalstate2349) 
                stream_COMMA.add(COMMA193)


                self._state.following.append(self.FOLLOW_process_finalident_in_process_finalstate2351)
                process_finalident194 = self.process_finalident()

                self._state.following.pop()
                stream_process_finalident.add(process_finalident194.tree)


                # AST Rewrite
                # elements: process_finalident
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 272:50: -> ^( process_finalident )
                # Parser/ProtoCC.g:272:53: ^( process_finalident )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(stream_process_finalident.nextNode(), root_1)

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "process_finalstate"


    class process_finalident_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "process_finalident"
    # Parser/ProtoCC.g:273:5: process_finalident : ( ID | STATE ) ;
    def process_finalident(self, ):
        retval = self.process_finalident_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set195 = None

        set195_tree = None

        try:
            try:
                # Parser/ProtoCC.g:273:23: ( ( ID | STATE ) )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set195 = self.input.LT(1)

                if self.input.LA(1) in {ID, STATE}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set195))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "process_finalident"


    class process_events_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "process_events"
    # Parser/ProtoCC.g:274:5: process_events : ( ACCESS | EVICT | ID ) ;
    def process_events(self, ):
        retval = self.process_events_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set196 = None

        set196_tree = None

        try:
            try:
                # Parser/ProtoCC.g:274:20: ( ( ACCESS | EVICT | ID ) )
                # Parser/ProtoCC.g:
                pass 
                root_0 = self._adaptor.nil()


                set196 = self.input.LT(1)

                if self.input.LA(1) in {ACCESS, EVICT, ID}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set196))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "process_events"


    class process_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "process_expr"
    # Parser/ProtoCC.g:275:5: process_expr : ( expressions | network_send | network_mcast | network_bcast | transaction );
    def process_expr(self, ):
        retval = self.process_expr_return()
        retval.start = self.input.LT(1)


        root_0 = None

        expressions197 = None
        network_send198 = None
        network_mcast199 = None
        network_bcast200 = None
        transaction201 = None


        try:
            try:
                # Parser/ProtoCC.g:275:17: ( expressions | network_send | network_mcast | network_bcast | transaction )
                alt31 = 5
                LA31 = self.input.LA(1)
                if LA31 in {ID}:
                    LA31_1 = self.input.LA(2)

                    if (LA31_1 == DOT) :
                        LA31 = self.input.LA(3)
                        if LA31 in {ID, NID, 112, 114, 115, 116, 117, 120}:
                            alt31 = 1
                        elif LA31 in {110, 119}:
                            alt31 = 2
                        elif LA31 in {108, 118}:
                            alt31 = 3
                        elif LA31 in {106, 113}:
                            alt31 = 4
                        else:
                            nvae = NoViableAltException("", 31, 9, self.input)

                            raise nvae


                    elif (LA31_1 in {EQUALSIGN, SEMICOLON}) :
                        alt31 = 1
                    else:
                        nvae = NoViableAltException("", 31, 1, self.input)

                        raise nvae


                elif LA31 in {ACCESS, IF, STALL, STATE, UNDEF, 107}:
                    alt31 = 1
                elif LA31 in {AWAIT}:
                    alt31 = 5
                else:
                    nvae = NoViableAltException("", 31, 0, self.input)

                    raise nvae


                if alt31 == 1:
                    # Parser/ProtoCC.g:275:19: expressions
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_expressions_in_process_expr2404)
                    expressions197 = self.expressions()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expressions197.tree)



                elif alt31 == 2:
                    # Parser/ProtoCC.g:275:33: network_send
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_send_in_process_expr2408)
                    network_send198 = self.network_send()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_send198.tree)



                elif alt31 == 3:
                    # Parser/ProtoCC.g:275:48: network_mcast
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_mcast_in_process_expr2412)
                    network_mcast199 = self.network_mcast()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_mcast199.tree)



                elif alt31 == 4:
                    # Parser/ProtoCC.g:275:64: network_bcast
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_bcast_in_process_expr2416)
                    network_bcast200 = self.network_bcast()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_bcast200.tree)



                elif alt31 == 5:
                    # Parser/ProtoCC.g:275:79: transaction
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_transaction_in_process_expr2419)
                    transaction201 = self.transaction()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, transaction201.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "process_expr"


    class transaction_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "transaction"
    # Parser/ProtoCC.g:278:1: transaction : AWAIT OCBRACE ( trans )* CCBRACE -> ^( AWAIT_ ( trans )* ) ;
    def transaction(self, ):
        retval = self.transaction_return()
        retval.start = self.input.LT(1)


        root_0 = None

        AWAIT202 = None
        OCBRACE203 = None
        CCBRACE205 = None
        trans204 = None

        AWAIT202_tree = None
        OCBRACE203_tree = None
        CCBRACE205_tree = None
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_AWAIT = RewriteRuleTokenStream(self._adaptor, "token AWAIT")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_trans = RewriteRuleSubtreeStream(self._adaptor, "rule trans")
        try:
            try:
                # Parser/ProtoCC.g:278:13: ( AWAIT OCBRACE ( trans )* CCBRACE -> ^( AWAIT_ ( trans )* ) )
                # Parser/ProtoCC.g:278:15: AWAIT OCBRACE ( trans )* CCBRACE
                pass 
                AWAIT202 = self.match(self.input, AWAIT, self.FOLLOW_AWAIT_in_transaction2429) 
                stream_AWAIT.add(AWAIT202)


                OCBRACE203 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_transaction2431) 
                stream_OCBRACE.add(OCBRACE203)


                # Parser/ProtoCC.g:278:29: ( trans )*
                while True: #loop32
                    alt32 = 2
                    LA32_0 = self.input.LA(1)

                    if (LA32_0 == WHEN) :
                        alt32 = 1


                    if alt32 == 1:
                        # Parser/ProtoCC.g:278:29: trans
                        pass 
                        self._state.following.append(self.FOLLOW_trans_in_transaction2433)
                        trans204 = self.trans()

                        self._state.following.pop()
                        stream_trans.add(trans204.tree)



                    else:
                        break #loop32


                CCBRACE205 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_transaction2436) 
                stream_CCBRACE.add(CCBRACE205)


                # AST Rewrite
                # elements: trans
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 278:44: -> ^( AWAIT_ ( trans )* )
                # Parser/ProtoCC.g:278:47: ^( AWAIT_ ( trans )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(AWAIT_, "AWAIT_")
                , root_1)

                # Parser/ProtoCC.g:278:56: ( trans )*
                while stream_trans.hasNext():
                    self._adaptor.addChild(root_1, stream_trans.nextTree())


                stream_trans.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "transaction"


    class trans_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "trans"
    # Parser/ProtoCC.g:279:5: trans : WHEN ID DDOT ( trans_body )* -> ^( WHEN_ ^( GUARD_ ID ) ( trans_body )* ENDWHEN_ ) ;
    def trans(self, ):
        retval = self.trans_return()
        retval.start = self.input.LT(1)


        root_0 = None

        WHEN206 = None
        ID207 = None
        DDOT208 = None
        trans_body209 = None

        WHEN206_tree = None
        ID207_tree = None
        DDOT208_tree = None
        stream_WHEN = RewriteRuleTokenStream(self._adaptor, "token WHEN")
        stream_DDOT = RewriteRuleTokenStream(self._adaptor, "token DDOT")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_trans_body = RewriteRuleSubtreeStream(self._adaptor, "rule trans_body")
        try:
            try:
                # Parser/ProtoCC.g:279:11: ( WHEN ID DDOT ( trans_body )* -> ^( WHEN_ ^( GUARD_ ID ) ( trans_body )* ENDWHEN_ ) )
                # Parser/ProtoCC.g:279:13: WHEN ID DDOT ( trans_body )*
                pass 
                WHEN206 = self.match(self.input, WHEN, self.FOLLOW_WHEN_in_trans2456) 
                stream_WHEN.add(WHEN206)


                ID207 = self.match(self.input, ID, self.FOLLOW_ID_in_trans2458) 
                stream_ID.add(ID207)


                DDOT208 = self.match(self.input, DDOT, self.FOLLOW_DDOT_in_trans2460) 
                stream_DDOT.add(DDOT208)


                # Parser/ProtoCC.g:279:26: ( trans_body )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 in {ACCESS, AWAIT, BREAK, ID, IF, NEXT, STALL, STATE, UNDEF, 107}) :
                        alt33 = 1


                    if alt33 == 1:
                        # Parser/ProtoCC.g:279:26: trans_body
                        pass 
                        self._state.following.append(self.FOLLOW_trans_body_in_trans2462)
                        trans_body209 = self.trans_body()

                        self._state.following.pop()
                        stream_trans_body.add(trans_body209.tree)



                    else:
                        break #loop33


                # AST Rewrite
                # elements: ID, trans_body
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 279:38: -> ^( WHEN_ ^( GUARD_ ID ) ( trans_body )* ENDWHEN_ )
                # Parser/ProtoCC.g:279:41: ^( WHEN_ ^( GUARD_ ID ) ( trans_body )* ENDWHEN_ )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(WHEN_, "WHEN_")
                , root_1)

                # Parser/ProtoCC.g:279:49: ^( GUARD_ ID )
                root_2 = self._adaptor.nil()
                root_2 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(GUARD_, "GUARD_")
                , root_2)

                self._adaptor.addChild(root_2, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_1, root_2)

                # Parser/ProtoCC.g:279:62: ( trans_body )*
                while stream_trans_body.hasNext():
                    self._adaptor.addChild(root_1, stream_trans_body.nextTree())


                stream_trans_body.reset();

                self._adaptor.addChild(root_1, 
                self._adaptor.createFromType(ENDWHEN_, "ENDWHEN_")
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "trans"


    class trans_body_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "trans_body"
    # Parser/ProtoCC.g:280:9: trans_body : ( expressions | next_trans | next_break | transaction | network_send | network_mcast | network_bcast );
    def trans_body(self, ):
        retval = self.trans_body_return()
        retval.start = self.input.LT(1)


        root_0 = None

        expressions210 = None
        next_trans211 = None
        next_break212 = None
        transaction213 = None
        network_send214 = None
        network_mcast215 = None
        network_bcast216 = None


        try:
            try:
                # Parser/ProtoCC.g:280:20: ( expressions | next_trans | next_break | transaction | network_send | network_mcast | network_bcast )
                alt34 = 7
                LA34 = self.input.LA(1)
                if LA34 in {ID}:
                    LA34_1 = self.input.LA(2)

                    if (LA34_1 == DOT) :
                        LA34 = self.input.LA(3)
                        if LA34 in {ID, NID, 112, 114, 115, 116, 117, 120}:
                            alt34 = 1
                        elif LA34 in {110, 119}:
                            alt34 = 5
                        elif LA34 in {108, 118}:
                            alt34 = 6
                        elif LA34 in {106, 113}:
                            alt34 = 7
                        else:
                            nvae = NoViableAltException("", 34, 11, self.input)

                            raise nvae


                    elif (LA34_1 in {EQUALSIGN, SEMICOLON}) :
                        alt34 = 1
                    else:
                        nvae = NoViableAltException("", 34, 1, self.input)

                        raise nvae


                elif LA34 in {ACCESS, IF, STALL, STATE, UNDEF, 107}:
                    alt34 = 1
                elif LA34 in {NEXT}:
                    alt34 = 2
                elif LA34 in {BREAK}:
                    alt34 = 3
                elif LA34 in {AWAIT}:
                    alt34 = 4
                else:
                    nvae = NoViableAltException("", 34, 0, self.input)

                    raise nvae


                if alt34 == 1:
                    # Parser/ProtoCC.g:280:22: expressions
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_expressions_in_trans_body2495)
                    expressions210 = self.expressions()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expressions210.tree)



                elif alt34 == 2:
                    # Parser/ProtoCC.g:280:36: next_trans
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_next_trans_in_trans_body2499)
                    next_trans211 = self.next_trans()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, next_trans211.tree)



                elif alt34 == 3:
                    # Parser/ProtoCC.g:280:49: next_break
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_next_break_in_trans_body2503)
                    next_break212 = self.next_break()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, next_break212.tree)



                elif alt34 == 4:
                    # Parser/ProtoCC.g:280:62: transaction
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_transaction_in_trans_body2507)
                    transaction213 = self.transaction()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, transaction213.tree)



                elif alt34 == 5:
                    # Parser/ProtoCC.g:280:76: network_send
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_send_in_trans_body2511)
                    network_send214 = self.network_send()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_send214.tree)



                elif alt34 == 6:
                    # Parser/ProtoCC.g:280:91: network_mcast
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_mcast_in_trans_body2515)
                    network_mcast215 = self.network_mcast()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_mcast215.tree)



                elif alt34 == 7:
                    # Parser/ProtoCC.g:280:107: network_bcast
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_bcast_in_trans_body2519)
                    network_bcast216 = self.network_bcast()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_bcast216.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "trans_body"


    class next_trans_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "next_trans"
    # Parser/ProtoCC.g:281:13: next_trans : NEXT OCBRACE ( trans )* CCBRACE -> ^( NEXT_ ( trans )* ) ;
    def next_trans(self, ):
        retval = self.next_trans_return()
        retval.start = self.input.LT(1)


        root_0 = None

        NEXT217 = None
        OCBRACE218 = None
        CCBRACE220 = None
        trans219 = None

        NEXT217_tree = None
        OCBRACE218_tree = None
        CCBRACE220_tree = None
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_NEXT = RewriteRuleTokenStream(self._adaptor, "token NEXT")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_trans = RewriteRuleSubtreeStream(self._adaptor, "rule trans")
        try:
            try:
                # Parser/ProtoCC.g:281:23: ( NEXT OCBRACE ( trans )* CCBRACE -> ^( NEXT_ ( trans )* ) )
                # Parser/ProtoCC.g:281:25: NEXT OCBRACE ( trans )* CCBRACE
                pass 
                NEXT217 = self.match(self.input, NEXT, self.FOLLOW_NEXT_in_next_trans2537) 
                stream_NEXT.add(NEXT217)


                OCBRACE218 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_next_trans2539) 
                stream_OCBRACE.add(OCBRACE218)


                # Parser/ProtoCC.g:281:38: ( trans )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == WHEN) :
                        alt35 = 1


                    if alt35 == 1:
                        # Parser/ProtoCC.g:281:38: trans
                        pass 
                        self._state.following.append(self.FOLLOW_trans_in_next_trans2541)
                        trans219 = self.trans()

                        self._state.following.pop()
                        stream_trans.add(trans219.tree)



                    else:
                        break #loop35


                CCBRACE220 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_next_trans2544) 
                stream_CCBRACE.add(CCBRACE220)


                # AST Rewrite
                # elements: trans
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 281:53: -> ^( NEXT_ ( trans )* )
                # Parser/ProtoCC.g:281:56: ^( NEXT_ ( trans )* )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(NEXT_, "NEXT_")
                , root_1)

                # Parser/ProtoCC.g:281:64: ( trans )*
                while stream_trans.hasNext():
                    self._adaptor.addChild(root_1, stream_trans.nextTree())


                stream_trans.reset();

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "next_trans"


    class next_break_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "next_break"
    # Parser/ProtoCC.g:283:5: next_break : BREAK SEMICOLON -> ^( BREAK_ ) ;
    def next_break(self, ):
        retval = self.next_break_return()
        retval.start = self.input.LT(1)


        root_0 = None

        BREAK221 = None
        SEMICOLON222 = None

        BREAK221_tree = None
        SEMICOLON222_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_BREAK = RewriteRuleTokenStream(self._adaptor, "token BREAK")

        try:
            try:
                # Parser/ProtoCC.g:283:16: ( BREAK SEMICOLON -> ^( BREAK_ ) )
                # Parser/ProtoCC.g:283:18: BREAK SEMICOLON
                pass 
                BREAK221 = self.match(self.input, BREAK, self.FOLLOW_BREAK_in_next_break2565) 
                stream_BREAK.add(BREAK221)


                SEMICOLON222 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_next_break2567) 
                stream_SEMICOLON.add(SEMICOLON222)


                # AST Rewrite
                # elements: 
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 283:34: -> ^( BREAK_ )
                # Parser/ProtoCC.g:283:37: ^( BREAK_ )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(BREAK_, "BREAK_")
                , root_1)

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "next_break"


    class expressions_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "expressions"
    # Parser/ProtoCC.g:286:1: expressions : ( assignment | conditional | object_block | set_block | internal_event_block | msg_stall | set_access | undefine );
    def expressions(self, ):
        retval = self.expressions_return()
        retval.start = self.input.LT(1)


        root_0 = None

        assignment223 = None
        conditional224 = None
        object_block225 = None
        set_block226 = None
        internal_event_block227 = None
        msg_stall228 = None
        set_access229 = None
        undefine230 = None


        try:
            try:
                # Parser/ProtoCC.g:286:13: ( assignment | conditional | object_block | set_block | internal_event_block | msg_stall | set_access | undefine )
                alt36 = 8
                LA36 = self.input.LA(1)
                if LA36 in {ID}:
                    LA36 = self.input.LA(2)
                    if LA36 in {DOT}:
                        LA36_8 = self.input.LA(3)

                        if (LA36_8 in {ID, NID}) :
                            alt36 = 3
                        elif (LA36_8 in {112, 114, 115, 116, 117, 120}) :
                            alt36 = 4
                        else:
                            nvae = NoViableAltException("", 36, 8, self.input)

                            raise nvae


                    elif LA36 in {EQUALSIGN}:
                        alt36 = 1
                    elif LA36 in {SEMICOLON}:
                        alt36 = 3
                    else:
                        nvae = NoViableAltException("", 36, 1, self.input)

                        raise nvae


                elif LA36 in {IF}:
                    alt36 = 2
                elif LA36 in {STATE}:
                    alt36 = 1
                elif LA36 in {107}:
                    alt36 = 5
                elif LA36 in {STALL}:
                    alt36 = 6
                elif LA36 in {ACCESS}:
                    alt36 = 7
                elif LA36 in {UNDEF}:
                    alt36 = 8
                else:
                    nvae = NoViableAltException("", 36, 0, self.input)

                    raise nvae


                if alt36 == 1:
                    # Parser/ProtoCC.g:286:15: assignment
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_assignment_in_expressions2583)
                    assignment223 = self.assignment()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, assignment223.tree)



                elif alt36 == 2:
                    # Parser/ProtoCC.g:286:28: conditional
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_conditional_in_expressions2587)
                    conditional224 = self.conditional()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, conditional224.tree)



                elif alt36 == 3:
                    # Parser/ProtoCC.g:286:42: object_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_block_in_expressions2591)
                    object_block225 = self.object_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_block225.tree)



                elif alt36 == 4:
                    # Parser/ProtoCC.g:286:57: set_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_set_block_in_expressions2595)
                    set_block226 = self.set_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_block226.tree)



                elif alt36 == 5:
                    # Parser/ProtoCC.g:286:69: internal_event_block
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_internal_event_block_in_expressions2599)
                    internal_event_block227 = self.internal_event_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, internal_event_block227.tree)



                elif alt36 == 6:
                    # Parser/ProtoCC.g:286:92: msg_stall
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_msg_stall_in_expressions2603)
                    msg_stall228 = self.msg_stall()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, msg_stall228.tree)



                elif alt36 == 7:
                    # Parser/ProtoCC.g:286:104: set_access
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_set_access_in_expressions2607)
                    set_access229 = self.set_access()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_access229.tree)



                elif alt36 == 8:
                    # Parser/ProtoCC.g:286:117: undefine
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_undefine_in_expressions2611)
                    undefine230 = self.undefine()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, undefine230.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "expressions"


    class assignment_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "assignment"
    # Parser/ProtoCC.g:287:1: assignment : process_finalident EQUALSIGN assign_types SEMICOLON -> ^( ASSIGN_ process_finalident EQUALSIGN assign_types ) ;
    def assignment(self, ):
        retval = self.assignment_return()
        retval.start = self.input.LT(1)


        root_0 = None

        EQUALSIGN232 = None
        SEMICOLON234 = None
        process_finalident231 = None
        assign_types233 = None

        EQUALSIGN232_tree = None
        SEMICOLON234_tree = None
        stream_EQUALSIGN = RewriteRuleTokenStream(self._adaptor, "token EQUALSIGN")
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_assign_types = RewriteRuleSubtreeStream(self._adaptor, "rule assign_types")
        stream_process_finalident = RewriteRuleSubtreeStream(self._adaptor, "rule process_finalident")
        try:
            try:
                # Parser/ProtoCC.g:287:12: ( process_finalident EQUALSIGN assign_types SEMICOLON -> ^( ASSIGN_ process_finalident EQUALSIGN assign_types ) )
                # Parser/ProtoCC.g:287:14: process_finalident EQUALSIGN assign_types SEMICOLON
                pass 
                self._state.following.append(self.FOLLOW_process_finalident_in_assignment2618)
                process_finalident231 = self.process_finalident()

                self._state.following.pop()
                stream_process_finalident.add(process_finalident231.tree)


                EQUALSIGN232 = self.match(self.input, EQUALSIGN, self.FOLLOW_EQUALSIGN_in_assignment2620) 
                stream_EQUALSIGN.add(EQUALSIGN232)


                self._state.following.append(self.FOLLOW_assign_types_in_assignment2622)
                assign_types233 = self.assign_types()

                self._state.following.pop()
                stream_assign_types.add(assign_types233.tree)


                SEMICOLON234 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_assignment2624) 
                stream_SEMICOLON.add(SEMICOLON234)


                # AST Rewrite
                # elements: process_finalident, EQUALSIGN, assign_types
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 287:65: -> ^( ASSIGN_ process_finalident EQUALSIGN assign_types )
                # Parser/ProtoCC.g:287:68: ^( ASSIGN_ process_finalident EQUALSIGN assign_types )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(ASSIGN_, "ASSIGN_")
                , root_1)

                self._adaptor.addChild(root_1, stream_process_finalident.nextTree())

                self._adaptor.addChild(root_1, 
                stream_EQUALSIGN.nextNode()
                )

                self._adaptor.addChild(root_1, stream_assign_types.nextTree())

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "assignment"


    class assign_types_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "assign_types"
    # Parser/ProtoCC.g:288:5: assign_types : ( object_expr | message_constr | math_op | set_func | INT | BOOL | NID );
    def assign_types(self, ):
        retval = self.assign_types_return()
        retval.start = self.input.LT(1)


        root_0 = None

        INT239 = None
        BOOL240 = None
        NID241 = None
        object_expr235 = None
        message_constr236 = None
        math_op237 = None
        set_func238 = None

        INT239_tree = None
        BOOL240_tree = None
        NID241_tree = None

        try:
            try:
                # Parser/ProtoCC.g:288:18: ( object_expr | message_constr | math_op | set_func | INT | BOOL | NID )
                alt37 = 7
                LA37 = self.input.LA(1)
                if LA37 in {ID}:
                    LA37 = self.input.LA(2)
                    if LA37 in {DOT}:
                        LA37_5 = self.input.LA(3)

                        if (LA37_5 in {ID, NID}) :
                            alt37 = 1
                        elif (LA37_5 in {112, 114, 115, 116, 117, 120}) :
                            alt37 = 4
                        else:
                            nvae = NoViableAltException("", 37, 5, self.input)

                            raise nvae


                    elif LA37 in {OBRACE}:
                        alt37 = 2
                    elif LA37 in {SEMICOLON}:
                        alt37 = 1
                    elif LA37 in {MINUS, PLUS}:
                        alt37 = 3
                    else:
                        nvae = NoViableAltException("", 37, 1, self.input)

                        raise nvae


                elif LA37 in {INT}:
                    LA37_2 = self.input.LA(2)

                    if (LA37_2 in {MINUS, PLUS}) :
                        alt37 = 3
                    elif (LA37_2 == SEMICOLON) :
                        alt37 = 5
                    else:
                        nvae = NoViableAltException("", 37, 2, self.input)

                        raise nvae


                elif LA37 in {BOOL}:
                    alt37 = 6
                elif LA37 in {NID}:
                    alt37 = 7
                else:
                    nvae = NoViableAltException("", 37, 0, self.input)

                    raise nvae


                if alt37 == 1:
                    # Parser/ProtoCC.g:288:20: object_expr
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_expr_in_assign_types2646)
                    object_expr235 = self.object_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_expr235.tree)



                elif alt37 == 2:
                    # Parser/ProtoCC.g:288:34: message_constr
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_message_constr_in_assign_types2650)
                    message_constr236 = self.message_constr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, message_constr236.tree)



                elif alt37 == 3:
                    # Parser/ProtoCC.g:288:51: math_op
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_math_op_in_assign_types2654)
                    math_op237 = self.math_op()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, math_op237.tree)



                elif alt37 == 4:
                    # Parser/ProtoCC.g:288:61: set_func
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_set_func_in_assign_types2658)
                    set_func238 = self.set_func()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_func238.tree)



                elif alt37 == 5:
                    # Parser/ProtoCC.g:288:72: INT
                    pass 
                    root_0 = self._adaptor.nil()


                    INT239 = self.match(self.input, INT, self.FOLLOW_INT_in_assign_types2662)
                    INT239_tree = self._adaptor.createWithPayload(INT239)
                    self._adaptor.addChild(root_0, INT239_tree)




                elif alt37 == 6:
                    # Parser/ProtoCC.g:288:78: BOOL
                    pass 
                    root_0 = self._adaptor.nil()


                    BOOL240 = self.match(self.input, BOOL, self.FOLLOW_BOOL_in_assign_types2666)
                    BOOL240_tree = self._adaptor.createWithPayload(BOOL240)
                    self._adaptor.addChild(root_0, BOOL240_tree)




                elif alt37 == 7:
                    # Parser/ProtoCC.g:288:85: NID
                    pass 
                    root_0 = self._adaptor.nil()


                    NID241 = self.match(self.input, NID, self.FOLLOW_NID_in_assign_types2670)
                    NID241_tree = self._adaptor.createWithPayload(NID241)
                    self._adaptor.addChild(root_0, NID241_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "assign_types"


    class math_op_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "math_op"
    # Parser/ProtoCC.g:289:5: math_op : val_range ( PLUS | MINUS ) val_range ;
    def math_op(self, ):
        retval = self.math_op_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set243 = None
        val_range242 = None
        val_range244 = None

        set243_tree = None

        try:
            try:
                # Parser/ProtoCC.g:289:13: ( val_range ( PLUS | MINUS ) val_range )
                # Parser/ProtoCC.g:289:15: val_range ( PLUS | MINUS ) val_range
                pass 
                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_val_range_in_math_op2681)
                val_range242 = self.val_range()

                self._state.following.pop()
                self._adaptor.addChild(root_0, val_range242.tree)


                set243 = self.input.LT(1)

                if self.input.LA(1) in {MINUS, PLUS}:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set243))

                    self._state.errorRecovery = False


                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse



                self._state.following.append(self.FOLLOW_val_range_in_math_op2691)
                val_range244 = self.val_range()

                self._state.following.pop()
                self._adaptor.addChild(root_0, val_range244.tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "math_op"


    class msg_stall_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "msg_stall"
    # Parser/ProtoCC.g:290:1: msg_stall : STALL SEMICOLON -> ^( STALL_ ) ;
    def msg_stall(self, ):
        retval = self.msg_stall_return()
        retval.start = self.input.LT(1)


        root_0 = None

        STALL245 = None
        SEMICOLON246 = None

        STALL245_tree = None
        SEMICOLON246_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_STALL = RewriteRuleTokenStream(self._adaptor, "token STALL")

        try:
            try:
                # Parser/ProtoCC.g:290:10: ( STALL SEMICOLON -> ^( STALL_ ) )
                # Parser/ProtoCC.g:290:12: STALL SEMICOLON
                pass 
                STALL245 = self.match(self.input, STALL, self.FOLLOW_STALL_in_msg_stall2697) 
                stream_STALL.add(STALL245)


                SEMICOLON246 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_msg_stall2699) 
                stream_SEMICOLON.add(SEMICOLON246)


                # AST Rewrite
                # elements: 
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 290:28: -> ^( STALL_ )
                # Parser/ProtoCC.g:290:31: ^( STALL_ )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(STALL_, "STALL_")
                , root_1)

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "msg_stall"


    class set_access_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "set_access"
    # Parser/ProtoCC.g:291:1: set_access : ACCESS SEMICOLON -> ^( ACCESS_ ACCESS ) ;
    def set_access(self, ):
        retval = self.set_access_return()
        retval.start = self.input.LT(1)


        root_0 = None

        ACCESS247 = None
        SEMICOLON248 = None

        ACCESS247_tree = None
        SEMICOLON248_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ACCESS = RewriteRuleTokenStream(self._adaptor, "token ACCESS")

        try:
            try:
                # Parser/ProtoCC.g:291:11: ( ACCESS SEMICOLON -> ^( ACCESS_ ACCESS ) )
                # Parser/ProtoCC.g:291:13: ACCESS SEMICOLON
                pass 
                ACCESS247 = self.match(self.input, ACCESS, self.FOLLOW_ACCESS_in_set_access2711) 
                stream_ACCESS.add(ACCESS247)


                SEMICOLON248 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_set_access2713) 
                stream_SEMICOLON.add(SEMICOLON248)


                # AST Rewrite
                # elements: ACCESS
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 291:30: -> ^( ACCESS_ ACCESS )
                # Parser/ProtoCC.g:291:33: ^( ACCESS_ ACCESS )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(ACCESS_, "ACCESS_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ACCESS.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "set_access"


    class undefine_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "undefine"
    # Parser/ProtoCC.g:292:1: undefine : UNDEF ID SEMICOLON -> ^( UNDEF_ ID ) ;
    def undefine(self, ):
        retval = self.undefine_return()
        retval.start = self.input.LT(1)


        root_0 = None

        UNDEF249 = None
        ID250 = None
        SEMICOLON251 = None

        UNDEF249_tree = None
        ID250_tree = None
        SEMICOLON251_tree = None
        stream_SEMICOLON = RewriteRuleTokenStream(self._adaptor, "token SEMICOLON")
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")
        stream_UNDEF = RewriteRuleTokenStream(self._adaptor, "token UNDEF")

        try:
            try:
                # Parser/ProtoCC.g:292:9: ( UNDEF ID SEMICOLON -> ^( UNDEF_ ID ) )
                # Parser/ProtoCC.g:292:11: UNDEF ID SEMICOLON
                pass 
                UNDEF249 = self.match(self.input, UNDEF, self.FOLLOW_UNDEF_in_undefine2727) 
                stream_UNDEF.add(UNDEF249)


                ID250 = self.match(self.input, ID, self.FOLLOW_ID_in_undefine2729) 
                stream_ID.add(ID250)


                SEMICOLON251 = self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_undefine2731) 
                stream_SEMICOLON.add(SEMICOLON251)


                # AST Rewrite
                # elements: ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 292:30: -> ^( UNDEF_ ID )
                # Parser/ProtoCC.g:292:33: ^( UNDEF_ ID )
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(
                self._adaptor.createFromType(UNDEF_, "UNDEF_")
                , root_1)

                self._adaptor.addChild(root_1, 
                stream_ID.nextNode()
                )

                self._adaptor.addChild(root_0, root_1)




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "undefine"


    class conditional_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "conditional"
    # Parser/ProtoCC.g:295:1: conditional : ( if_stmt | ifnot_stmt );
    def conditional(self, ):
        retval = self.conditional_return()
        retval.start = self.input.LT(1)


        root_0 = None

        if_stmt252 = None
        ifnot_stmt253 = None


        try:
            try:
                # Parser/ProtoCC.g:295:12: ( if_stmt | ifnot_stmt )
                alt38 = 2
                LA38_0 = self.input.LA(1)

                if (LA38_0 == IF) :
                    LA38_1 = self.input.LA(2)

                    if (LA38_1 == NEG) :
                        alt38 = 2
                    elif (LA38_1 in {BOOL, ID, INT, NID, OBRACE}) :
                        alt38 = 1
                    else:
                        nvae = NoViableAltException("", 38, 1, self.input)

                        raise nvae


                else:
                    nvae = NoViableAltException("", 38, 0, self.input)

                    raise nvae


                if alt38 == 1:
                    # Parser/ProtoCC.g:295:14: if_stmt
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_if_stmt_in_conditional2748)
                    if_stmt252 = self.if_stmt()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, if_stmt252.tree)



                elif alt38 == 2:
                    # Parser/ProtoCC.g:295:24: ifnot_stmt
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_ifnot_stmt_in_conditional2752)
                    ifnot_stmt253 = self.ifnot_stmt()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, ifnot_stmt253.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "conditional"


    class if_stmt_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "if_stmt"
    # Parser/ProtoCC.g:296:5: if_stmt : IF cond_comb OCBRACE if_expression CCBRACE ( ELSE OCBRACE else_expression CCBRACE )* -> {t_else}? ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ( else_expression )* ENDIF_ ) ) -> ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ENDIF_ ) ) ;
    def if_stmt(self, ):
        retval = self.if_stmt_return()
        retval.start = self.input.LT(1)


        root_0 = None

        IF254 = None
        OCBRACE256 = None
        CCBRACE258 = None
        ELSE259 = None
        OCBRACE260 = None
        CCBRACE262 = None
        cond_comb255 = None
        if_expression257 = None
        else_expression261 = None

        IF254_tree = None
        OCBRACE256_tree = None
        CCBRACE258_tree = None
        ELSE259_tree = None
        OCBRACE260_tree = None
        CCBRACE262_tree = None
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_ELSE = RewriteRuleTokenStream(self._adaptor, "token ELSE")
        stream_IF = RewriteRuleTokenStream(self._adaptor, "token IF")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_else_expression = RewriteRuleSubtreeStream(self._adaptor, "rule else_expression")
        stream_if_expression = RewriteRuleSubtreeStream(self._adaptor, "rule if_expression")
        stream_cond_comb = RewriteRuleSubtreeStream(self._adaptor, "rule cond_comb")
        t_else = 0
        try:
            try:
                # Parser/ProtoCC.g:297:5: ( IF cond_comb OCBRACE if_expression CCBRACE ( ELSE OCBRACE else_expression CCBRACE )* -> {t_else}? ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ( else_expression )* ENDIF_ ) ) -> ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ENDIF_ ) ) )
                # Parser/ProtoCC.g:297:7: IF cond_comb OCBRACE if_expression CCBRACE ( ELSE OCBRACE else_expression CCBRACE )*
                pass 
                IF254 = self.match(self.input, IF, self.FOLLOW_IF_in_if_stmt2771) 
                stream_IF.add(IF254)


                self._state.following.append(self.FOLLOW_cond_comb_in_if_stmt2773)
                cond_comb255 = self.cond_comb()

                self._state.following.pop()
                stream_cond_comb.add(cond_comb255.tree)


                OCBRACE256 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_if_stmt2775) 
                stream_OCBRACE.add(OCBRACE256)


                self._state.following.append(self.FOLLOW_if_expression_in_if_stmt2777)
                if_expression257 = self.if_expression()

                self._state.following.pop()
                stream_if_expression.add(if_expression257.tree)


                CCBRACE258 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_if_stmt2779) 
                stream_CCBRACE.add(CCBRACE258)


                # Parser/ProtoCC.g:298:5: ( ELSE OCBRACE else_expression CCBRACE )*
                while True: #loop39
                    alt39 = 2
                    LA39_0 = self.input.LA(1)

                    if (LA39_0 == ELSE) :
                        alt39 = 1


                    if alt39 == 1:
                        # Parser/ProtoCC.g:298:6: ELSE OCBRACE else_expression CCBRACE
                        pass 
                        ELSE259 = self.match(self.input, ELSE, self.FOLLOW_ELSE_in_if_stmt2786) 
                        stream_ELSE.add(ELSE259)


                        #action start
                        t_else=1
                        #action end


                        OCBRACE260 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_if_stmt2790) 
                        stream_OCBRACE.add(OCBRACE260)


                        self._state.following.append(self.FOLLOW_else_expression_in_if_stmt2792)
                        else_expression261 = self.else_expression()

                        self._state.following.pop()
                        stream_else_expression.add(else_expression261.tree)


                        CCBRACE262 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_if_stmt2794) 
                        stream_CCBRACE.add(CCBRACE262)



                    else:
                        break #loop39


                # AST Rewrite
                # elements: cond_comb, if_expression, cond_comb, else_expression, cond_comb, if_expression, cond_comb
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                if t_else:
                    # 299:5: -> {t_else}? ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ( else_expression )* ENDIF_ ) )
                    # Parser/ProtoCC.g:299:18: ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ( else_expression )* ENDIF_ ) )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IFELSE_, "IFELSE_")
                    , root_1)

                    # Parser/ProtoCC.g:299:28: ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:299:34: ^( COND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(COND_, "COND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    # Parser/ProtoCC.g:299:53: ( if_expression )*
                    while stream_if_expression.hasNext():
                        self._adaptor.addChild(root_2, stream_if_expression.nextTree())


                    stream_if_expression.reset();

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    # Parser/ProtoCC.g:299:76: ^( IF_ ^( NCOND_ cond_comb ) ( else_expression )* ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:299:82: ^( NCOND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(NCOND_, "NCOND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    # Parser/ProtoCC.g:299:102: ( else_expression )*
                    while stream_else_expression.hasNext():
                        self._adaptor.addChild(root_2, stream_else_expression.nextTree())


                    stream_else_expression.reset();

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    self._adaptor.addChild(root_0, root_1)



                else: 
                    # 300:5: -> ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ENDIF_ ) )
                    # Parser/ProtoCC.g:300:8: ^( IFELSE_ ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( NCOND_ cond_comb ) ENDIF_ ) )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IFELSE_, "IFELSE_")
                    , root_1)

                    # Parser/ProtoCC.g:300:18: ^( IF_ ^( COND_ cond_comb ) ( if_expression )* ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:300:24: ^( COND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(COND_, "COND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    # Parser/ProtoCC.g:300:43: ( if_expression )*
                    while stream_if_expression.hasNext():
                        self._adaptor.addChild(root_2, stream_if_expression.nextTree())


                    stream_if_expression.reset();

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    # Parser/ProtoCC.g:300:66: ^( IF_ ^( NCOND_ cond_comb ) ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:300:72: ^( NCOND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(NCOND_, "NCOND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    self._adaptor.addChild(root_0, root_1)



                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "if_stmt"


    class ifnot_stmt_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "ifnot_stmt"
    # Parser/ProtoCC.g:303:5: ifnot_stmt : IF NEG cond_comb OCBRACE if_expression CCBRACE ( ELSE OCBRACE else_expression CCBRACE )* -> {t_else}? ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ( else_expression )* ENDIF_ ) ) -> ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ENDIF_ ) ) ;
    def ifnot_stmt(self, ):
        retval = self.ifnot_stmt_return()
        retval.start = self.input.LT(1)


        root_0 = None

        IF263 = None
        NEG264 = None
        OCBRACE266 = None
        CCBRACE268 = None
        ELSE269 = None
        OCBRACE270 = None
        CCBRACE272 = None
        cond_comb265 = None
        if_expression267 = None
        else_expression271 = None

        IF263_tree = None
        NEG264_tree = None
        OCBRACE266_tree = None
        CCBRACE268_tree = None
        ELSE269_tree = None
        OCBRACE270_tree = None
        CCBRACE272_tree = None
        stream_NEG = RewriteRuleTokenStream(self._adaptor, "token NEG")
        stream_OCBRACE = RewriteRuleTokenStream(self._adaptor, "token OCBRACE")
        stream_ELSE = RewriteRuleTokenStream(self._adaptor, "token ELSE")
        stream_IF = RewriteRuleTokenStream(self._adaptor, "token IF")
        stream_CCBRACE = RewriteRuleTokenStream(self._adaptor, "token CCBRACE")
        stream_else_expression = RewriteRuleSubtreeStream(self._adaptor, "rule else_expression")
        stream_if_expression = RewriteRuleSubtreeStream(self._adaptor, "rule if_expression")
        stream_cond_comb = RewriteRuleSubtreeStream(self._adaptor, "rule cond_comb")
        t_else = 0
        try:
            try:
                # Parser/ProtoCC.g:304:5: ( IF NEG cond_comb OCBRACE if_expression CCBRACE ( ELSE OCBRACE else_expression CCBRACE )* -> {t_else}? ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ( else_expression )* ENDIF_ ) ) -> ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ENDIF_ ) ) )
                # Parser/ProtoCC.g:304:7: IF NEG cond_comb OCBRACE if_expression CCBRACE ( ELSE OCBRACE else_expression CCBRACE )*
                pass 
                IF263 = self.match(self.input, IF, self.FOLLOW_IF_in_ifnot_stmt2900) 
                stream_IF.add(IF263)


                NEG264 = self.match(self.input, NEG, self.FOLLOW_NEG_in_ifnot_stmt2902) 
                stream_NEG.add(NEG264)


                self._state.following.append(self.FOLLOW_cond_comb_in_ifnot_stmt2904)
                cond_comb265 = self.cond_comb()

                self._state.following.pop()
                stream_cond_comb.add(cond_comb265.tree)


                OCBRACE266 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_ifnot_stmt2906) 
                stream_OCBRACE.add(OCBRACE266)


                self._state.following.append(self.FOLLOW_if_expression_in_ifnot_stmt2908)
                if_expression267 = self.if_expression()

                self._state.following.pop()
                stream_if_expression.add(if_expression267.tree)


                CCBRACE268 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_ifnot_stmt2910) 
                stream_CCBRACE.add(CCBRACE268)


                # Parser/ProtoCC.g:305:5: ( ELSE OCBRACE else_expression CCBRACE )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == ELSE) :
                        alt40 = 1


                    if alt40 == 1:
                        # Parser/ProtoCC.g:305:6: ELSE OCBRACE else_expression CCBRACE
                        pass 
                        ELSE269 = self.match(self.input, ELSE, self.FOLLOW_ELSE_in_ifnot_stmt2917) 
                        stream_ELSE.add(ELSE269)


                        #action start
                        t_else=1
                        #action end


                        OCBRACE270 = self.match(self.input, OCBRACE, self.FOLLOW_OCBRACE_in_ifnot_stmt2921) 
                        stream_OCBRACE.add(OCBRACE270)


                        self._state.following.append(self.FOLLOW_else_expression_in_ifnot_stmt2923)
                        else_expression271 = self.else_expression()

                        self._state.following.pop()
                        stream_else_expression.add(else_expression271.tree)


                        CCBRACE272 = self.match(self.input, CCBRACE, self.FOLLOW_CCBRACE_in_ifnot_stmt2925) 
                        stream_CCBRACE.add(CCBRACE272)



                    else:
                        break #loop40


                # AST Rewrite
                # elements: cond_comb, if_expression, cond_comb, else_expression, cond_comb, if_expression, cond_comb
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                if t_else:
                    # 306:5: -> {t_else}? ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ( else_expression )* ENDIF_ ) )
                    # Parser/ProtoCC.g:306:18: ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ( else_expression )* ENDIF_ ) )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IFELSE_, "IFELSE_")
                    , root_1)

                    # Parser/ProtoCC.g:306:28: ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:306:34: ^( NCOND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(NCOND_, "NCOND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    # Parser/ProtoCC.g:306:54: ( if_expression )*
                    while stream_if_expression.hasNext():
                        self._adaptor.addChild(root_2, stream_if_expression.nextTree())


                    stream_if_expression.reset();

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    # Parser/ProtoCC.g:306:77: ^( IF_ ^( COND_ cond_comb ) ( else_expression )* ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:306:83: ^( COND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(COND_, "COND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    # Parser/ProtoCC.g:306:102: ( else_expression )*
                    while stream_else_expression.hasNext():
                        self._adaptor.addChild(root_2, stream_else_expression.nextTree())


                    stream_else_expression.reset();

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    self._adaptor.addChild(root_0, root_1)



                else: 
                    # 307:5: -> ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ENDIF_ ) )
                    # Parser/ProtoCC.g:307:8: ^( IFELSE_ ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ ) ^( IF_ ^( COND_ cond_comb ) ENDIF_ ) )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IFELSE_, "IFELSE_")
                    , root_1)

                    # Parser/ProtoCC.g:307:18: ^( IF_ ^( NCOND_ cond_comb ) ( if_expression )* ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:307:24: ^( NCOND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(NCOND_, "NCOND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    # Parser/ProtoCC.g:307:44: ( if_expression )*
                    while stream_if_expression.hasNext():
                        self._adaptor.addChild(root_2, stream_if_expression.nextTree())


                    stream_if_expression.reset();

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    # Parser/ProtoCC.g:307:67: ^( IF_ ^( COND_ cond_comb ) ENDIF_ )
                    root_2 = self._adaptor.nil()
                    root_2 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(IF_, "IF_")
                    , root_2)

                    # Parser/ProtoCC.g:307:73: ^( COND_ cond_comb )
                    root_3 = self._adaptor.nil()
                    root_3 = self._adaptor.becomeRoot(
                    self._adaptor.createFromType(COND_, "COND_")
                    , root_3)

                    self._adaptor.addChild(root_3, stream_cond_comb.nextTree())

                    self._adaptor.addChild(root_2, root_3)

                    self._adaptor.addChild(root_2, 
                    self._adaptor.createFromType(ENDIF_, "ENDIF_")
                    )

                    self._adaptor.addChild(root_1, root_2)

                    self._adaptor.addChild(root_0, root_1)



                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "ifnot_stmt"


    class if_expression_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "if_expression"
    # Parser/ProtoCC.g:310:9: if_expression : ( exprwbreak )* ;
    def if_expression(self, ):
        retval = self.if_expression_return()
        retval.start = self.input.LT(1)


        root_0 = None

        exprwbreak273 = None


        try:
            try:
                # Parser/ProtoCC.g:310:22: ( ( exprwbreak )* )
                # Parser/ProtoCC.g:310:24: ( exprwbreak )*
                pass 
                root_0 = self._adaptor.nil()


                # Parser/ProtoCC.g:310:24: ( exprwbreak )*
                while True: #loop41
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 in {ACCESS, AWAIT, BREAK, ID, IF, STALL, STATE, UNDEF, 107}) :
                        alt41 = 1


                    if alt41 == 1:
                        # Parser/ProtoCC.g:310:24: exprwbreak
                        pass 
                        self._state.following.append(self.FOLLOW_exprwbreak_in_if_expression3026)
                        exprwbreak273 = self.exprwbreak()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exprwbreak273.tree)



                    else:
                        break #loop41




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "if_expression"


    class else_expression_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "else_expression"
    # Parser/ProtoCC.g:311:9: else_expression : ( exprwbreak )* ;
    def else_expression(self, ):
        retval = self.else_expression_return()
        retval.start = self.input.LT(1)


        root_0 = None

        exprwbreak274 = None


        try:
            try:
                # Parser/ProtoCC.g:311:24: ( ( exprwbreak )* )
                # Parser/ProtoCC.g:311:26: ( exprwbreak )*
                pass 
                root_0 = self._adaptor.nil()


                # Parser/ProtoCC.g:311:26: ( exprwbreak )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 in {ACCESS, AWAIT, BREAK, ID, IF, STALL, STATE, UNDEF, 107}) :
                        alt42 = 1


                    if alt42 == 1:
                        # Parser/ProtoCC.g:311:26: exprwbreak
                        pass 
                        self._state.following.append(self.FOLLOW_exprwbreak_in_else_expression3041)
                        exprwbreak274 = self.exprwbreak()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exprwbreak274.tree)



                    else:
                        break #loop42




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "else_expression"


    class exprwbreak_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "exprwbreak"
    # Parser/ProtoCC.g:312:9: exprwbreak : ( expressions | network_send | network_mcast | network_bcast | transaction | next_break );
    def exprwbreak(self, ):
        retval = self.exprwbreak_return()
        retval.start = self.input.LT(1)


        root_0 = None

        expressions275 = None
        network_send276 = None
        network_mcast277 = None
        network_bcast278 = None
        transaction279 = None
        next_break280 = None


        try:
            try:
                # Parser/ProtoCC.g:312:19: ( expressions | network_send | network_mcast | network_bcast | transaction | next_break )
                alt43 = 6
                LA43 = self.input.LA(1)
                if LA43 in {ID}:
                    LA43_1 = self.input.LA(2)

                    if (LA43_1 == DOT) :
                        LA43 = self.input.LA(3)
                        if LA43 in {ID, NID, 112, 114, 115, 116, 117, 120}:
                            alt43 = 1
                        elif LA43 in {110, 119}:
                            alt43 = 2
                        elif LA43 in {108, 118}:
                            alt43 = 3
                        elif LA43 in {106, 113}:
                            alt43 = 4
                        else:
                            nvae = NoViableAltException("", 43, 10, self.input)

                            raise nvae


                    elif (LA43_1 in {EQUALSIGN, SEMICOLON}) :
                        alt43 = 1
                    else:
                        nvae = NoViableAltException("", 43, 1, self.input)

                        raise nvae


                elif LA43 in {ACCESS, IF, STALL, STATE, UNDEF, 107}:
                    alt43 = 1
                elif LA43 in {AWAIT}:
                    alt43 = 5
                elif LA43 in {BREAK}:
                    alt43 = 6
                else:
                    nvae = NoViableAltException("", 43, 0, self.input)

                    raise nvae


                if alt43 == 1:
                    # Parser/ProtoCC.g:312:21: expressions
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_expressions_in_exprwbreak3056)
                    expressions275 = self.expressions()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expressions275.tree)



                elif alt43 == 2:
                    # Parser/ProtoCC.g:312:35: network_send
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_send_in_exprwbreak3060)
                    network_send276 = self.network_send()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_send276.tree)



                elif alt43 == 3:
                    # Parser/ProtoCC.g:312:50: network_mcast
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_mcast_in_exprwbreak3064)
                    network_mcast277 = self.network_mcast()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_mcast277.tree)



                elif alt43 == 4:
                    # Parser/ProtoCC.g:312:66: network_bcast
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_network_bcast_in_exprwbreak3068)
                    network_bcast278 = self.network_bcast()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, network_bcast278.tree)



                elif alt43 == 5:
                    # Parser/ProtoCC.g:312:82: transaction
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_transaction_in_exprwbreak3072)
                    transaction279 = self.transaction()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, transaction279.tree)



                elif alt43 == 6:
                    # Parser/ProtoCC.g:312:96: next_break
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_next_break_in_exprwbreak3076)
                    next_break280 = self.next_break()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, next_break280.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "exprwbreak"


    class cond_comb_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "cond_comb"
    # Parser/ProtoCC.g:313:9: cond_comb : cond_rel ( combinatorial_operator cond_rel )* ;
    def cond_comb(self, ):
        retval = self.cond_comb_return()
        retval.start = self.input.LT(1)


        root_0 = None

        cond_rel281 = None
        combinatorial_operator282 = None
        cond_rel283 = None


        try:
            try:
                # Parser/ProtoCC.g:313:18: ( cond_rel ( combinatorial_operator cond_rel )* )
                # Parser/ProtoCC.g:313:20: cond_rel ( combinatorial_operator cond_rel )*
                pass 
                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_cond_rel_in_cond_comb3090)
                cond_rel281 = self.cond_rel()

                self._state.following.pop()
                self._adaptor.addChild(root_0, cond_rel281.tree)


                # Parser/ProtoCC.g:313:29: ( combinatorial_operator cond_rel )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 in {100, 121}) :
                        alt44 = 1


                    if alt44 == 1:
                        # Parser/ProtoCC.g:313:30: combinatorial_operator cond_rel
                        pass 
                        self._state.following.append(self.FOLLOW_combinatorial_operator_in_cond_comb3093)
                        combinatorial_operator282 = self.combinatorial_operator()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, combinatorial_operator282.tree)


                        self._state.following.append(self.FOLLOW_cond_rel_in_cond_comb3095)
                        cond_rel283 = self.cond_rel()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, cond_rel283.tree)



                    else:
                        break #loop44




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "cond_comb"


    class cond_rel_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "cond_rel"
    # Parser/ProtoCC.g:314:9: cond_rel : ( OBRACE )* cond_sel ( CBRACE )* -> cond_sel ;
    def cond_rel(self, ):
        retval = self.cond_rel_return()
        retval.start = self.input.LT(1)


        root_0 = None

        OBRACE284 = None
        CBRACE286 = None
        cond_sel285 = None

        OBRACE284_tree = None
        CBRACE286_tree = None
        stream_OBRACE = RewriteRuleTokenStream(self._adaptor, "token OBRACE")
        stream_CBRACE = RewriteRuleTokenStream(self._adaptor, "token CBRACE")
        stream_cond_sel = RewriteRuleSubtreeStream(self._adaptor, "rule cond_sel")
        try:
            try:
                # Parser/ProtoCC.g:314:18: ( ( OBRACE )* cond_sel ( CBRACE )* -> cond_sel )
                # Parser/ProtoCC.g:314:20: ( OBRACE )* cond_sel ( CBRACE )*
                pass 
                # Parser/ProtoCC.g:314:20: ( OBRACE )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == OBRACE) :
                        alt45 = 1


                    if alt45 == 1:
                        # Parser/ProtoCC.g:314:20: OBRACE
                        pass 
                        OBRACE284 = self.match(self.input, OBRACE, self.FOLLOW_OBRACE_in_cond_rel3112) 
                        stream_OBRACE.add(OBRACE284)



                    else:
                        break #loop45


                self._state.following.append(self.FOLLOW_cond_sel_in_cond_rel3115)
                cond_sel285 = self.cond_sel()

                self._state.following.pop()
                stream_cond_sel.add(cond_sel285.tree)


                # Parser/ProtoCC.g:314:37: ( CBRACE )*
                while True: #loop46
                    alt46 = 2
                    LA46_0 = self.input.LA(1)

                    if (LA46_0 == CBRACE) :
                        alt46 = 1


                    if alt46 == 1:
                        # Parser/ProtoCC.g:314:37: CBRACE
                        pass 
                        CBRACE286 = self.match(self.input, CBRACE, self.FOLLOW_CBRACE_in_cond_rel3117) 
                        stream_CBRACE.add(CBRACE286)



                    else:
                        break #loop46


                # AST Rewrite
                # elements: cond_sel
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                retval.tree = root_0
                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 314:45: -> cond_sel
                self._adaptor.addChild(root_0, stream_cond_sel.nextTree())




                retval.tree = root_0





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "cond_rel"


    class cond_sel_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "cond_sel"
    # Parser/ProtoCC.g:315:13: cond_sel : cond_type_expr ( relational_operator cond_type_expr )* ;
    def cond_sel(self, ):
        retval = self.cond_sel_return()
        retval.start = self.input.LT(1)


        root_0 = None

        cond_type_expr287 = None
        relational_operator288 = None
        cond_type_expr289 = None


        try:
            try:
                # Parser/ProtoCC.g:315:22: ( cond_type_expr ( relational_operator cond_type_expr )* )
                # Parser/ProtoCC.g:315:24: cond_type_expr ( relational_operator cond_type_expr )*
                pass 
                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_cond_type_expr_in_cond_sel3141)
                cond_type_expr287 = self.cond_type_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, cond_type_expr287.tree)


                # Parser/ProtoCC.g:315:39: ( relational_operator cond_type_expr )*
                while True: #loop47
                    alt47 = 2
                    LA47_0 = self.input.LA(1)

                    if ((101 <= LA47_0 <= 105) or LA47_0 in {99}) :
                        alt47 = 1


                    if alt47 == 1:
                        # Parser/ProtoCC.g:315:40: relational_operator cond_type_expr
                        pass 
                        self._state.following.append(self.FOLLOW_relational_operator_in_cond_sel3144)
                        relational_operator288 = self.relational_operator()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, relational_operator288.tree)


                        self._state.following.append(self.FOLLOW_cond_type_expr_in_cond_sel3146)
                        cond_type_expr289 = self.cond_type_expr()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, cond_type_expr289.tree)



                    else:
                        break #loop47




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "cond_sel"


    class cond_type_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "cond_type_expr"
    # Parser/ProtoCC.g:316:13: cond_type_expr : cond_types ( ( PLUS | MINUS | MULT ) cond_types )* ;
    def cond_type_expr(self, ):
        retval = self.cond_type_expr_return()
        retval.start = self.input.LT(1)


        root_0 = None

        set291 = None
        cond_types290 = None
        cond_types292 = None

        set291_tree = None

        try:
            try:
                # Parser/ProtoCC.g:316:27: ( cond_types ( ( PLUS | MINUS | MULT ) cond_types )* )
                # Parser/ProtoCC.g:316:29: cond_types ( ( PLUS | MINUS | MULT ) cond_types )*
                pass 
                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_cond_types_in_cond_type_expr3166)
                cond_types290 = self.cond_types()

                self._state.following.pop()
                self._adaptor.addChild(root_0, cond_types290.tree)


                # Parser/ProtoCC.g:316:40: ( ( PLUS | MINUS | MULT ) cond_types )*
                while True: #loop48
                    alt48 = 2
                    LA48_0 = self.input.LA(1)

                    if (LA48_0 in {MINUS, MULT, PLUS}) :
                        alt48 = 1


                    if alt48 == 1:
                        # Parser/ProtoCC.g:316:41: ( PLUS | MINUS | MULT ) cond_types
                        pass 
                        set291 = self.input.LT(1)

                        if self.input.LA(1) in {MINUS, MULT, PLUS}:
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set291))

                            self._state.errorRecovery = False


                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse



                        self._state.following.append(self.FOLLOW_cond_types_in_cond_type_expr3181)
                        cond_types292 = self.cond_types()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, cond_types292.tree)



                    else:
                        break #loop48




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "cond_type_expr"


    class cond_types_return(ParserRuleReturnScope):
        def __init__(self):
            super().__init__()

            self.tree = None





    # $ANTLR start "cond_types"
    # Parser/ProtoCC.g:317:13: cond_types : ( object_expr | set_func | INT | BOOL | NID );
    def cond_types(self, ):
        retval = self.cond_types_return()
        retval.start = self.input.LT(1)


        root_0 = None

        INT295 = None
        BOOL296 = None
        NID297 = None
        object_expr293 = None
        set_func294 = None

        INT295_tree = None
        BOOL296_tree = None
        NID297_tree = None

        try:
            try:
                # Parser/ProtoCC.g:317:24: ( object_expr | set_func | INT | BOOL | NID )
                alt49 = 5
                LA49 = self.input.LA(1)
                if LA49 in {ID}:
                    LA49_1 = self.input.LA(2)

                    if (LA49_1 == DOT) :
                        LA49_5 = self.input.LA(3)

                        if (LA49_5 in {ID, NID}) :
                            alt49 = 1
                        elif (LA49_5 in {112, 114, 115, 116, 117, 120}) :
                            alt49 = 2
                        else:
                            nvae = NoViableAltException("", 49, 5, self.input)

                            raise nvae


                    elif ((99 <= LA49_1 <= 105) or LA49_1 in {CBRACE, MINUS, MULT, OCBRACE, PLUS, 121}) :
                        alt49 = 1
                    else:
                        nvae = NoViableAltException("", 49, 1, self.input)

                        raise nvae


                elif LA49 in {INT}:
                    alt49 = 3
                elif LA49 in {BOOL}:
                    alt49 = 4
                elif LA49 in {NID}:
                    alt49 = 5
                else:
                    nvae = NoViableAltException("", 49, 0, self.input)

                    raise nvae


                if alt49 == 1:
                    # Parser/ProtoCC.g:317:26: object_expr
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_object_expr_in_cond_types3202)
                    object_expr293 = self.object_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, object_expr293.tree)



                elif alt49 == 2:
                    # Parser/ProtoCC.g:317:40: set_func
                    pass 
                    root_0 = self._adaptor.nil()


                    self._state.following.append(self.FOLLOW_set_func_in_cond_types3206)
                    set_func294 = self.set_func()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_func294.tree)



                elif alt49 == 3:
                    # Parser/ProtoCC.g:317:51: INT
                    pass 
                    root_0 = self._adaptor.nil()


                    INT295 = self.match(self.input, INT, self.FOLLOW_INT_in_cond_types3210)
                    INT295_tree = self._adaptor.createWithPayload(INT295)
                    self._adaptor.addChild(root_0, INT295_tree)




                elif alt49 == 4:
                    # Parser/ProtoCC.g:317:57: BOOL
                    pass 
                    root_0 = self._adaptor.nil()


                    BOOL296 = self.match(self.input, BOOL, self.FOLLOW_BOOL_in_cond_types3214)
                    BOOL296_tree = self._adaptor.createWithPayload(BOOL296)
                    self._adaptor.addChild(root_0, BOOL296_tree)




                elif alt49 == 5:
                    # Parser/ProtoCC.g:317:64: NID
                    pass 
                    root_0 = self._adaptor.nil()


                    NID297 = self.match(self.input, NID, self.FOLLOW_NID_in_cond_types3218)
                    NID297_tree = self._adaptor.createWithPayload(NID297)
                    self._adaptor.addChild(root_0, NID297_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        finally:
            pass
        return retval

    # $ANTLR end "cond_types"



 

    FOLLOW_107_in_internal_event_function705 = frozenset([1])
    FOLLOW_const_decl_in_document1033 = frozenset([1, 4, 6, 19, 27, 32, 48, 50, 61, 64, 70, 90, 92, 94, 107])
    FOLLOW_init_hw_in_document1037 = frozenset([1, 4, 6, 19, 27, 32, 48, 50, 61, 64, 70, 90, 92, 94, 107])
    FOLLOW_arch_block_in_document1041 = frozenset([1, 4, 6, 19, 27, 32, 48, 50, 61, 64, 70, 90, 92, 94, 107])
    FOLLOW_expressions_in_document1045 = frozenset([1, 4, 6, 19, 27, 32, 48, 50, 61, 64, 70, 90, 92, 94, 107])
    FOLLOW_int_decl_in_declarations1058 = frozenset([1])
    FOLLOW_bool_decl_in_declarations1062 = frozenset([1])
    FOLLOW_state_decl_in_declarations1066 = frozenset([1])
    FOLLOW_data_decl_in_declarations1070 = frozenset([1])
    FOLLOW_id_decl_in_declarations1074 = frozenset([1])
    FOLLOW_CONSTANT_in_const_decl1086 = frozenset([48])
    FOLLOW_ID_in_const_decl1088 = frozenset([55])
    FOLLOW_INT_in_const_decl1090 = frozenset([1])
    FOLLOW_INTID_in_int_decl1112 = frozenset([78])
    FOLLOW_range_in_int_decl1114 = frozenset([48])
    FOLLOW_ID_in_int_decl1116 = frozenset([41, 83])
    FOLLOW_EQUALSIGN_in_int_decl1119 = frozenset([55])
    FOLLOW_INT_in_int_decl1121 = frozenset([41, 83])
    FOLLOW_SEMICOLON_in_int_decl1125 = frozenset([1])
    FOLLOW_BOOLID_in_bool_decl1153 = frozenset([48])
    FOLLOW_ID_in_bool_decl1155 = frozenset([41, 83])
    FOLLOW_EQUALSIGN_in_bool_decl1158 = frozenset([14])
    FOLLOW_BOOL_in_bool_decl1160 = frozenset([41, 83])
    FOLLOW_SEMICOLON_in_bool_decl1164 = frozenset([1])
    FOLLOW_STATE_in_state_decl1191 = frozenset([48])
    FOLLOW_ID_in_state_decl1193 = frozenset([83])
    FOLLOW_SEMICOLON_in_state_decl1195 = frozenset([1])
    FOLLOW_DATA_in_data_decl1214 = frozenset([48])
    FOLLOW_ID_in_data_decl1216 = frozenset([83])
    FOLLOW_SEMICOLON_in_data_decl1218 = frozenset([1])
    FOLLOW_set_decl_in_id_decl1237 = frozenset([74, 85])
    FOLLOW_NID_in_id_decl1240 = frozenset([48])
    FOLLOW_ID_in_id_decl1242 = frozenset([41, 83])
    FOLLOW_EQUALSIGN_in_id_decl1245 = frozenset([48, 85])
    FOLLOW_set_decl_in_id_decl1247 = frozenset([48, 85])
    FOLLOW_ID_in_id_decl1250 = frozenset([41, 83])
    FOLLOW_SEMICOLON_in_id_decl1254 = frozenset([1])
    FOLLOW_SET_in_set_decl1291 = frozenset([78])
    FOLLOW_OEBRACE_in_set_decl1293 = frozenset([48, 55])
    FOLLOW_val_range_in_set_decl1295 = frozenset([23])
    FOLLOW_CEBRACE_in_set_decl1297 = frozenset([1])
    FOLLOW_OEBRACE_in_range1320 = frozenset([48, 55])
    FOLLOW_val_range_in_range1322 = frozenset([34])
    FOLLOW_DOT_in_range1324 = frozenset([34])
    FOLLOW_DOT_in_range1326 = frozenset([48, 55])
    FOLLOW_val_range_in_range1328 = frozenset([23])
    FOLLOW_CEBRACE_in_range1330 = frozenset([1])
    FOLLOW_ARRAY_in_array_decl1379 = frozenset([78])
    FOLLOW_range_in_array_decl1381 = frozenset([1])
    FOLLOW_FIFO_in_fifo_decl1391 = frozenset([78])
    FOLLOW_range_in_fifo_decl1393 = frozenset([1])
    FOLLOW_network_block_in_init_hw1403 = frozenset([1])
    FOLLOW_machines_in_init_hw1407 = frozenset([1])
    FOLLOW_message_block_in_init_hw1411 = frozenset([1])
    FOLLOW_object_expr_in_object_block1422 = frozenset([83])
    FOLLOW_SEMICOLON_in_object_block1424 = frozenset([1])
    FOLLOW_object_id_in_object_expr1439 = frozenset([1])
    FOLLOW_object_func_in_object_expr1443 = frozenset([1])
    FOLLOW_ID_in_object_id1454 = frozenset([1])
    FOLLOW_ID_in_object_func1471 = frozenset([34])
    FOLLOW_DOT_in_object_func1473 = frozenset([48, 74])
    FOLLOW_object_idres_in_object_func1475 = frozenset([1, 76])
    FOLLOW_OBRACE_in_object_func1478 = frozenset([21, 24, 48])
    FOLLOW_object_expr_in_object_func1480 = frozenset([21, 24, 48])
    FOLLOW_COMMA_in_object_func1484 = frozenset([48])
    FOLLOW_object_expr_in_object_func1486 = frozenset([21, 24])
    FOLLOW_CBRACE_in_object_func1490 = frozenset([1, 76])
    FOLLOW_cache_block_in_machines1559 = frozenset([1])
    FOLLOW_dir_block_in_machines1563 = frozenset([1])
    FOLLOW_mem_block_in_machines1567 = frozenset([1])
    FOLLOW_CACHE_in_cache_block1582 = frozenset([77])
    FOLLOW_OCBRACE_in_cache_block1584 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_declarations_in_cache_block1586 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_CCBRACE_in_cache_block1589 = frozenset([48, 85])
    FOLLOW_objset_decl_in_cache_block1591 = frozenset([48, 85])
    FOLLOW_ID_in_cache_block1594 = frozenset([83])
    FOLLOW_SEMICOLON_in_cache_block1596 = frozenset([1])
    FOLLOW_DIR_in_dir_block1637 = frozenset([77])
    FOLLOW_OCBRACE_in_dir_block1639 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_declarations_in_dir_block1641 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_CCBRACE_in_dir_block1644 = frozenset([48, 85])
    FOLLOW_objset_decl_in_dir_block1646 = frozenset([48, 85])
    FOLLOW_ID_in_dir_block1649 = frozenset([83])
    FOLLOW_SEMICOLON_in_dir_block1651 = frozenset([1])
    FOLLOW_MEM_in_mem_block1692 = frozenset([77])
    FOLLOW_OCBRACE_in_mem_block1694 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_declarations_in_mem_block1696 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_CCBRACE_in_mem_block1699 = frozenset([48, 85])
    FOLLOW_objset_decl_in_mem_block1701 = frozenset([48, 85])
    FOLLOW_ID_in_mem_block1704 = frozenset([83])
    FOLLOW_SEMICOLON_in_mem_block1706 = frozenset([1])
    FOLLOW_SET_in_objset_decl1748 = frozenset([78])
    FOLLOW_OEBRACE_in_objset_decl1750 = frozenset([48, 55])
    FOLLOW_val_range_in_objset_decl1752 = frozenset([23])
    FOLLOW_CEBRACE_in_objset_decl1754 = frozenset([1])
    FOLLOW_NETWORK_in_network_block1780 = frozenset([77])
    FOLLOW_OCBRACE_in_network_block1782 = frozenset([22, 109, 111])
    FOLLOW_network_element_in_network_block1784 = frozenset([22, 109, 111])
    FOLLOW_CCBRACE_in_network_block1787 = frozenset([83])
    FOLLOW_SEMICOLON_in_network_block1789 = frozenset([1])
    FOLLOW_element_type_in_network_element1832 = frozenset([48])
    FOLLOW_ID_in_network_element1834 = frozenset([83])
    FOLLOW_SEMICOLON_in_network_element1836 = frozenset([1])
    FOLLOW_ID_in_network_send1857 = frozenset([34])
    FOLLOW_DOT_in_network_send1859 = frozenset([110, 119])
    FOLLOW_send_function_in_network_send1861 = frozenset([76])
    FOLLOW_OBRACE_in_network_send1863 = frozenset([48])
    FOLLOW_ID_in_network_send1865 = frozenset([21])
    FOLLOW_CBRACE_in_network_send1867 = frozenset([83])
    FOLLOW_SEMICOLON_in_network_send1869 = frozenset([1])
    FOLLOW_ID_in_network_bcast1889 = frozenset([34])
    FOLLOW_DOT_in_network_bcast1891 = frozenset([106, 113])
    FOLLOW_bcast_function_in_network_bcast1893 = frozenset([76])
    FOLLOW_OBRACE_in_network_bcast1895 = frozenset([48])
    FOLLOW_ID_in_network_bcast1897 = frozenset([21])
    FOLLOW_CBRACE_in_network_bcast1899 = frozenset([83])
    FOLLOW_SEMICOLON_in_network_bcast1901 = frozenset([1])
    FOLLOW_ID_in_network_mcast1921 = frozenset([34])
    FOLLOW_DOT_in_network_mcast1923 = frozenset([108, 118])
    FOLLOW_mcast_function_in_network_mcast1925 = frozenset([76])
    FOLLOW_OBRACE_in_network_mcast1927 = frozenset([48])
    FOLLOW_ID_in_network_mcast1929 = frozenset([24])
    FOLLOW_COMMA_in_network_mcast1931 = frozenset([48])
    FOLLOW_ID_in_network_mcast1933 = frozenset([21])
    FOLLOW_CBRACE_in_network_mcast1935 = frozenset([83])
    FOLLOW_SEMICOLON_in_network_mcast1937 = frozenset([1])
    FOLLOW_MSG_in_message_block1967 = frozenset([48])
    FOLLOW_ID_in_message_block1969 = frozenset([77])
    FOLLOW_OCBRACE_in_message_block1971 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_declarations_in_message_block1973 = frozenset([15, 22, 29, 56, 74, 85, 92])
    FOLLOW_CCBRACE_in_message_block1976 = frozenset([83])
    FOLLOW_SEMICOLON_in_message_block1978 = frozenset([1])
    FOLLOW_ID_in_message_constr2000 = frozenset([76])
    FOLLOW_OBRACE_in_message_constr2002 = frozenset([14, 21, 24, 48, 55, 74])
    FOLLOW_message_expr_in_message_constr2004 = frozenset([14, 21, 24, 48, 55, 74])
    FOLLOW_COMMA_in_message_constr2008 = frozenset([14, 48, 55, 74])
    FOLLOW_message_expr_in_message_constr2010 = frozenset([21, 24])
    FOLLOW_CBRACE_in_message_constr2014 = frozenset([1])
    FOLLOW_object_expr_in_message_expr2036 = frozenset([1])
    FOLLOW_set_func_in_message_expr2040 = frozenset([1])
    FOLLOW_INT_in_message_expr2044 = frozenset([1])
    FOLLOW_BOOL_in_message_expr2048 = frozenset([1])
    FOLLOW_NID_in_message_expr2052 = frozenset([1])
    FOLLOW_set_func_in_set_block2070 = frozenset([83])
    FOLLOW_SEMICOLON_in_set_block2072 = frozenset([1])
    FOLLOW_ID_in_set_func2087 = frozenset([34])
    FOLLOW_DOT_in_set_func2089 = frozenset([112, 114, 115, 116, 117, 120])
    FOLLOW_set_function_types_in_set_func2091 = frozenset([76])
    FOLLOW_OBRACE_in_set_func2093 = frozenset([21, 48])
    FOLLOW_set_nest_in_set_func2095 = frozenset([21, 48])
    FOLLOW_CBRACE_in_set_func2098 = frozenset([1])
    FOLLOW_set_func_in_set_nest2136 = frozenset([1])
    FOLLOW_object_expr_in_set_nest2140 = frozenset([1])
    FOLLOW_internal_event_func_in_internal_event_block2158 = frozenset([83])
    FOLLOW_SEMICOLON_in_internal_event_block2160 = frozenset([1])
    FOLLOW_internal_event_function_in_internal_event_func2174 = frozenset([76])
    FOLLOW_OBRACE_in_internal_event_func2176 = frozenset([48])
    FOLLOW_ID_in_internal_event_func2178 = frozenset([21])
    FOLLOW_CBRACE_in_internal_event_func2180 = frozenset([1])
    FOLLOW_ARCH_in_arch_block2204 = frozenset([48])
    FOLLOW_ID_in_arch_block2206 = frozenset([77])
    FOLLOW_OCBRACE_in_arch_block2208 = frozenset([22, 80, 88])
    FOLLOW_arch_body_in_arch_block2210 = frozenset([22])
    FOLLOW_CCBRACE_in_arch_block2212 = frozenset([1])
    FOLLOW_stable_def_in_arch_body2234 = frozenset([1, 80, 88])
    FOLLOW_process_block_in_arch_body2238 = frozenset([1, 80, 88])
    FOLLOW_STABLE_in_stable_def2248 = frozenset([77])
    FOLLOW_OCBRACE_in_stable_def2250 = frozenset([48])
    FOLLOW_ID_in_stable_def2252 = frozenset([22, 24])
    FOLLOW_COMMA_in_stable_def2255 = frozenset([48])
    FOLLOW_ID_in_stable_def2257 = frozenset([22, 24])
    FOLLOW_CCBRACE_in_stable_def2261 = frozenset([1])
    FOLLOW_PROC_in_process_block2280 = frozenset([76])
    FOLLOW_process_trans_in_process_block2282 = frozenset([77])
    FOLLOW_OCBRACE_in_process_block2284 = frozenset([4, 11, 22, 48, 50, 90, 92, 94, 107])
    FOLLOW_process_expr_in_process_block2286 = frozenset([4, 11, 22, 48, 50, 90, 92, 94, 107])
    FOLLOW_CCBRACE_in_process_block2289 = frozenset([1])
    FOLLOW_OBRACE_in_process_trans2315 = frozenset([48])
    FOLLOW_ID_in_process_trans2317 = frozenset([24])
    FOLLOW_COMMA_in_process_trans2319 = frozenset([4, 44, 48])
    FOLLOW_process_events_in_process_trans2321 = frozenset([21, 24])
    FOLLOW_process_finalstate_in_process_trans2323 = frozenset([21, 24])
    FOLLOW_CBRACE_in_process_trans2326 = frozenset([1])
    FOLLOW_COMMA_in_process_finalstate2349 = frozenset([48, 92])
    FOLLOW_process_finalident_in_process_finalstate2351 = frozenset([1])
    FOLLOW_expressions_in_process_expr2404 = frozenset([1])
    FOLLOW_network_send_in_process_expr2408 = frozenset([1])
    FOLLOW_network_mcast_in_process_expr2412 = frozenset([1])
    FOLLOW_network_bcast_in_process_expr2416 = frozenset([1])
    FOLLOW_transaction_in_process_expr2419 = frozenset([1])
    FOLLOW_AWAIT_in_transaction2429 = frozenset([77])
    FOLLOW_OCBRACE_in_transaction2431 = frozenset([22, 96])
    FOLLOW_trans_in_transaction2433 = frozenset([22, 96])
    FOLLOW_CCBRACE_in_transaction2436 = frozenset([1])
    FOLLOW_WHEN_in_trans2456 = frozenset([48])
    FOLLOW_ID_in_trans2458 = frozenset([31])
    FOLLOW_DDOT_in_trans2460 = frozenset([1, 4, 11, 17, 48, 50, 72, 90, 92, 94, 107])
    FOLLOW_trans_body_in_trans2462 = frozenset([1, 4, 11, 17, 48, 50, 72, 90, 92, 94, 107])
    FOLLOW_expressions_in_trans_body2495 = frozenset([1])
    FOLLOW_next_trans_in_trans_body2499 = frozenset([1])
    FOLLOW_next_break_in_trans_body2503 = frozenset([1])
    FOLLOW_transaction_in_trans_body2507 = frozenset([1])
    FOLLOW_network_send_in_trans_body2511 = frozenset([1])
    FOLLOW_network_mcast_in_trans_body2515 = frozenset([1])
    FOLLOW_network_bcast_in_trans_body2519 = frozenset([1])
    FOLLOW_NEXT_in_next_trans2537 = frozenset([77])
    FOLLOW_OCBRACE_in_next_trans2539 = frozenset([22, 96])
    FOLLOW_trans_in_next_trans2541 = frozenset([22, 96])
    FOLLOW_CCBRACE_in_next_trans2544 = frozenset([1])
    FOLLOW_BREAK_in_next_break2565 = frozenset([83])
    FOLLOW_SEMICOLON_in_next_break2567 = frozenset([1])
    FOLLOW_assignment_in_expressions2583 = frozenset([1])
    FOLLOW_conditional_in_expressions2587 = frozenset([1])
    FOLLOW_object_block_in_expressions2591 = frozenset([1])
    FOLLOW_set_block_in_expressions2595 = frozenset([1])
    FOLLOW_internal_event_block_in_expressions2599 = frozenset([1])
    FOLLOW_msg_stall_in_expressions2603 = frozenset([1])
    FOLLOW_set_access_in_expressions2607 = frozenset([1])
    FOLLOW_undefine_in_expressions2611 = frozenset([1])
    FOLLOW_process_finalident_in_assignment2618 = frozenset([41])
    FOLLOW_EQUALSIGN_in_assignment2620 = frozenset([14, 48, 55, 74])
    FOLLOW_assign_types_in_assignment2622 = frozenset([83])
    FOLLOW_SEMICOLON_in_assignment2624 = frozenset([1])
    FOLLOW_object_expr_in_assign_types2646 = frozenset([1])
    FOLLOW_message_constr_in_assign_types2650 = frozenset([1])
    FOLLOW_math_op_in_assign_types2654 = frozenset([1])
    FOLLOW_set_func_in_assign_types2658 = frozenset([1])
    FOLLOW_INT_in_assign_types2662 = frozenset([1])
    FOLLOW_BOOL_in_assign_types2666 = frozenset([1])
    FOLLOW_NID_in_assign_types2670 = frozenset([1])
    FOLLOW_val_range_in_math_op2681 = frozenset([63, 79])
    FOLLOW_set_in_math_op2683 = frozenset([48, 55])
    FOLLOW_val_range_in_math_op2691 = frozenset([1])
    FOLLOW_STALL_in_msg_stall2697 = frozenset([83])
    FOLLOW_SEMICOLON_in_msg_stall2699 = frozenset([1])
    FOLLOW_ACCESS_in_set_access2711 = frozenset([83])
    FOLLOW_SEMICOLON_in_set_access2713 = frozenset([1])
    FOLLOW_UNDEF_in_undefine2727 = frozenset([48])
    FOLLOW_ID_in_undefine2729 = frozenset([83])
    FOLLOW_SEMICOLON_in_undefine2731 = frozenset([1])
    FOLLOW_if_stmt_in_conditional2748 = frozenset([1])
    FOLLOW_ifnot_stmt_in_conditional2752 = frozenset([1])
    FOLLOW_IF_in_if_stmt2771 = frozenset([14, 48, 55, 74, 76])
    FOLLOW_cond_comb_in_if_stmt2773 = frozenset([77])
    FOLLOW_OCBRACE_in_if_stmt2775 = frozenset([4, 11, 17, 22, 48, 50, 90, 92, 94, 107])
    FOLLOW_if_expression_in_if_stmt2777 = frozenset([22])
    FOLLOW_CCBRACE_in_if_stmt2779 = frozenset([1, 36])
    FOLLOW_ELSE_in_if_stmt2786 = frozenset([77])
    FOLLOW_OCBRACE_in_if_stmt2790 = frozenset([4, 11, 17, 22, 48, 50, 90, 92, 94, 107])
    FOLLOW_else_expression_in_if_stmt2792 = frozenset([22])
    FOLLOW_CCBRACE_in_if_stmt2794 = frozenset([1, 36])
    FOLLOW_IF_in_ifnot_stmt2900 = frozenset([69])
    FOLLOW_NEG_in_ifnot_stmt2902 = frozenset([14, 48, 55, 74, 76])
    FOLLOW_cond_comb_in_ifnot_stmt2904 = frozenset([77])
    FOLLOW_OCBRACE_in_ifnot_stmt2906 = frozenset([4, 11, 17, 22, 48, 50, 90, 92, 94, 107])
    FOLLOW_if_expression_in_ifnot_stmt2908 = frozenset([22])
    FOLLOW_CCBRACE_in_ifnot_stmt2910 = frozenset([1, 36])
    FOLLOW_ELSE_in_ifnot_stmt2917 = frozenset([77])
    FOLLOW_OCBRACE_in_ifnot_stmt2921 = frozenset([4, 11, 17, 22, 48, 50, 90, 92, 94, 107])
    FOLLOW_else_expression_in_ifnot_stmt2923 = frozenset([22])
    FOLLOW_CCBRACE_in_ifnot_stmt2925 = frozenset([1, 36])
    FOLLOW_exprwbreak_in_if_expression3026 = frozenset([1, 4, 11, 17, 48, 50, 90, 92, 94, 107])
    FOLLOW_exprwbreak_in_else_expression3041 = frozenset([1, 4, 11, 17, 48, 50, 90, 92, 94, 107])
    FOLLOW_expressions_in_exprwbreak3056 = frozenset([1])
    FOLLOW_network_send_in_exprwbreak3060 = frozenset([1])
    FOLLOW_network_mcast_in_exprwbreak3064 = frozenset([1])
    FOLLOW_network_bcast_in_exprwbreak3068 = frozenset([1])
    FOLLOW_transaction_in_exprwbreak3072 = frozenset([1])
    FOLLOW_next_break_in_exprwbreak3076 = frozenset([1])
    FOLLOW_cond_rel_in_cond_comb3090 = frozenset([1, 100, 121])
    FOLLOW_combinatorial_operator_in_cond_comb3093 = frozenset([14, 48, 55, 74, 76])
    FOLLOW_cond_rel_in_cond_comb3095 = frozenset([1, 100, 121])
    FOLLOW_OBRACE_in_cond_rel3112 = frozenset([14, 48, 55, 74, 76])
    FOLLOW_cond_sel_in_cond_rel3115 = frozenset([1, 21])
    FOLLOW_CBRACE_in_cond_rel3117 = frozenset([1, 21])
    FOLLOW_cond_type_expr_in_cond_sel3141 = frozenset([1, 99, 101, 102, 103, 104, 105])
    FOLLOW_relational_operator_in_cond_sel3144 = frozenset([14, 48, 55, 74])
    FOLLOW_cond_type_expr_in_cond_sel3146 = frozenset([1, 99, 101, 102, 103, 104, 105])
    FOLLOW_cond_types_in_cond_type_expr3166 = frozenset([1, 63, 67, 79])
    FOLLOW_set_in_cond_type_expr3169 = frozenset([14, 48, 55, 74])
    FOLLOW_cond_types_in_cond_type_expr3181 = frozenset([1, 63, 67, 79])
    FOLLOW_object_expr_in_cond_types3202 = frozenset([1])
    FOLLOW_set_func_in_cond_types3206 = frozenset([1])
    FOLLOW_INT_in_cond_types3210 = frozenset([1])
    FOLLOW_BOOL_in_cond_types3214 = frozenset([1])
    FOLLOW_NID_in_cond_types3218 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("ProtoCCLexer", ProtoCCParser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
