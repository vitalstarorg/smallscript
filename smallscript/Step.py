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
    def visitUnaryhead(self, cxt): return self.visitCommon(cxt)
    def visitUnarytail(self, cxt): return self.visitCommon(cxt)
    def visitUnarymsg(self, cxt): return self.visitCommon(cxt)
    def visitUnaryop(self, cxt): return self.visitCommon(cxt)

    def visitCascade(self, cxt): return self.visitCommon(cxt)
    def visitPtfin(self, cxt): return self.visitCommon(cxt)
    def visitMsg(self, cxt): return self.visitCommon(cxt)
    def visitAssign(self, cxt): return self.visitCommon(cxt)
    def visitRef(self, cxt): return self.visitCommon(cxt)
    def visitBinhead(self, cxt): return self.visitCommon(cxt)
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
    isElement = Holder().name('isElement').type('False_') # Is an element of a list
    isList = Holder().name('isList').type('False_')       # Is a list
    children = Holder().name('children').type('Map')
    intermediate = Holder().name('intermediate')
    final = Holder().name('final')

    def mainStep(self): return nil if self.children().isNil() else self.children().head()
    def keyname(self):
        return self.name() if self.hasKey('name') or self.ruleName().isNil() else self.ruleName()
    def getStep(self, name, default=nil): return self.children().getValue(name, default)
    def isFinal(self): return self.final().notNil()
    def isEmpty(self): return true_ if self.children().isNil() else self.children().isEmpty()

    def addStep(self, name, step):
        children = self.children()
        if children.hasKey(name):
            child = children.getValue(name)
            if not isinstance(child, List):
                child = List().append(child)
                children.setValue(name, child)
            child.append(step)
        else:
            children[name] = step
        return self

    def _ruleName(self, cxt):
        if isinstance(cxt, RuleContext):
            return cxt.parser.ruleNames[cxt.getRuleIndex()]
        return cxt.symbol.text

    def retrieve(self, cxt, final=false_):
        name = self._ruleName(cxt)
        self.ruleName(name).ruleCxt(cxt)
        if not isinstance(cxt.children[0], RuleContext):
            terminal = cxt.children[0]
            text = terminal.symbol.text
            if final:
                self.final(text)
            else:
                self.intermediate(text)
        return self

    def interpret(self, interpreter):
        rulename = self.ruleName()      # debugging purpose
        if rulename == 'unarymsg':
            x = 1
        currentStep = interpreter.currentStep()
        interpreter.currentStep(self)
        cxt = self.ruleCxt()
        for childcxt in cxt.getChildren():
            chdRulename = self._ruleName(childcxt)  # debugging purpose
            childStep = childcxt.accept(interpreter)
            if childStep.isNil(): continue
            if childStep.isElement(): continue  # e.g. blkparam, tempvar
            if childStep.toKeep() or childStep.children().len() != 1:
                self.addStep(childStep.ruleName(), childStep)
            else:
                self.addStep(childStep.ruleName(), childStep.children().head())
        interpreter.currentStep(currentStep)
        return self

    def describe(self):
        if self.hasKey('name'): return f"{self.name()}:{self.ruleName()}"
        if self.final().notNil(): return f"{self.final()}:{self.ruleName()}"
        if self.intermediate().notNil(): return f"{self.intermediate()}:{self.ruleName()}"
        return self.keyname()

class RuntimeStep(Step):
    "Helper class for all steps that have runtime implications."
    def __init__(self):
        self.toKeep(true_)

    def interpret(self, interpreter):
        super().interpret(interpreter)
        interpreter.instructions().append(self)
        return self

class ClosureStep(RuntimeStep):
    method = Holder().name('method').type('Method')

    def interpret(self, interpreter):
        closureInterpreter = Interpreter().currentStep(self)
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

class AssignStep(RuntimeStep):
    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.final()
        final = self.getStep('expr').final()
        refObj.setValue(ref.name(), final)
        self.final(final)
        return final

class VarStep(RuntimeStep):
    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.final()
        final = refObj.getValue(ref.name())
        self.final(final)
        return final

class RefStep(RuntimeStep):
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

    def visitCommon(self, cxt): return Step().retrieve(cxt).interpret(self)
    def visitClosure(self, cxt): return ClosureStep().retrieve(cxt).interpret(self)
    def visitExprs(self, cxt):
        # currentStep = self.currentStep()        # save the current step
        exprsStep = Step().retrieve(cxt)
        exprsStep.interpret(self)               # process list of expressions

        # keep the last expression for closure
        children = exprsStep.children()
        if children.hasKey('exprlst'):
            exprlst = children['exprlst']
            children.clear()
            last = exprlst[-1]
            children['exprlst'] = last
        # self.currentStep(currentStep)          # restore the current step
        return exprsStep

    def visitUnaryhead(self, cxt): return self.visitCommon(cxt)
    def visitUnaryop(self, cxt): return Step().retrieve(cxt)

    def visitTemps(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitTempvar(self, cxt):
        currentStep = self.currentStep()
        step = Step().retrieve(cxt).isElement(true_)
        text = step.intermediate()
        step.name(text).final(text)
        currentStep.addStep(step.keyname(), step)
        return step

    def visitBlkparamlst(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitBlkparam(self, cxt):
        currentStep = self.currentStep()
        step = Step().retrieve(cxt).isElement(true_)
        text = step.intermediate()
        ret = text[1:]
        step.name(ret).final(ret)
        currentStep.addStep(step.keyname(), step)
        return step

    def visitAssign(self, cxt): return AssignStep().retrieve(cxt).interpret(self)
    def visitVar(self, cxt): return VarStep().retrieve(cxt).interpret(self)
    def visitRef(self, cxt): return RefStep().retrieve(cxt).interpret(self)

    def visitString(self, cxt):
        step = Step().retrieve(cxt)
        ret = String(step.intermediate()[1:-1])     # "'abc'" -> "abc"
        step.final(ret)
        return step

    def visitNum(self, cxt):
        step = Step().retrieve(cxt)
        ret = step.intermediate().asNumber()
        step.final(ret)
        return step

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
    def visitPtfin(self, cxt): return Step().retrieve(cxt, true_)
    # def visitPrimitive(self, cxt):    # common
    def visitPrimkey(self, cxt): return Step().retrieve(cxt, true_)
    def visitPrimtxt(self, cxt): return Step().retrieve(cxt, true_)
    # def visitParselit(self, cxt): self._addTextStep(cxt, Step())
    def visitSymbol(self, cxt): return Step().retrieve(cxt, true_)
    def visitBaresym(self, cxt): return Step().retrieve(cxt, true_)
    def visitWs(self, cxt): return nil
    def visitTerminal(self, tnode): return nil


