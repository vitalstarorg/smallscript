# Generated from SmallScript.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SmallScriptParser import SmallScriptParser
else:
    from SmallScriptParser import SmallScriptParser

# This class defines a complete generic visitor for a parse tree produced by SmallScriptParser.

class SmallScriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SmallScriptParser#smallscript.
    def visitSmallscript(self, ctx:SmallScriptParser.SmallscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#closure.
    def visitClosure(self, ctx:SmallScriptParser.ClosureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#blk.
    def visitBlk(self, ctx:SmallScriptParser.BlkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#temps.
    def visitTemps(self, ctx:SmallScriptParser.TempsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#tempvar.
    def visitTempvar(self, ctx:SmallScriptParser.TempvarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#blkparamlst.
    def visitBlkparamlst(self, ctx:SmallScriptParser.BlkparamlstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#blkparam.
    def visitBlkparam(self, ctx:SmallScriptParser.BlkparamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#expr.
    def visitExpr(self, ctx:SmallScriptParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#exprs.
    def visitExprs(self, ctx:SmallScriptParser.ExprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#exprlst.
    def visitExprlst(self, ctx:SmallScriptParser.ExprlstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#unaryhead.
    def visitUnaryhead(self, ctx:SmallScriptParser.UnaryheadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#unarytail.
    def visitUnarytail(self, ctx:SmallScriptParser.UnarytailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#unarymsg.
    def visitUnarymsg(self, ctx:SmallScriptParser.UnarymsgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#unaryop.
    def visitUnaryop(self, ctx:SmallScriptParser.UnaryopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#operand.
    def visitOperand(self, ctx:SmallScriptParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#kwhead.
    def visitKwhead(self, ctx:SmallScriptParser.KwheadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#kwmsg.
    def visitKwmsg(self, ctx:SmallScriptParser.KwmsgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#kwpair.
    def visitKwpair(self, ctx:SmallScriptParser.KwpairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ptkey.
    def visitPtkey(self, ctx:SmallScriptParser.PtkeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#binhead.
    def visitBinhead(self, ctx:SmallScriptParser.BinheadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#bintail.
    def visitBintail(self, ctx:SmallScriptParser.BintailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#binmsg.
    def visitBinmsg(self, ctx:SmallScriptParser.BinmsgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#binop.
    def visitBinop(self, ctx:SmallScriptParser.BinopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#subexpr.
    def visitSubexpr(self, ctx:SmallScriptParser.SubexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#chain.
    def visitChain(self, ctx:SmallScriptParser.ChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ptfin.
    def visitPtfin(self, ctx:SmallScriptParser.PtfinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#msg.
    def visitMsg(self, ctx:SmallScriptParser.MsgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#assign.
    def visitAssign(self, ctx:SmallScriptParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#literal.
    def visitLiteral(self, ctx:SmallScriptParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#rtlit.
    def visitRtlit(self, ctx:SmallScriptParser.RtlitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#dynarr.
    def visitDynarr(self, ctx:SmallScriptParser.DynarrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#parselit.
    def visitParselit(self, ctx:SmallScriptParser.ParselitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#litarr.
    def visitLitarr(self, ctx:SmallScriptParser.LitarrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#litarrcnt.
    def visitLitarrcnt(self, ctx:SmallScriptParser.LitarrcntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#keywords.
    def visitKeywords(self, ctx:SmallScriptParser.KeywordsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#symbol.
    def visitSymbol(self, ctx:SmallScriptParser.SymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#baresym.
    def visitBaresym(self, ctx:SmallScriptParser.BaresymContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#char.
    def visitChar(self, ctx:SmallScriptParser.CharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#string.
    def visitString(self, ctx:SmallScriptParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#primitive.
    def visitPrimitive(self, ctx:SmallScriptParser.PrimitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#primkey.
    def visitPrimkey(self, ctx:SmallScriptParser.PrimkeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#primtxt.
    def visitPrimtxt(self, ctx:SmallScriptParser.PrimtxtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#var.
    def visitVar(self, ctx:SmallScriptParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ref.
    def visitRef(self, ctx:SmallScriptParser.RefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ws.
    def visitWs(self, ctx:SmallScriptParser.WsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#num.
    def visitNum(self, ctx:SmallScriptParser.NumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ssFloat.
    def visitSsFloat(self, ctx:SmallScriptParser.SsFloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ssHex.
    def visitSsHex(self, ctx:SmallScriptParser.SsHexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallScriptParser#ssInt.
    def visitSsInt(self, ctx:SmallScriptParser.SsIntContext):
        return self.visitChildren(ctx)



del SmallScriptParser