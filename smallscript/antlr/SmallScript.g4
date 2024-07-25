/*
History
2024/07/24
      SmallScript is adapted from https://github.com/antlr/grammars-v4/blob/master/smalltalk/Smalltalk.g4
2015/01/18 James Ladd (object@redline.st)
      Converted to ANTLR 4 by James Ladd (Redline Smalltalk Project http://redline.st).
      Adapted from the Amber Smalltalk grammar parser.pegjs
*/

grammar SmallScript;

smallscript: sequence EOF;
//sequence: temps ws? statements? | ws? statements;
sequence: temps ws? exprs | ws? exprs;
ws: (SEP | COMMENT)+;
temps: PIPE (ws? tempvar)+ ws? PIPE;
tempvar: IDENT;

//statements
//    : answer ws?                        # StatementAnswer
//    | exprs ws? PERIOD ws? answer # StatementExpressionsAnswer
//    | exprs PERIOD? ws?           # StatementExpressions
//    ;
//answer: CARROT ws? expr ws? PERIOD?;
expr: assign | cascade | kwhead | binhead | primitive;
exprs: expr exprlst*;
exprlst: PERIOD ws? expr;
cascade: (kwhead | binhead) (ws? ptfin ws? msg)+;
ptfin: SEMI;
msg: kwmsg| unarytail? ws? bintail?;
assign: ref ws? ASSIGN ws? expr;
ref: IDENT;
binhead: unaryhead bintail?;
unaryhead: operand ws? unarytail?;
kwhead: unaryhead kwmsg;
kwmsg: ws? (kwpair ws?)+;
kwpair: ptkey ws? binhead ws?;
ptkey: KEYWORD;
operand: lit | var | subexpr;
subexpr: OPEN_PAREN ws? expr ws? CLOSE_PAREN;
lit: rtlit | parselit;
rtlit: dyndict | dynarr | blk;
blk: BLK_START blkparamlst? ws? sequence? BLK_END;
blkparamlst: (ws? blkparam)+ ws? PIPE;
blkparam: BLK_PARAM;
dyndict: DYNDICT_START ws? exprs? ws? DYNARR_END;
dynarr: DYNARR_START ws? exprs? ws? DYNARR_END;
parselit: baresym | num | char | litarr | string ;
num: NUMEXP | HEX_ | ST_FLOAT | ST_INT;
NUMEXP: (ST_FLOAT | ST_INT) EXP ST_INT;
char: CHAR;
HEX_: MINUS? HEX HEXDIGIT+;
ST_INT: MINUS? DIGIT+;
ST_FLOAT: MINUS? DIGIT+ PERIOD DIGIT+;
string: STRING;
primitive: P_START primkey ws? primtxt P_END;
primkey: KEYWORD;
primtxt: STRING;
P_START: LT SEP*;
P_END: SEP* GT;
baresym: HASH IDENT;
symbol: (IDENT | BIN_OP) | KEYWORD+ | string;
litarr: LITARR_START litarrcnt;
litarrcnt: ws? ((parselit | barelitarr | symbol) ws?)* CLOSE_PAREN;
barelitarr: OPEN_PAREN litarrcnt;
unarytail: unarymsg ws? unarytail? ws?;
unarymsg: ws? unaryop;
unaryop: IDENT;
keywords: KEYWORD+;
var: ref;
bintail: binmsg bintail?;
binmsg: ws? binop ws? (unaryhead | operand);
binop: BIN_OP;

SEP: [ \t\r\n];
STRING: '\'' (.)*? '\'';
COMMENT: '"' (.)*? '"';
BLK_START: '[';
BLK_END: ']';
CLOSE_PAREN: ')';
OPEN_PAREN: '(';
PIPE: '|';
PERIOD: '.';
SEMI: ';';
BIN_OP: ('\\' | '+' | '*' | '/' | '=' | '>' | '<' | ',' | '@' | '%' | '~' | PIPE | '&' | '-' | '?')+;
LT: '<';
GT: '>';
MINUS: '-';
IDENT: [a-zA-Z_]+ [a-zA-Z0-9_]*;
CARROT: '^';
COLON: ':';
ASSIGN: ':=';
HASH: '#';
DOLLAR: '$';
EXP: 'e';
HEX: '16r';
LITARR_START: '#(';
DYNDICT_START: '#{';
DYNARR_END: '}';
DYNARR_START: '{';
DIGIT: [0-9];
HEXDIGIT: [0-9a-fA-F];
KEYWORD: IDENT COLON;
BLK_PARAM: COLON IDENT;
CHAR: DOLLAR (HEXDIGIT | DOLLAR);