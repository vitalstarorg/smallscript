# coding=utf-8
# Copyright 2024 Vital Star Foundation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from smallscript.antlr.SmallScriptParser import SmallScriptParser as Parser
from smallscript.antlr.SmallScriptListener import SmallScriptListener as Listener
from smallscript.SObject import Metaclass
from antlr4.tree.Tree import TerminalNode

import re
import io
import inspect
import copy

from smallscript.SObject import *
from smallscript.antlr.SmallScriptVisitor import SmallScriptVisitor
from smallscript.antlr.SmallScriptParser import SmallScriptParser
from antlr4 import RuleContext

class StepVisitor(SmallScriptVisitor):
    def visitCommon(self, cxt): return cxt.getText()
    def visitSmallscript(self, cxt): return self.visitCommon(cxt)
    def visitClosure(self, cxt): return self.visitCommon(cxt)
    def visitWs(self, cxt): return self.visitCommon(cxt)
    def visitTemps(self, cxt): return self.visitCommon(cxt)
    def visitTempvar(self, cxt): return self.visitCommon(cxt)
    def visitExpr(self, cxt): return self.visitCommon(cxt)
    def visitExprs(self, cxt): return self.visitCommon(cxt)
    def visitExprlst(self, cxt): return self.visitCommon(cxt)
    def visitCascade(self, cxt): return self.visitCommon(cxt)
    def visitPtfin(self, cxt): return self.visitCommon(cxt)
    def visitMsg(self, cxt): return self.visitCommon(cxt)
    def visitAssign(self, cxt): return self.visitCommon(cxt)
    def visitRef(self, cxt): return self.visitCommon(cxt)
    def visitBinhead(self, cxt): return self.visitCommon(cxt)
    def visitUnaryhead(self, cxt): return self.visitCommon(cxt)
    def visitKwhead(self, cxt): return self.visitCommon(cxt)
    def visitKwmsg(self, cxt): return self.visitCommon(cxt)
    def visitKwpair(self, cxt): return self.visitCommon(cxt)
    def visitPtkey(self, cxt): return self.visitCommon(cxt)
    def visitOperand(self, cxt): return self.visitCommon(cxt)
    def visitSubexpr(self, cxt): return self.visitCommon(cxt)
    def visitLiteral(self, cxt): return self.visitCommon(cxt)
    def visitRtlit(self, cxt): return self.visitCommon(cxt)
    def visitBlk(self, cxt): return self.visitCommon(cxt)
    def visitBlkparamlst(self, cxt): return self.visitCommon(cxt)
    def visitBlkparam(self, cxt): return self.visitCommon(cxt)
    def visitDyndict(self, cxt): return self.visitCommon(cxt)
    def visitDynarr(self, cxt): return self.visitCommon(cxt)
    def visitParselit(self, cxt): return self.visitCommon(cxt)
    def visitNum(self, cxt): return self.visitCommon(cxt)
    def visitChar(self, cxt): return self.visitCommon(cxt)
    def visitString(self, cxt): return self.visitCommon(cxt)
    def visitPrimitive(self, cxt): return self.visitCommon(cxt)
    def visitPrimkey(self, cxt): return self.visitCommon(cxt)
    def visitPrimtxt(self, cxt): return self.visitCommon(cxt)
    def visitBaresym(self, cxt): return self.visitCommon(cxt)
    def visitSymbol(self, cxt): return self.visitCommon(cxt)
    def visitLitarr(self, cxt): return self.visitCommon(cxt)
    def visitLitarrcnt(self, cxt): return self.visitCommon(cxt)
    def visitBarelitarr(self, cxt): return self.visitCommon(cxt)
    def visitUnarytail(self, cxt): return self.visitCommon(cxt)
    def visitUnarymsg(self, cxt): return self.visitCommon(cxt)
    def visitUnaryop(self, cxt): return self.visitCommon(cxt)
    def visitKeywords(self, cxt): return self.visitCommon(cxt)
    def visitVar(self, cxt): return self.visitCommon(cxt)
    def visitBintail(self, cxt): return self.visitCommon(cxt)
    def visitBinmsg(self, cxt): return self.visitCommon(cxt)
    def visitBinop(self, cxt): return self.visitCommon(cxt)
    def visitTerminal(self, tnode): return self.visitCommon(tnode)
    def visitErrorNode(self, errnode): return self.visitCommon(errnode)

class Step(SObject):
    ruleCxt = Holder().name('ruleCxt')
    ruleName = Holder().name('ruleName')
    parent = Holder().name('parent')
    toKeep = Holder().name('toKeep').type('False_') # Interpreter hint to keep in instructions explicitly.
    isElement = Holder().name('isElement').type('False_') # Is a list element
    children = Holder().name('children').type('Map')
    intermediate = Holder().name('intermediate')
    final = Holder().name('final')

    def mainStep(self): return nil if self.children().isNil() else self.children().head()
    def keyname(self):
        return self.name() if self.hasKey('name') or self.ruleName().isNil() else self.ruleName()
    def addStep(self, name, step): self.children()[name] = step; return self
    def getStep(self, name, default=nil): return self.children().getValue(name, default)
    def isFinal(self): return self.final().notNil()
    def isEmpty(self): return true_ if self.children().isNil() else self.children().isEmpty()

    def retrieve(self, cxt):
        name = cxt.parser.ruleNames[cxt.getRuleIndex()]
        return self.ruleName(name).ruleCxt(cxt)

    def interpret(self, interpreter):
        cxt = self.ruleCxt()
        for childcxt in cxt.getChildren():
            # we want to keep SmallScript untouched without modifying accept(),
            # so we set currentStep to precompiler.
            interpreter.currentStep(self)
            childStep = childcxt.accept(interpreter)
            # if childStep.isNil() or self.toKeep(): continue
            if childStep.isNil(): continue
            if childStep.isElement(): continue  # childStep handled addStep already
            if not childStep.toKeep() and childStep.children().len() == 1:
                self.addStep(childStep.ruleName(), childStep.children().head())
            else:
                self.addStep(childStep.ruleName(), childStep)
        return self

    def describe(self):
        if self.hasKey('name'): return f"{self.name()}:{self.ruleName()}"
        if self.final().notNil(): return f"{self.final()}:{self.ruleName()}"
        if self.intermediate().notNil(): return f"{self.intermediate()}:{self.ruleName()}"
        return self.keyname()

class ClosureStep(Step):
    method = Holder().name('method').type('Method')

    def interpret(self, interpreter):
        closureInterpreter = Interpreter()
        closureInterpreter.currentStep(self)
        super().interpret(closureInterpreter)
        closureInterpreter.instructions().append(self)
        method = self.method()
        method.interpreter(closureInterpreter)
        bplStep = self.getStep('blkparamlst')
        if bplStep.notNil() and bplStep.notEmpty():
            method.params(bplStep.children().keys())
        tsStep = self.getStep('temps')
        if tsStep.notNil() and tsStep.notEmpty():
            method.tempvars(tsStep.children().keys())
        self.final(method)
        interpreter.instructions().append(self)
        return self

    def run(self, scope):
        exprs = self.getStep('exprs')
        if exprs.isNil(): return nil
        final = exprs.final()
        return final

class AssignStep(Step):
    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.final()
        final = self.getStep('expr').final()
        refObj.setValue(ref.name(), final)
        self.final(final)
        return final

class VarStep(Step):
    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.final()
        final = refObj.getValue(ref.name())
        self.final(final)
        return final

class RefStep(Step):
    def run(self, scope):
        varname = self.intermediate()
        self.name(varname)
        obj = scope.lookup(varname)
        if obj.isNil(): obj = scope
        self.final(obj)
        return obj

class Interpreter(SObject, StepVisitor):
    currentStep = Holder().name('currentStep')
    instructions = Holder().name('instructions').type('List')

    def _visitCommon(self, cxt, childStep):
        if not isinstance(cxt, RuleContext): return self
        currentStep = self.currentStep()        # save the current step
        childStep.retrieve(cxt)
        childStep.interpret(self)
        self.currentStep(currentStep)                  # restore the current step
        return childStep

    def visitCommon(self, cxt): return self._visitCommon(cxt, Step())
    def visitClosure(self, cxt): return self._visitCommon(cxt, ClosureStep().toKeep(true_))

    def visitTemps(self, cxt): return self._visitCommon(cxt, Step().toKeep(true_))
    def visitTempvar(self, cxt):
        currentStep = self.currentStep()
        step = Step().retrieve(cxt).isElement(true_)
        ret = self._retrieveTerminalText(cxt)
        step.name(ret).final(ret)
        currentStep.addStep(step.keyname(), step)
        return step

    def visitBlkparamlst(self, cxt): return self._visitCommon(cxt, Step().toKeep(true_))
    def visitBlkparam(self, cxt):
        currentStep = self.currentStep()
        step = Step().retrieve(cxt).isElement(true_)
        text = self._retrieveTerminalText(cxt)
        ret = text[1:]
        step.name(ret).final(ret)
        currentStep.addStep(step.keyname(), step)
        return step

    def visitAssign(self, cxt):
        step = self._visitCommon(cxt, AssignStep().toKeep(true_))
        self.instructions().append(step)
        return step

    def visitVar(self, cxt):
        step = self._visitCommon(cxt, VarStep().toKeep(true_))
        self.instructions().append(step)
        return step

    def visitRef(self, cxt):
        step = self._addTextStep(cxt, RefStep().toKeep(true_), false_)
        self.instructions().append(step)
        return step

    def visitString(self, cxt):
        step =  self._addTextStep(cxt, Step(), false_)
        ret = String(step.intermediate()[1:-1])     # "'abc'" -> "abc"
        step.final(ret)
        return step

    def visitNum(self, cxt):
        step = self._addTextStep(cxt, Step(), false_)
        ret = step.intermediate().asNumber()
        step.final(ret)
        return step

    def _addTextStep(self, cxt, step, final=true_):
        currentStep = self.currentStep()
        step.retrieve(cxt)
        text = self._retrieveTerminalText(cxt)
        if final:
            step.final(text)
        else:
            step.intermediate(text)
        currentStep.addStep(step.ruleName(), step)
        return step

    def _retrieveTerminalText(self, cxt):
        terminal = cxt.children[0]
        text = terminal.symbol.text
        return text

    # def visitBlk(self, cxt):          # common
    # def visitExpr(self, cxt):         # Collapsible
    # def visitAssign(self, cxt):       # Collapsible
    # def visitCascade(self, cxt):      # common
    # def visitMsg(self, cxt):          # common
    # def visitBinhead(self, cxt):      # Collapsible
    # def visitBinmsg(self, cxt):       # Collapsible
    # def visitBinop(self, cxt):        # common
    # def visitKwhead(self, cxt):       # Collapsible
    # def visitKwmsg(self, cxt):        # common
    # def visitKwpair(self, cxt):       # common
    # def visitPtkey(self, cxt):        # common
    # def visitUnaryhead(self, cxt):    # Collapsible
    # def visitUnaryop(self, cxt):      # common
    # def visitLitarr(self, cxt):       # Collapsible
    def visitPtfin(self, cxt): return self._addTextStep(cxt, Step())
    # def visitPrimitive(self, cxt):    # common
    def visitPrimkey(self, cxt): return self._addTextStep(cxt, Step())
    def visitPrimtxt(self, cxt): return self._addTextStep(cxt, Step())
    # def visitParselit(self, cxt): self._addTextStep(cxt, Step())
    def visitSymbol(self, cxt): return self._addTextStep(cxt, Step())
    def visitBaresym(self, cxt): return self._addTextStep(cxt, Step())
    def visitWs(self, cxt): return nil
    def visitTerminal(self, tnode): return nil


