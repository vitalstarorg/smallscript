/*
History
2024/07/24
      SmallScript is adapted from https://github.com/antlr/grammars-v4/blob/master/smalltalk/Smalltalk.g4
2015/01/18 James Ladd (object@redline.st)
      Converted to ANTLR 4 by James Ladd (Redline Smalltalk Project http://redline.st).
      Adapted from the Amber Smalltalk grammar parser.pegjs
*/

grammar SmallScript;

smallscript: closure EOF;
closure: blkparamlst? ws? temps? ws? exprs | blkparamlst? ws? exprs;
blk: BLK_START ws? closure? BLK_END;
temps: PIPE (ws? tempvar)+ ws? PIPE;
tempvar: IDENT;
blkparamlst: (ws? blkparam)+ ws? PIPE;
blkparam: BLK_PARAM;
expr: assign | chain | kwhead | binhead | primitive;
exprs: expr exprlst* ws? SEMI? ws?;
exprlst: (SEMI)+ ws? expr;
unaryhead: operand ws? unarytail?;
unarytail: unarymsg ws? unarytail? ws?;
unarymsg: ws? unaryop;
unaryop: IDENT;
operand: literal | var | subexpr;
kwhead: unaryhead kwmsg;
kwmsg: ws? (kwpair ws?)+;
kwpair: ptkey ws? binhead ws?;
ptkey: KEYWORD;
binhead: unaryhead bintail?;
bintail: binmsg bintail?;
binmsg: ws? binop ws? (unaryhead | operand);
binop: BIN_OP;
//subexpr: OPEN_PAREN ws? expr ws? CLOSE_PAREN;
subexpr: OPEN_PAREN ws? (kwhead | binhead | primitive) ws? CLOSE_PAREN;
chain: (kwhead | binhead) (ws? ptfin ws? msg)+;
ptfin: PIPE;
msg: kwmsg| unarytail? ws? bintail?;
assign: ref ws? ASSIGN ws? expr;

literal: rtlit | parselit;
rtlit: dynarr | blk;
dynarr: DYNARR_START ws? ((operand | dynarr) ws?)* DYNARR_END;
    //rtlit: dyndict | dynarr | blk;
    //dyndict: DYNDICT_START ws? exprs? ws? DYNARR_END;   # not working
    //dynarr: DYNARR_START ws? exprs? ws? DYNARR_END;     # not working

parselit: baresym | num | char | litarr | string;
litarr: LITARR_START litarrcnt  CLOSE_PAREN;
litarrcnt: ws? ((parselit | baresym) ws?)*;
    //litarrcnt: ws? ((parselit | symbol) ws?)* CLOSE_PAREN;
    //litarrcnt: ws? ((parselit | barelitarr | symbol) ws?)* CLOSE_PAREN;
    //barelitarr: OPEN_PAREN litarrcnt;

keywords: KEYWORD+;
symbol: (IDENT | BIN_OP) | KEYWORD+ | string;
baresym: HASH IDENT;
char: CHAR;
string: (STRING | HEREDOC);
primitive: P_START primkey ws? exprs P_END ws?;
primkey: KEYWORD;
//primtxt: STRING;
var: ref;
ref: (IDENT | primitive);
ws: (WS | COMMENT)+;

//num: numberExp | hex_ | stFloat | stInteger;
//numberExp: (stFloat | stInteger) EXP stInteger;
//hex_: MINUS? HEX HEXDIGIT+;
//stInteger: MINUS? DIGIT+;
//stFloat: MINUS? DIGIT+ PERIOD DIGIT+;

// "1+2-3" not working, "1+2- 3" working.
//num: NUMEXP | HEX_ | ST_FLOAT | ST_INT;
num: ssHex | ssFloat | ssInt;
ssFloat: NUMEXP | ST_FLOAT;
NUMEXP: (ST_FLOAT | ST_INT) EXP ST_INT;
ssHex: HEX_;
HEX_: MINUS? HEX HEXDIGIT+;
ssInt: ST_INT;
ST_INT: MINUS? DIGIT+;
ST_FLOAT: MINUS? DIGIT+ PERIOD DIGIT+;

P_START: LT (SPACES | CR)*;
P_END: (SPACES | CR)* GT;
//STRING: '\'' (.)*? '\'';
STRING: '\'' (.)*? '\'' | '"' (.)*? '"';
WS: (SPACES | CR)+;
SPACES: ([ \t])+;
CR: ([\r\n])+;
COMMENT: ('//' '/'* (.)*? CR | HEREDOC CR)+;
HEREDOC:
'\'\'\'' (.)*? '\'\'\'';

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
IDENT: [a-zA-Z_]+ ([a-zA-Z0-9_] | PERIOD)*;
CARROT: '^';
COLON: ':';
ASSIGN: ':=';
HASH: '#';
DOLLAR: '$';
EXP: 'e';
HEX: '0x';
LITARR_START: '#(';
DYNARR_START: '#{';
//DYNDICT_START: '{';
DYNARR_END: '}';
DIGIT: [0-9];
HEXDIGIT: [0-9a-fA-F];
KEYWORD: IDENT COLON;
BLK_PARAM: COLON IDENT;
CHAR: DOLLAR (HEXDIGIT+ | DOLLAR);