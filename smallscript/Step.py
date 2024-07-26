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
    def visitSequence(self, cxt): return self.visitCommon(cxt)
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
    children = Holder().name('children').type('Map')
    intermediate = Holder().name('intermediate')
    final = Holder().name('final')

    def mainStep(self): return nil if self.children().isNil() else self.children().head()
    def keyname(self):
        return self.name() if self.hasKey('name') or self.ruleName().isNil() else self.ruleName()

    def addStep(self, step): self.children()[step.keyname()] = step; return self
    def getStep(self, name, default=nil): return self.children().getValue(name, default)
    def isFinal(self): return self.final().notNil()

    def precompile(self):
        precompilation = PrecompilationStep()
        cxt = self.ruleCxt()
        precompilation._scanChildren(self, cxt)
        return precompilation

    def desc(self):
        if self.final().notNil(): return self.final()
        if self.intermediate().notNil(): return self.intermediate()
        return self.keyname()

class AssignStep(Step):
    def run(self):
        refname = self.getStep('ref')
        expr = self.getStep('expr')
        final = expr.final()
        self.final(final)
        return self
class RefStep(Step):
    def run(self):
        varname = self.intermediate()
        self.final(varname)
        return self

    def desc(self): return f"{self.intermediate()}"

class PrecompilationStep(SObject, StepVisitor):
    currentStep = Holder().name('currentStep')
    instructions = Holder().name('instructions').type('List')

    def visitWs(self, cxt): return
    def visitTerminal(self, tnode):
        # currentStep = self.currentStep()
        # text = tnode.symbol.text
        # currentStep.name(text)
        return self

    def _scanChildren(self, step, cxt):
        self.currentStep(step)
        for child in cxt.getChildren():
            child.accept(self)

    def _getRuleName(self, cxt):
        name = cxt.parser.ruleNames[cxt.getRuleIndex()]
        return name

    def _visitCommon(self, cxt, step):
        currentStep = self.currentStep()
        if not isinstance(cxt, RuleContext):
            return self
        ruleName = self._getRuleName(cxt)
        if ruleName == 'blkparam':
            x = 1
        step.ruleName(ruleName)
        self._scanChildren(step, cxt)
        self.currentStep(currentStep)
        if step.children().len() == 1:
            step = step.children().head()
        currentStep.addStep(step)
        return step

    def visitCommon(self, cxt):
        step = Step()
        self._visitCommon(cxt, step)
        # if not step.isFinal():
        #     self.instructions().append(step)

    def visitBlkparam(self, cxt):
        currentStep = self.currentStep()
        step = Step()
        text = self._retrieveText(cxt, step)
        ret = text[1:]
        step.name(ret).final(ret)
        currentStep.addStep(step)
        return self

    def visitAssign(self, cxt):
        step = self._visitCommon(cxt, AssignStep())
        self.instructions().append(step)
        return self

    def visitRef(self, cxt):
        step = self._addTextStep(cxt, RefStep(), false_);
        self.instructions().append(step)
        return self

    def visitNum(self, cxt):
        step = self._addTextStep(cxt, Step(), false_)
        ret = step.intermediate().asNumber()
        step.final(ret)
        return self

    def _addTextStep(self, cxt, step, final=true_):
        currentStep = self.currentStep()
        text = self._retrieveText(cxt, step)
        if final:
            step.final(text)
        else:
            step.intermediate(text)
        currentStep.addStep(step)
        return step

    def _retrieveText(self, cxt, step):
        terminal = cxt.children[0]
        text = terminal.symbol.text
        step.ruleName(self._getRuleName(cxt))
        return text

    # def visitBlk(self, cxt):          # common
    # def visitTempvar(self, cxt):      # common
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
    # def visitVar(self, cxt):          # additional processing
    # def visitLitarr(self, cxt):       # Collapsible
    def visitPtfin(self, cxt): self._addTextStep(cxt, Step()); return self
    def visitString(self, cxt): self._addTextStep(cxt, Step()); return self
    # def visitPrimitive(self, cxt):    # common
    def visitPrimkey(self, cxt): self._addTextStep(cxt, Step()); return self
    def visitPrimtxt(self, cxt): self._addTextStep(cxt, Step()); return self
    # def visitParselit(self, cxt): self._addTextStep(cxt, Step()); return self
    def visitSymbol(self, cxt): self._addTextStep(cxt, Step()); return self
    def visitBaresym(self, cxt): self._addTextStep(cxt, Step()); return self

    # def visitSequence(self, cxt):
    #     ruleName = self._getRuleName(cxt)
    #     sequence = Step().name(ruleName)
    #     currentStep = self.currentStep()
    #     self.scanChildren(sequence, cxt)
    #     exprs = sequence.getStep('exprs')
    #     temps = sequence.getStep('temps')
    #     if exprs.len() == 1:
    #         currentStep.addStep('exprs', exprs.head())
    #     else:
    #         currentStep.addStep('exprs', exprs)
    #     if temps.notNil():
    #         currentStep.addStep('temps', temps)
    #     return self
