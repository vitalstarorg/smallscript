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
temps: PIPE (ws? tempVar)+ ws? PIPE;
tempVar: IDENT;

//statements
//    : answer ws?                        # StatementAnswer
//    | exprs ws? PERIOD ws? answer # StatementExpressionsAnswer
//    | exprs PERIOD? ws?           # StatementExpressions
//    ;
//answer: CARROT ws? expr ws? PERIOD?;
expr: assign | cascade | kwHead | binHead | primitive;
exprs: expr exprList*;
exprList: PERIOD ws? expr;
cascade: (kwHead | binHead) (ws? ptFin ws? msg)+;
ptFin: SEMI;
msg: kwMsg| unaryTail? ws? binTail?;
assign: ref ws? ASSIGN ws? expr;
ref: IDENT;
binHead: unaryHead binTail?;
unaryHead: operand ws? unaryTail?;
kwHead: unaryHead kwMsg;
kwMsg: ws? (kwPair ws?)+;
kwPair: ptKey ws? binHead ws?;
ptKey: KEYWORD;
operand: lit | var | subexpr;
subexpr: OPEN_PAREN ws? expr ws? CLOSE_PAREN;
lit: rtLit | parseLit;
rtLit: dynDict | dynArr | blk;
blk: BLK_START blkParamList? ws? sequence? BLK_END;
blkParamList: (ws? blkParam)+ ws? PIPE;
blkParam: BLK_PARAM;
dynDict: DYNDICT_START ws? exprs? ws? DYNARR_END;
dynArr: DYNARR_START ws? exprs? ws? DYNARR_END;
parseLit: bareSym | num | char | litArray | string ;
num: NUMEXP | HEX_ | ST_FLOAT | ST_INT;
NUMEXP: (ST_FLOAT | ST_INT) EXP ST_INT;
char: CHAR;
HEX_: MINUS? HEX HEXDIGIT+;
ST_INT: MINUS? DIGIT+;
ST_FLOAT: MINUS? DIGIT+ PERIOD DIGIT+;
string: STRING;
primitive: P_START primKey ws? primText P_END;
primKey: KEYWORD;
primText: STRING;
P_START: LT SEP*;
P_END: SEP* GT;
bareSym: HASH IDENT;
symbol: (IDENT | BIN_OP) | KEYWORD+ | string;
litArray: LITARR_START litArrayRest;
litArrayRest: ws? ((parseLit | bareLitArr | symbol) ws?)* CLOSE_PAREN;
bareLitArr: OPEN_PAREN litArrayRest;
unaryTail: unaryMsg ws? unaryTail? ws?;
unaryMsg: ws? unaryOp;
unaryOp: IDENT;
keywords: KEYWORD+;
var: ref;
binTail: binMsg binTail?;
binMsg: ws? binOp ws? (unaryHead | operand);
binOp: BIN_OP;

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