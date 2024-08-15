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
    def visitTemps(self, cxt): return self.visitCommon(cxt)
    def visitTempvar(self, cxt): return self.visitCommon(cxt)
    def visitBlkparamlst(self, cxt): return self.visitCommon(cxt)
    def visitBlkparam(self, cxt): return self.visitCommon(cxt)
    def visitExpr(self, cxt): return self.visitCommon(cxt)
    def visitExprs(self, cxt): return self.visitCommon(cxt)
    def visitUnaryhead(self, cxt): return self.visitCommon(cxt)
    def visitUnarytail(self, cxt): return self.visitCommon(cxt)
    def visitUnarymsg(self, cxt): return self.visitCommon(cxt)
    def visitUnaryop(self, cxt): return self.visitCommon(cxt)
    def visitOperand(self, cxt): return self.visitCommon(cxt)
    def visitKwhead(self, cxt): return self.visitCommon(cxt)
    def visitKwmsg(self, cxt): return self.visitCommon(cxt)
    def visitKwpair(self, cxt): return self.visitCommon(cxt)
    def visitBinhead(self, cxt): return self.visitCommon(cxt)
    def visitBintail(self, cxt): return self.visitCommon(cxt)
    def visitBinmsg(self, cxt): return self.visitCommon(cxt)
    def visitBinop(self, cxt): return self.visitCommon(cxt)
    def visitCascade(self, cxt): return self.visitCommon(cxt)
    def visitPtfin(self, cxt): return self.visitCommon(cxt)

    def visitAssign(self, cxt): return self.visitCommon(cxt)
    def visitVar(self, cxt): return self.visitCommon(cxt)
    def visitRef(self, cxt): return self.visitCommon(cxt)
    def visitNum(self, cxt): return self.visitCommon(cxt)
    def visitString(self, cxt): return self.visitCommon(cxt)
    def visitWs(self, cxt): return self.visitCommon(cxt)
    def visitExprlst(self, cxt): return self.visitCommon(cxt)

    def visitMsg(self, cxt): return self.visitCommon(cxt)
    def visitPtkey(self, cxt): return self.visitCommon(cxt)
    def visitSubexpr(self, cxt): return self.visitCommon(cxt)
    def visitLiteral(self, cxt): return self.visitCommon(cxt)
    def visitRtlit(self, cxt): return self.visitCommon(cxt)
    def visitBlk(self, cxt): return self.visitCommon(cxt)
    def visitDyndict(self, cxt): return self.visitCommon(cxt)
    def visitDynarr(self, cxt): return self.visitCommon(cxt)
    def visitParselit(self, cxt): return self.visitCommon(cxt)
    def visitChar(self, cxt): return self.visitCommon(cxt)
    def visitPrimitive(self, cxt): return self.visitCommon(cxt)
    def visitPrimkey(self, cxt): return self.visitCommon(cxt)
    def visitPrimtxt(self, cxt): return self.visitCommon(cxt)
    def visitBaresym(self, cxt): return self.visitCommon(cxt)
    def visitSymbol(self, cxt): return self.visitCommon(cxt)
    def visitLitarr(self, cxt): return self.visitCommon(cxt)
    def visitLitarrcnt(self, cxt): return self.visitCommon(cxt)
    def visitBarelitarr(self, cxt): return self.visitCommon(cxt)
    def visitKeywords(self, cxt): return self.visitCommon(cxt)
    def visitTerminal(self, tnode): return self.visitCommon(tnode)
    def visitErrorNode(self, errnode): return self.visitCommon(errnode)

class Step(SObject):
    ruleCxt = Holder().name('ruleCxt')
    ruleName = Holder().name('ruleName')
    parent = Holder().name('parent')
    toKeep = Holder().name('toKeep').type('False_') # Interpreter hint to keep in instructions explicitly.
    isElement = Holder().name('isElement').type('False_') # Is an element of a list
    # isList = Holder().name('isList').type('False_')       # Is a list
    children = Holder().name('children').type('Map')
    compileRes = Holder().name('compileRes')
    runtimeRes = Holder().name('runtimeRes')

    def mainStep(self): return nil if self.children().isNil() else self.children().head()
    def keyname(self):
        return self.name() if self.hasKey('name') or self.ruleName().isNil() else self.ruleName()
    def getStep(self, name, default=nil): return self.children().getValue(name, default)
    def isFinal(self): return self.runtimeRes().notNil()
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

    def retrieve(self, cxt):
        name = self._ruleName(cxt)
        self.ruleName(name).ruleCxt(cxt)
        if not isinstance(cxt.children[0], RuleContext):
            terminal = cxt.children[0]
            text = terminal.symbol.text
            self.compileRes(text)
        return self

    def _addToParent(self, interpreter, parentStep, toKeep):
        if toKeep:
            parentStep.addStep(self.ruleName(), self)
            interpreter.instructions().append(self)
        else:
            if self.children().len() == 1:
                parentStep.addStep(self.ruleName(), self.children().head())
            else:
                parentStep.addStep(self.ruleName(), self)
        return self

    def interpret(self, interpreter):
        rulename = self.ruleName()      # debugging purpose
        if rulename == 'unarytail':
            x = 1
        currentStep = interpreter.currentStep()
        interpreter.currentStep(self)
        cxt = self.ruleCxt()
        for childcxt in cxt.getChildren():
            chdRulename = self._ruleName(childcxt)  # debugging purpose
            childStep = childcxt.accept(interpreter)
            if childStep.isNil() or childStep.isElement(): continue  # e.g. blkparam, tempvar
            childStep._addToParent(interpreter, self, childStep.toKeep())
        interpreter.currentStep(currentStep)
        return self

    def run(self, scope):
        "Subclass responsibility"
        return nil

    def describe(self):
        if self.hasKey('name'): return f"{self.name()}:{self.ruleName()}"
        if self.runtimeRes().notNil(): return f"{self.runtimeRes()}:{self.ruleName()}"
        if self.compileRes().notNil(): return f"{self.compileRes()}:{self.ruleName()}"
        return self.keyname()

class RuntimeStep(Step):
    "Helper class for all steps that have runtime implications."
    def __init__(self): self.toKeep(true_)

    def interpret(self, interpreter):
        super().interpret(interpreter)
        # interpreter.instructions().append(self)
        return self

class SmallScriptStep(RuntimeStep):
    def getClosure(self, interpreter):
        interpreter.currentStep(self)
        ssCxt = self.ruleCxt()
        closureCxt = next(ssCxt.getChildren())
        closureStep = closureCxt.accept(interpreter)
        return closureStep

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
        self.runtimeRes(method)
        interpreter.instructions().append(self)
        return self

    def run(self, scope):
        # exprs = self.getStep('exprs')
        # if exprs.isNil(): return nil
        # res = exprs.runtimeRes()
        # return res
        exprs = self.getStep('exprs')
        if exprs.isNil(): return nil
        if exprs.ruleName() == 'exprs':
            if exprs.isNil(): return nil
            exprlst = exprs.getStep('exprlst')
            if exprlst.notNil():
                res = exprlst.runtimeRes()
            else:
                expr = self.getStep('expr')
                res = expr.runtimeRes()
        else:
            res = exprs.runtimeRes()
        return res

class UnaryHeadStep(RuntimeStep):
    def _addToParent(self, interpreter, parentStep, toKeep):
        if self.children().len() == 1:
            parentStep.addStep(self.ruleName(), self.children().head())
        else:
            parentStep.addStep(self.ruleName(), self)
            interpreter.instructions().append(self)
        return self

    def _unaryops(self, tail, oplist):
        if tail.children().isEmpty():
            oplist.append(tail.compileRes())    # this tail is unaryops
            return
        unarymsg = tail.getStep('unarymsg')
        oplist.append(unarymsg.compileRes())
        unarytail = tail.getStep('unarytail')
        self._unaryops(unarytail, oplist)
        return self

    def invoke(self, scope, obj, oplist):   # obj can be Python obj
        res = obj
        for op in oplist:
            method = getattr(res, op, nil)  # Holder.valueFunc
            if method == nil and isinstance(res, SObject):
                holder = res.metaclass().holderByName(op)
                # if holder.notNil() and holder.method().notNil():
                if holder.notNil():
                    method = holder.__get__(obj)
            # if method == nil: method = getattr(res, op, nil)  # Holder.valueFunc
            if method == nil: return nil
            res = method()
        return res

    def run(self, scope):
        operand = self.getStep('operand')
        obj = operand.runtimeRes()
        unarytail = self.getStep('unarytail')
        unaryopList = List()
        self._unaryops(unarytail, unaryopList)
        res = self.invoke(scope, obj, unaryopList)
        self.runtimeRes(res)
        return res

class BinHeadStep(RuntimeStep):
    operators = Holder().name('operators').type('Map').asClassType()

    @Holder().asClassType()
    def metaInit(scope):
        self = scope['self']
        operators = self.operators()
        operators. \
            setValue('\\', '__floordiv__').setValue('+', '__add__').setValue('*', '__mul__'). \
            setValue('/', '__truediv__').setValue('=', '__eq__').setValue('>', '__gt__'). \
            setValue('<', '__lt__').setValue(',', '__comma__').setValue('@', '__at__'). \
            setValue('%', '__mod__').setValue('~', '__invert__').setValue('|', '__or__'). \
            setValue('&', '__and__').setValue('-', '__sub__').setValue('?', '__question__'). \
            setValue('>=', '__ge__').setValue('<=', '__le__').setValue('^', '__xor__')

    def _addToParent(self, interpreter, parentStep, toKeep):
        if self.children().len() == 1:
            parentStep.addStep(self.ruleName(), self.children().head())
        else:
            parentStep.addStep(self.ruleName(), self)
            interpreter.instructions().append(self)
        return self

    def _binaryops(self, tail, binopList):
        if tail.ruleName() == 'binmsg':
            binmsg = tail
        else:
            binmsg = tail.getStep('binmsg')
        binop = binmsg.getStep('binop').compileRes()
        unaryhead = binmsg.getStep('unaryhead').runtimeRes()
        binopList.append((binop, unaryhead))
        bintail = tail.getStep('bintail')
        if bintail.notNil():
            self._binaryops(bintail, binopList)
        return self

    def invoke(self, scope, obj, binopList):   # obj can be Python obj
        operators = self.operators()
        res = obj
        for binop, unaryhead in binopList:
            method = getattr(res, binop, nil)
            if method == nil:
                if binop in operators:
                    binop = operators[binop]
                method = getattr(res, binop, nil)
                if method == nil: return nil
            res = method(unaryhead)
        return res

    def run(self, scope):
        unaryhead = self.getStep('unaryhead')
        obj = unaryhead.runtimeRes()
        bintail = self.getStep('bintail')
        binopList = List()
        self._binaryops(bintail, binopList)
        res = self.invoke(scope, obj, binopList)
        self.runtimeRes(res)
        return res

class KwHeadStep(RuntimeStep):
    def _addToParent(self, interpreter, parentStep, toKeep):
        if self.children().len() == 1:
            parentStep.addStep(self.ruleName(), self.children().head())
        else:
            parentStep.addStep(self.ruleName(), self)
            interpreter.instructions().append(self)
        return self

    def _kwmsg(self, kwmsg):
        if not isinstance(kwmsg, List):
            kwmsg = List().append(kwmsg)
        kwMap = Map()
        for kwpair in kwmsg:
            ptkey = kwpair.children()['ptkey'].compileRes()[:-1]
            binhead = kwpair.children()['binhead'].runtimeRes()
            kwMap[ptkey] = binhead
        return kwMap

    def _methodLookup(self, obj, prefix, fullname, nArgs):
        "Lookup method in python obj including SObject. Return a matched bound method with fullname and nArgs, or using prefix only."
        # obj firstname: 'first' lastname: 'last'
        # match #1: firstname__lastname__(firstname, lastname)      - SObject protocol
        # match #2: firstname(firstname, lastname)                  - Python protocol
        methods = Map()
        for name in dir(obj):
            if not name.startswith(prefix): continue
            item = getattr(obj, name)
            if inspect.ismethod(item) and item.__self__ is obj:
                signature = inspect.signature(item)
                nParam = nDefault = 0
                for argname, param in signature.parameters.items():
                    nParam += 1
                    if param.default is not inspect.Parameter.empty:
                        nDefault += 1
                if nArgs > nParam or nArgs < nParam - nDefault: continue
                params = List(signature.parameters.values())
                methods[name] = (nParam, nDefault, item)
        if fullname in methods: return methods[fullname][2]
        if prefix in methods: return methods[prefix][2]
        return nil

    def invoke(self, scope, obj, kwMap):   # obj can be Python obj
        prefix = kwMap.keys().head()
        fullname = prefix
        if kwMap.len() > 1:
            fullname = "".join([f"{key}__" for key in kwMap.keys()])

        # Invoke method through Python protocol
        res = nil
        nArgs = kwMap.len()
        method = self._methodLookup(obj, prefix, fullname, nArgs)

        # Invoke method through SObject protocol
        if method == nil and isinstance(obj, SObject):
            holder = obj.metaclass().holderByName(fullname)
            if holder.notNil():
                method = holder.__get__(obj)
            else:
                holder = obj.metaclass().holderByName(prefix)
                # if holder.notNil() and holder.method().notNil():
                if holder.notNil():
                        method = holder.__get__(obj)

        if method != nil:
            res = method(*kwMap.values())
        return res

    def run(self, scope):
        unaryhead = self.getStep('unaryhead')
        obj = unaryhead.runtimeRes()
        kwmsg = self.getStep('kwmsg')
        kwMap = self._kwmsg(kwmsg)
        res = self.invoke(scope, obj, kwMap)
        self.runtimeRes(res)
        return res

class CascadeStep(RuntimeStep):
    def run(self, scope):
        head = self.getStep('kwhead')
        if head.isNil():
           head = self.getStep('binhead')
        obj = head.runtimeRes()
        msgs = self.getStep('msg')
        if not isinstance(msgs, List):
            msgs = List().append(msgs)
        return nil

class AssignStep(RuntimeStep):
    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.runtimeRes()
        res = self.getStep('expr').runtimeRes()
        refObj.setValue(ref.name(), res)
        self.runtimeRes(res)
        return res

class VarStep(RuntimeStep):
    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.runtimeRes()
        res = refObj.getValue(ref.name())
        self.runtimeRes(res)
        return res

class RefStep(RuntimeStep):
    def run(self, scope):
        varname = self.compileRes()
        self.name(varname)
        obj = scope.lookup(varname)
        if obj.isNil(): obj = scope
        self.runtimeRes(obj)
        return obj

class Interpreter(SObject, StepVisitor):
    currentStep = Holder().name('currentStep')
    instructions = Holder().name('instructions').type('List')

    def visitWs(self, cxt): return nil
    def visitTerminal(self, tnode): return nil
    def visitPtfin(self, cxt): return nil
    def visitCommon(self, cxt): return Step().retrieve(cxt).interpret(self)
    def visitClosure(self, cxt): return ClosureStep().retrieve(cxt).interpret(self)

    def visitTemps(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitTempvar(self, cxt):
        currentStep = self.currentStep()
        step = Step().retrieve(cxt).isElement(true_)
        text = step.compileRes()
        step.name(text).runtimeRes(text)
        currentStep.addStep(step.keyname(), step)
        return step

    def visitBlkparamlst(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitBlkparam(self, cxt):
        currentStep = self.currentStep()
        step = Step().retrieve(cxt).isElement(true_)
        text = step.compileRes()
        res = text[1:]
        step.name(res).runtimeRes(res)
        currentStep.addStep(step.keyname(), step)
        return step

    def visitExprs(self, cxt):
        # currentStep = self.currentStep()        # save the current step
        exprsStep = Step().retrieve(cxt)
        exprsStep.interpret(self)               # process list of expressions

        # keep the last expression for closure
        children = exprsStep.children()
        if children.hasKey('exprlst'):
            exprlst = children['exprlst']
            if isinstance(exprlst,List):    # exprs can be a single step.
                last = exprlst[-1]
                children.clear()
                children['exprlst'] = last
        # self.currentStep(currentStep)          # restore the current step
        return exprsStep

    def visitUnaryhead(self, cxt): return UnaryHeadStep().retrieve(cxt).interpret(self)
    def visitKwhead(self, cxt): return KwHeadStep().retrieve(cxt).interpret(self)
    # def visitKwmsg(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitBinhead(self, cxt): return BinHeadStep().retrieve(cxt).interpret(self)
    def visitCascade(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)

    def visitAssign(self, cxt): return AssignStep().retrieve(cxt).interpret(self)
    def visitVar(self, cxt): return VarStep().retrieve(cxt).interpret(self)
    def visitRef(self, cxt): return RefStep().retrieve(cxt).interpret(self)

    def visitString(self, cxt):
        step = Step().retrieve(cxt)
        res = String(step.compileRes()[1:-1])     # "'abc'" -> "abc"
        step.runtimeRes(res)
        return step

    def visitNum(self, cxt):
        step = Step().retrieve(cxt)
        res = step.compileRes().asNumber()
        step.runtimeRes(res)
        return step
