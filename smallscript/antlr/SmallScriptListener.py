# Generated from SmallScript.g4 by ANTLR 4.13.1
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


    # Enter a parse tree produced by SmallScriptParser#sequence.
    def enterSequence(self, ctx:SmallScriptParser.SequenceContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#sequence.
    def exitSequence(self, ctx:SmallScriptParser.SequenceContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ws.
    def enterWs(self, ctx:SmallScriptParser.WsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ws.
    def exitWs(self, ctx:SmallScriptParser.WsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#temps.
    def enterTemps(self, ctx:SmallScriptParser.TempsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#temps.
    def exitTemps(self, ctx:SmallScriptParser.TempsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#tempVar.
    def enterTempVar(self, ctx:SmallScriptParser.TempVarContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#tempVar.
    def exitTempVar(self, ctx:SmallScriptParser.TempVarContext):
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


    # Enter a parse tree produced by SmallScriptParser#exprList.
    def enterExprList(self, ctx:SmallScriptParser.ExprListContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#exprList.
    def exitExprList(self, ctx:SmallScriptParser.ExprListContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#cascade.
    def enterCascade(self, ctx:SmallScriptParser.CascadeContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#cascade.
    def exitCascade(self, ctx:SmallScriptParser.CascadeContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ptFin.
    def enterPtFin(self, ctx:SmallScriptParser.PtFinContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ptFin.
    def exitPtFin(self, ctx:SmallScriptParser.PtFinContext):
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


    # Enter a parse tree produced by SmallScriptParser#ref.
    def enterRef(self, ctx:SmallScriptParser.RefContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ref.
    def exitRef(self, ctx:SmallScriptParser.RefContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binHead.
    def enterBinHead(self, ctx:SmallScriptParser.BinHeadContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binHead.
    def exitBinHead(self, ctx:SmallScriptParser.BinHeadContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unaryHead.
    def enterUnaryHead(self, ctx:SmallScriptParser.UnaryHeadContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unaryHead.
    def exitUnaryHead(self, ctx:SmallScriptParser.UnaryHeadContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#kwHead.
    def enterKwHead(self, ctx:SmallScriptParser.KwHeadContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#kwHead.
    def exitKwHead(self, ctx:SmallScriptParser.KwHeadContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#kwMsg.
    def enterKwMsg(self, ctx:SmallScriptParser.KwMsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#kwMsg.
    def exitKwMsg(self, ctx:SmallScriptParser.KwMsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#kwPair.
    def enterKwPair(self, ctx:SmallScriptParser.KwPairContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#kwPair.
    def exitKwPair(self, ctx:SmallScriptParser.KwPairContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#ptKey.
    def enterPtKey(self, ctx:SmallScriptParser.PtKeyContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#ptKey.
    def exitPtKey(self, ctx:SmallScriptParser.PtKeyContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#operand.
    def enterOperand(self, ctx:SmallScriptParser.OperandContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#operand.
    def exitOperand(self, ctx:SmallScriptParser.OperandContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#subexpr.
    def enterSubexpr(self, ctx:SmallScriptParser.SubexprContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#subexpr.
    def exitSubexpr(self, ctx:SmallScriptParser.SubexprContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#lit.
    def enterLit(self, ctx:SmallScriptParser.LitContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#lit.
    def exitLit(self, ctx:SmallScriptParser.LitContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#rtLit.
    def enterRtLit(self, ctx:SmallScriptParser.RtLitContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#rtLit.
    def exitRtLit(self, ctx:SmallScriptParser.RtLitContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#blk.
    def enterBlk(self, ctx:SmallScriptParser.BlkContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#blk.
    def exitBlk(self, ctx:SmallScriptParser.BlkContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#blkParamList.
    def enterBlkParamList(self, ctx:SmallScriptParser.BlkParamListContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#blkParamList.
    def exitBlkParamList(self, ctx:SmallScriptParser.BlkParamListContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#blkParam.
    def enterBlkParam(self, ctx:SmallScriptParser.BlkParamContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#blkParam.
    def exitBlkParam(self, ctx:SmallScriptParser.BlkParamContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#dynDict.
    def enterDynDict(self, ctx:SmallScriptParser.DynDictContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#dynDict.
    def exitDynDict(self, ctx:SmallScriptParser.DynDictContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#dynArr.
    def enterDynArr(self, ctx:SmallScriptParser.DynArrContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#dynArr.
    def exitDynArr(self, ctx:SmallScriptParser.DynArrContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#parseLit.
    def enterParseLit(self, ctx:SmallScriptParser.ParseLitContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#parseLit.
    def exitParseLit(self, ctx:SmallScriptParser.ParseLitContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#num.
    def enterNum(self, ctx:SmallScriptParser.NumContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#num.
    def exitNum(self, ctx:SmallScriptParser.NumContext):
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


    # Enter a parse tree produced by SmallScriptParser#primKey.
    def enterPrimKey(self, ctx:SmallScriptParser.PrimKeyContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#primKey.
    def exitPrimKey(self, ctx:SmallScriptParser.PrimKeyContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#primText.
    def enterPrimText(self, ctx:SmallScriptParser.PrimTextContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#primText.
    def exitPrimText(self, ctx:SmallScriptParser.PrimTextContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#bareSym.
    def enterBareSym(self, ctx:SmallScriptParser.BareSymContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#bareSym.
    def exitBareSym(self, ctx:SmallScriptParser.BareSymContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#symbol.
    def enterSymbol(self, ctx:SmallScriptParser.SymbolContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#symbol.
    def exitSymbol(self, ctx:SmallScriptParser.SymbolContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#litArray.
    def enterLitArray(self, ctx:SmallScriptParser.LitArrayContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#litArray.
    def exitLitArray(self, ctx:SmallScriptParser.LitArrayContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#litArrayRest.
    def enterLitArrayRest(self, ctx:SmallScriptParser.LitArrayRestContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#litArrayRest.
    def exitLitArrayRest(self, ctx:SmallScriptParser.LitArrayRestContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#bareLitArr.
    def enterBareLitArr(self, ctx:SmallScriptParser.BareLitArrContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#bareLitArr.
    def exitBareLitArr(self, ctx:SmallScriptParser.BareLitArrContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unaryTail.
    def enterUnaryTail(self, ctx:SmallScriptParser.UnaryTailContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unaryTail.
    def exitUnaryTail(self, ctx:SmallScriptParser.UnaryTailContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unaryMsg.
    def enterUnaryMsg(self, ctx:SmallScriptParser.UnaryMsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unaryMsg.
    def exitUnaryMsg(self, ctx:SmallScriptParser.UnaryMsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#unaryOp.
    def enterUnaryOp(self, ctx:SmallScriptParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#unaryOp.
    def exitUnaryOp(self, ctx:SmallScriptParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#keywords.
    def enterKeywords(self, ctx:SmallScriptParser.KeywordsContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#keywords.
    def exitKeywords(self, ctx:SmallScriptParser.KeywordsContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#var.
    def enterVar(self, ctx:SmallScriptParser.VarContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#var.
    def exitVar(self, ctx:SmallScriptParser.VarContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binTail.
    def enterBinTail(self, ctx:SmallScriptParser.BinTailContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binTail.
    def exitBinTail(self, ctx:SmallScriptParser.BinTailContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binMsg.
    def enterBinMsg(self, ctx:SmallScriptParser.BinMsgContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binMsg.
    def exitBinMsg(self, ctx:SmallScriptParser.BinMsgContext):
        pass


    # Enter a parse tree produced by SmallScriptParser#binOp.
    def enterBinOp(self, ctx:SmallScriptParser.BinOpContext):
        pass

    # Exit a parse tree produced by SmallScriptParser#binOp.
    def exitBinOp(self, ctx:SmallScriptParser.BinOpContext):
        pass



del SmallScriptParser