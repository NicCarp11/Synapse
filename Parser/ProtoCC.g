grammar ProtoCC;

options {
    language=Python3;
    output=AST;
    k=3;
}

tokens {
	ARCH	= 'Architecture' ;
	ARRAY	= 'array' ;
	AWAIT	= 'await' ;
	BOOLID	= 'bool' ;
	BREAK	= 'break' ;
	CACHE	= 'Cache' ;
	CBRACE	= ')' ;
	CCBRACE	= '}' ;
	CEBRACE	= ']' ;
	COMMA	= ',' ;
	CONSTANT	= '#' ;
	DATA	= 'Data' ;
	DDOT	= ':' ;
	DIR	= 'Directory' ;
	DOT	= '.' ;
	ELSE	= 'else' ;
	EQUALSIGN	= '=' ;
	FIFO	= 'FIFO' ;
	IF	= 'if' ;
	INTID	= 'int' ;
	MEM	= 'Memory' ;
	MINUS	= '-' ;
	MSG	= 'Message' ;
	MULT	= '*' ;
	NEG	= '!' ;
	NETWORK	= 'Network' ;
	NEXT	= 'next' ;
	NID	= 'ID' ;
	OBRACE	= '(' ;
	OCBRACE	= '{' ;
	OEBRACE	= '[' ;
	PLUS	= '+' ;
	PROC	= 'Process' ;
	SEMICOLON	= ';' ;
	SET	= 'set' ;
	STABLE	= 'Stable' ;
	STALL	= 'stall' ;
	STATE	= 'State' ;
	UNDEF	= 'undefine' ;
	WHEN	= 'when' ;

	ACCESS_ ;
	ARCH_ ;
	ARRAY_ ;
	ASSIGN_ ;
	AWAIT_ ;
	BCAST_ ;
	BOOL_ ;
	BREAK_ ;
	CACHE_ ;
	COND_ ;
	CONSTANT_ ;
	DATA_ ;
	DIR_ ;
	ELEMENT_ ;
	ENDIFELSE_ ;
	ENDIF_ ;
	ENDPROC_ ;
	ENDWHEN_ ;
	EVENT_ ;
	EVENT_ACK_ ;
	FIFO_ ;
	GUARD_ ;
	ID_ ;
	IFELSE_ ;
	IF_ ;
	INITSTATE_ ;
	INITVAL_ ;
	INT_ ;
	MACHN_ ;
	MCAST_ ;
	MEM_ ;
	MSGCSTR_ ;
	MSG_ ;
	NCOND_ ;
	NETWORK_ ;
	NEXT_ ;
	OBJSET_ ;
	PROC_ ;
	RANGE_ ;
	SEND_ ;
	SETFUNC_ ;
	SET_ ;
	STABLE_ ;
	STALL_ ;
	TRANS_ ;
	UNDEF_ ;
	WHEN_ ;
}

/*
 * RECONSTRUCTED GRAMMAR. The original ProtoCC.g of ProtoGen/HieraGen/HeteroGen
 * (Nicolai Oswald, University of Edinburgh) is not publicly available; this file
 * was rebuilt from the ANTLR 3.5.2 output ProtoCCLexer.py / ProtoCCParser.py
 * (generated 2021-04-30 from /home/tux/PycharmProjects/ProtoCCv2/Parser/ProtoCC.g).
 * Rules, AST rewrites, actions, tokens, options, rule order, line/column positions
 * and grammar token indices are recovered so that ANTLR 3.5.2 regenerates both
 * files byte-for-byte (apart from the timestamp/path header line). Comment texts
 * are placeholders and some blank lines are padding: they only reproduce the
 * original token count and line numbers. Changing the layout only changes source
 * comments and FOLLOW_* names in the generated code, not the parser's behaviour.
 *
 * Extensions (after the reconstruction):
 *   set function 'smallest': the smallest identifier in a set (SLICC smallestElement()),
 *   used to elect a new MESIF forwarder.
 */








/*------------------------------------------------------------------
 * PARSER RULES
 *------------------------------------------------------------------*/

send_function
	:	'send'
	|	'Send'
	;

mcast_function
	:	'mcast'
	|	'Mcast'
	;

bcast_function
	:	'bcast'
	|	'Bcast'
	;

internal_event_function
	:	'Event'
	;

set_function_types
	:	'add'
	|	'count'
	|	'contains'
	|	'del'
	|	'clear'
	|	'smallest'
	;

relational_operator
	:	'=='
	|	'!='
	|	'<='
	|	'>='
	|	'<'
	|	'>'
	;

combinatorial_operator
    :   '&' | '|';



WS  :   ( ' '
        | '\t'
        | '\r'
        | '\n'
        ) {$channel=HIDDEN;}
    ;

COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;

LINE_COMMENT
    : '//' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;



BOOL:   'true' | 'false';
INT :	'0'..'9'+
    ;
ACCESS: 'load' | 'store';
EVICT: 'evict';

ID  :	('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
    ;

document
	:	(const_decl | init_hw | arch_block | expressions)*
	;


declarations : int_decl | bool_decl | state_decl | data_decl | id_decl;

    const_decl : CONSTANT ID INT -> ^(CONSTANT_ ID INT);

    int_decl : INTID range ID (EQUALSIGN INT)* SEMICOLON -> ^(INT_ ID range ^(INITVAL_ INT)*);
    bool_decl : BOOLID ID (EQUALSIGN BOOL)* SEMICOLON -> ^(BOOL_ ID ^(INITVAL_ BOOL)*);

    state_decl : STATE ID SEMICOLON -> ^(INITSTATE_ ID);
    data_decl : DATA ID SEMICOLON -> ^(DATA_ ID);
    id_decl : set_decl* NID ID (EQUALSIGN set_decl* ID)* SEMICOLON -> ^(ID_ ID set_decl* ^(INITVAL_ set_decl* ID)*);

        set_decl : SET OEBRACE val_range CEBRACE -> ^(SET_ val_range);
        range : OEBRACE val_range DOT DOT val_range CEBRACE -> ^(RANGE_ OEBRACE val_range DOT DOT val_range CEBRACE);
        val_range : INT | ID;

    array_decl : ARRAY range;
    fifo_decl: FIFO range;

/* Hardware */
init_hw : network_block | machines | message_block;
    object_block : object_expr SEMICOLON -> object_expr;
    object_expr : object_id | object_func;
    object_id:  ID -> ^(ID);
    object_func : ID DOT object_idres (OBRACE object_expr* (COMMA object_expr)* CBRACE)* ->
        ^(ID DOT object_idres (OBRACE object_expr* (COMMA object_expr)* CBRACE)*);
    object_idres:  ID | NID;

    // Machines
    machines : cache_block | dir_block | mem_block;
        cache_block : CACHE OCBRACE declarations* CCBRACE objset_decl* ID SEMICOLON ->
            ^(CACHE_ ID objset_decl* declarations*);
        dir_block : DIR OCBRACE declarations* CCBRACE objset_decl* ID SEMICOLON ->
            ^(DIR_ ID objset_decl* declarations*);
        mem_block : MEM OCBRACE declarations* CCBRACE objset_decl* ID SEMICOLON ->
            ^(MEM_ ID objset_decl* declarations*);

        objset_decl : SET OEBRACE val_range CEBRACE -> ^(OBJSET_ val_range);

    /* Network */
    network_block : NETWORK OCBRACE network_element* CCBRACE SEMICOLON -> ^(NETWORK_ network_element*);
        element_type : 'Ordered' | 'Unordered';
        network_element : element_type ID SEMICOLON -> ^(ELEMENT_ element_type ID);
    network_send : ID DOT send_function OBRACE ID CBRACE SEMICOLON -> ^(SEND_ ID ID);
    network_bcast: ID DOT bcast_function OBRACE ID CBRACE SEMICOLON -> ^(BCAST_ ID ID);
    network_mcast: ID DOT mcast_function OBRACE ID COMMA ID CBRACE SEMICOLON -> ^(MCAST_ ID ID ID);

    /* Messages */
    message_block : MSG ID OCBRACE declarations* CCBRACE SEMICOLON -> ^(MSG_ ID declarations*);
    message_constr : ID OBRACE message_expr* (COMMA message_expr)* CBRACE -> ^(MSGCSTR_ ID message_expr*);
    message_expr : object_expr | set_func | INT | BOOL | NID;

    /* Sets */
    set_block : set_func SEMICOLON -> set_func;
    set_func : ID DOT set_function_types OBRACE set_nest* CBRACE ->
        ^(SETFUNC_ ID DOT set_function_types OBRACE set_nest* CBRACE);
    set_nest : set_func | object_expr;


    /* Internal events */
    internal_event_block: internal_event_func SEMICOLON -> internal_event_func;
    internal_event_func: internal_event_function OBRACE ID CBRACE -> ^(EVENT_ ID) ^(EVENT_ACK_ ID);

/* Architecture */
arch_block : ARCH ID OCBRACE arch_body CCBRACE -> ^(ARCH_ ^(MACHN_ ID) arch_body);

arch_body: (stable_def | process_block)*;

stable_def : STABLE OCBRACE ID (COMMA ID)* CCBRACE -> ^(STABLE_ ID ID*);

process_block : PROC process_trans OCBRACE process_expr* CCBRACE -> ^(PROC_ process_trans process_expr* ^(ENDPROC_));
    process_trans : OBRACE ID COMMA process_events process_finalstate* CBRACE -> ^(TRANS_ ID process_events process_finalstate*);
    process_finalstate: COMMA process_finalident -> ^(process_finalident);
    process_finalident: (ID | STATE);
    process_events : (ACCESS | EVICT | ID);
    process_expr: expressions | network_send | network_mcast | network_bcast| transaction;

/* Transactions */
transaction : AWAIT OCBRACE trans* CCBRACE -> ^(AWAIT_ trans*);
    trans : WHEN ID DDOT trans_body* -> ^(WHEN_ ^(GUARD_ ID) trans_body* ENDWHEN_);
        trans_body : expressions | next_trans | next_break | transaction | network_send | network_mcast | network_bcast;
            next_trans: NEXT OCBRACE trans* CCBRACE -> ^(NEXT_ trans*);

    next_break : BREAK SEMICOLON -> ^(BREAK_);

/* Expressions */
expressions : assignment | conditional | object_block | set_block | internal_event_block | msg_stall | set_access | undefine;
assignment : process_finalident EQUALSIGN assign_types SEMICOLON-> ^(ASSIGN_ process_finalident EQUALSIGN assign_types);
    assign_types : object_expr | message_constr | math_op | set_func | INT | BOOL | NID;
    math_op : val_range (PLUS | MINUS) val_range;
msg_stall: STALL SEMICOLON -> ^(STALL_);
set_access: ACCESS SEMICOLON -> ^(ACCESS_ ACCESS);
undefine: UNDEF ID SEMICOLON -> ^(UNDEF_ ID);

/* Conditionals */
conditional: if_stmt | ifnot_stmt;
    if_stmt @init{t_else = 0}
    : IF cond_comb OCBRACE if_expression CCBRACE
    (ELSE {t_else=1} OCBRACE else_expression CCBRACE)*
    -> {t_else}? ^(IFELSE_ ^(IF_ ^(COND_ cond_comb) if_expression* ENDIF_) ^(IF_ ^(NCOND_ cond_comb) else_expression* ENDIF_))
    -> ^(IFELSE_ ^(IF_ ^(COND_ cond_comb) if_expression* ENDIF_) ^(IF_ ^(NCOND_ cond_comb) ENDIF_))
    ;

    ifnot_stmt @init{t_else = 0}
    : IF NEG cond_comb OCBRACE if_expression CCBRACE
    (ELSE {t_else=1} OCBRACE else_expression CCBRACE)*
    -> {t_else}? ^(IFELSE_ ^(IF_ ^(NCOND_ cond_comb) if_expression* ENDIF_) ^(IF_ ^(COND_ cond_comb) else_expression* ENDIF_))
    -> ^(IFELSE_ ^(IF_ ^(NCOND_ cond_comb) if_expression* ENDIF_) ^(IF_ ^(COND_ cond_comb) ENDIF_))
    ;

        if_expression: exprwbreak*;
        else_expression: exprwbreak*;
        exprwbreak: expressions | network_send | network_mcast | network_bcast | transaction | next_break;
        cond_comb: cond_rel (combinatorial_operator cond_rel)*;
        cond_rel : OBRACE* cond_sel CBRACE* -> cond_sel;
            cond_sel : cond_type_expr (relational_operator cond_type_expr)*;
            cond_type_expr: cond_types ((PLUS | MINUS | MULT) cond_types)*;
            cond_types : object_expr | set_func | INT | BOOL | NID;
