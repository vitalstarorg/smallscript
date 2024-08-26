# Generated from SmallScript.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SmallScriptParser import SmallScriptParser
else:
    from SmallScriptParser import SmallScriptParser

# This class defines a complete listener for a parse tree produced by SmallScriptParser.
class SmallScriptListener(ParseTreeListener):

    # Enter a parse tree produced by SmallScriptParser#smallscript.
    def enterSmallscript(self, ctx:SmallScriptParser.SmallscriptContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#smallscript.
    def exitSmallscript(self, ctx:SmallScriptParser.SmallscriptContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#closure.
    def enterClosure(self, ctx:SmallScriptParser.ClosureContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#closure.
    def exitClosure(self, ctx:SmallScriptParser.ClosureContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#blk.
    def enterBlk(self, ctx:SmallScriptParser.BlkContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#blk.
    def exitBlk(self, ctx:SmallScriptParser.BlkContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#temps.
    def enterTemps(self, ctx:SmallScriptParser.TempsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#temps.
    def exitTemps(self, ctx:SmallScriptParser.TempsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#tempvar.
    def enterTempvar(self, ctx:SmallScriptParser.TempvarContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#tempvar.
    def exitTempvar(self, ctx:SmallScriptParser.TempvarContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#blkparamlst.
    def enterBlkparamlst(self, ctx:SmallScriptParser.BlkparamlstContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#blkparamlst.
    def exitBlkparamlst(self, ctx:SmallScriptParser.BlkparamlstContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#blkparam.
    def enterBlkparam(self, ctx:SmallScriptParser.BlkparamContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#blkparam.
    def exitBlkparam(self, ctx:SmallScriptParser.BlkparamContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#expr.
    def enterExpr(self, ctx:SmallScriptParser.ExprContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#expr.
    def exitExpr(self, ctx:SmallScriptParser.ExprContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#exprs.
    def enterExprs(self, ctx:SmallScriptParser.ExprsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#exprs.
    def exitExprs(self, ctx:SmallScriptParser.ExprsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#exprlst.
    def enterExprlst(self, ctx:SmallScriptParser.ExprlstContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#exprlst.
    def exitExprlst(self, ctx:SmallScriptParser.ExprlstContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unaryhead.
    def enterUnaryhead(self, ctx:SmallScriptParser.UnaryheadContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unaryhead.
    def exitUnaryhead(self, ctx:SmallScriptParser.UnaryheadContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unarytail.
    def enterUnarytail(self, ctx:SmallScriptParser.UnarytailContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unarytail.
    def exitUnarytail(self, ctx:SmallScriptParser.UnarytailContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unarymsg.
    def enterUnarymsg(self, ctx:SmallScriptParser.UnarymsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unarymsg.
    def exitUnarymsg(self, ctx:SmallScriptParser.UnarymsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unaryop.
    def enterUnaryop(self, ctx:SmallScriptParser.UnaryopContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unaryop.
    def exitUnaryop(self, ctx:SmallScriptParser.UnaryopContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#operand.
    def enterOperand(self, ctx:SmallScriptParser.OperandContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#operand.
    def exitOperand(self, ctx:SmallScriptParser.OperandContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#kwhead.
    def enterKwhead(self, ctx:SmallScriptParser.KwheadContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#kwhead.
    def exitKwhead(self, ctx:SmallScriptParser.KwheadContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#kwmsg.
    def enterKwmsg(self, ctx:SmallScriptParser.KwmsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#kwmsg.
    def exitKwmsg(self, ctx:SmallScriptParser.KwmsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#kwpair.
    def enterKwpair(self, ctx:SmallScriptParser.KwpairContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#kwpair.
    def exitKwpair(self, ctx:SmallScriptParser.KwpairContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ptkey.
    def enterPtkey(self, ctx:SmallScriptParser.PtkeyContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ptkey.
    def exitPtkey(self, ctx:SmallScriptParser.PtkeyContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binhead.
    def enterBinhead(self, ctx:SmallScriptParser.BinheadContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binhead.
    def exitBinhead(self, ctx:SmallScriptParser.BinheadContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#bintail.
    def enterBintail(self, ctx:SmallScriptParser.BintailContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#bintail.
    def exitBintail(self, ctx:SmallScriptParser.BintailContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binmsg.
    def enterBinmsg(self, ctx:SmallScriptParser.BinmsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binmsg.
    def exitBinmsg(self, ctx:SmallScriptParser.BinmsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binop.
    def enterBinop(self, ctx:SmallScriptParser.BinopContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binop.
    def exitBinop(self, ctx:SmallScriptParser.BinopContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#subexpr.
    def enterSubexpr(self, ctx:SmallScriptParser.SubexprContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#subexpr.
    def exitSubexpr(self, ctx:SmallScriptParser.SubexprContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#chain.
    def enterChain(self, ctx:SmallScriptParser.ChainContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#chain.
    def exitChain(self, ctx:SmallScriptParser.ChainContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ptfin.
    def enterPtfin(self, ctx:SmallScriptParser.PtfinContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ptfin.
    def exitPtfin(self, ctx:SmallScriptParser.PtfinContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#msg.
    def enterMsg(self, ctx:SmallScriptParser.MsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#msg.
    def exitMsg(self, ctx:SmallScriptParser.MsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#assign.
    def enterAssign(self, ctx:SmallScriptParser.AssignContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#assign.
    def exitAssign(self, ctx:SmallScriptParser.AssignContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#literal.
    def enterLiteral(self, ctx:SmallScriptParser.LiteralContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#literal.
    def exitLiteral(self, ctx:SmallScriptParser.LiteralContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#rtlit.
    def enterRtlit(self, ctx:SmallScriptParser.RtlitContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#rtlit.
    def exitRtlit(self, ctx:SmallScriptParser.RtlitContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#dynarr.
    def enterDynarr(self, ctx:SmallScriptParser.DynarrContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#dynarr.
    def exitDynarr(self, ctx:SmallScriptParser.DynarrContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#parselit.
    def enterParselit(self, ctx:SmallScriptParser.ParselitContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#parselit.
    def exitParselit(self, ctx:SmallScriptParser.ParselitContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#litarr.
    def enterLitarr(self, ctx:SmallScriptParser.LitarrContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#litarr.
    def exitLitarr(self, ctx:SmallScriptParser.LitarrContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#litarrcnt.
    def enterLitarrcnt(self, ctx:SmallScriptParser.LitarrcntContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#litarrcnt.
    def exitLitarrcnt(self, ctx:SmallScriptParser.LitarrcntContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#keywords.
    def enterKeywords(self, ctx:SmallScriptParser.KeywordsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#keywords.
    def exitKeywords(self, ctx:SmallScriptParser.KeywordsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#symbol.
    def enterSymbol(self, ctx:SmallScriptParser.SymbolContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#symbol.
    def exitSymbol(self, ctx:SmallScriptParser.SymbolContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#baresym.
    def enterBaresym(self, ctx:SmallScriptParser.BaresymContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#baresym.
    def exitBaresym(self, ctx:SmallScriptParser.BaresymContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#char.
    def enterChar(self, ctx:SmallScriptParser.CharContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#char.
    def exitChar(self, ctx:SmallScriptParser.CharContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#string.
    def enterString(self, ctx:SmallScriptParser.StringContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#string.
    def exitString(self, ctx:SmallScriptParser.StringContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#primitive.
    def enterPrimitive(self, ctx:SmallScriptParser.PrimitiveContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#primitive.
    def exitPrimitive(self, ctx:SmallScriptParser.PrimitiveContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#primkey.
    def enterPrimkey(self, ctx:SmallScriptParser.PrimkeyContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#primkey.
    def exitPrimkey(self, ctx:SmallScriptParser.PrimkeyContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#primtxt.
    def enterPrimtxt(self, ctx:SmallScriptParser.PrimtxtContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#primtxt.
    def exitPrimtxt(self, ctx:SmallScriptParser.PrimtxtContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#var.
    def enterVar(self, ctx:SmallScriptParser.VarContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#var.
    def exitVar(self, ctx:SmallScriptParser.VarContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ref.
    def enterRef(self, ctx:SmallScriptParser.RefContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ref.
    def exitRef(self, ctx:SmallScriptParser.RefContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ws.
    def enterWs(self, ctx:SmallScriptParser.WsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ws.
    def exitWs(self, ctx:SmallScriptParser.WsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#num.
    def enterNum(self, ctx:SmallScriptParser.NumContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#num.
    def exitNum(self, ctx:SmallScriptParser.NumContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ssFloat.
    def enterSsFloat(self, ctx:SmallScriptParser.SsFloatContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ssFloat.
    def exitSsFloat(self, ctx:SmallScriptParser.SsFloatContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ssHex.
    def enterSsHex(self, ctx:SmallScriptParser.SsHexContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ssHex.
    def exitSsHex(self, ctx:SmallScriptParser.SsHexContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ssInt.
    def enterSsInt(self, ctx:SmallScriptParser.SsIntContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ssInt.
    def exitSsInt(self, ctx:SmallScriptParser.SsIntContext):
        pass



del SmallScriptParser