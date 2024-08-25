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

class RuleContextVisitor(SmallScriptVisitor):
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
    def visitChain(self, cxt): return self.visitCommon(cxt)
    def visitPtfin(self, cxt): return self.visitCommon(cxt)
    def visitMsg(self, cxt): return self.visitCommon(cxt)
    def visitSubexpr(self, cxt): return self.visitCommon(cxt)
    def visitChar(self, cxt): return self.visitCommon(cxt)
    def visitBaresym(self, cxt): return self.visitCommon(cxt)
    def visitPrimitive(self, cxt): return self.visitCommon(cxt)
    def visitAssign(self, cxt): return self.visitCommon(cxt)
    def visitVar(self, cxt): return self.visitCommon(cxt)
    def visitRef(self, cxt): return self.visitCommon(cxt)
    def visitString(self, cxt): return self.visitCommon(cxt)
    def visitWs(self, cxt): return self.visitCommon(cxt)
    def visitTerminal(self, tnode): return self.visitCommon(tnode)
    def visitNum(self, cxt): return self.visitCommon(cxt)
    def visitSsFloat(self, cxt): return self.visitCommon(cxt)
    def visitSsHex(self, cxt): return self.visitCommon(cxt)
    def visitSsInt(self, cxt):return self.visitCommon(cxt)
    def visitExprlst(self, cxt): return self.visitCommon(cxt)
    def visitBlk(self, cxt): return self.visitCommon(cxt)
    def visitPtkey(self, cxt): return self.visitCommon(cxt)
    def visitLiteral(self, cxt): return self.visitCommon(cxt)
    def visitRtlit(self, cxt): return self.visitCommon(cxt)
    def visitDyndict(self, cxt): return self.visitCommon(cxt)
    def visitDynarr(self, cxt): return self.visitCommon(cxt)
    def visitParselit(self, cxt): return self.visitCommon(cxt)
    def visitPrimkey(self, cxt): return self.visitCommon(cxt)
    def visitPrimtxt(self, cxt): return self.visitCommon(cxt)
    def visitSymbol(self, cxt): return self.visitCommon(cxt)
    def visitLitarr(self, cxt): return self.visitCommon(cxt)
    def visitLitarrcnt(self, cxt): return self.visitCommon(cxt)
    def visitBarelitarr(self, cxt): return self.visitCommon(cxt)
    def visitKeywords(self, cxt): return self.visitCommon(cxt)
    def visitErrorNode(self, errnode): return self.visitCommon(errnode)

class StepVisitor(SObject):
    def __getattr__(self, item):
        def defaultVisit(step):
            return step.visit(self)
        return defaultVisit

class Step(SObject):
    ruleCxt = Holder().name('ruleCxt')
    ruleName = Holder().name('ruleName')
    parent = Holder().name('parent')
    toKeep = Holder().name('toKeep').type('False_') # Interpreter hint to keep in instructions explicitly.
    isElement = Holder().name('isElement').type('False_') # Is an element of a list
    children = Holder().name('children').type('Map')
    compileRes = Holder().name('compileRes')
    runtimeRes = Holder().name('runtimeRes')

    def visit(self, visitor): return visitor.visitStep(self)
    def keyname(self):
        return self.name() if self.hasKey('name') or self.ruleName().isNil() else self.ruleName()
    def getStep(self, name, default=nil): return self.children().getValue(name, default)
    def isFinal(self): return self.runtimeRes().notNil()
    def isEmpty(self): return true_ if self.children().isNil() else self.children().isEmpty()
    def isRuntime(self): return false_

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
        if cxt.children is None: return self
        if not isinstance(cxt.children[0], RuleContext):
            # first terminal children to determine the whole context is not reliable e.g. baresym & litarry. cxt.getText() would slow down 2.5%. Can regain the perf by reimplement these rule contexts.
            # terminal = cxt.children[0]
            # text = terminal.symbol.text
            text = cxt.getText()
            self.compileRes(text)
            self.runtimeRes(text)
        return self

    def _addToParent(self, interpreter, parentStep, toKeep):
        if toKeep:
            parentStep.addStep(self.ruleName(), self)
        else:
            if self.children().len() == 1:
                parentStep.addStep(self.ruleName(), self.children().head())
            else:
                parentStep.addStep(self.ruleName(), self)
        if self.isRuntime():
            if interpreter.toDebug(): print(f"  {self.ruleName()} add to instructions")
            interpreter.instructions().append(self)
        return self

    def interpret(self, interpreter):
        if interpreter.toDebug():
            rulename = self.ruleName(); print(f"parent: {rulename}")
        currentStep = interpreter.currentStep()
        interpreter.currentStep(self)
        cxt = self.ruleCxt()
        for childcxt in cxt.getChildren():
            if interpreter.toDebug():
                chdRulename = self._ruleName(childcxt); print(f"  children: {chdRulename}")
            childStep = childcxt.accept(interpreter)
            if childStep.isNil() or childStep.isElement(): continue  # e.g. blkparam, tempvar
            if interpreter.toDebug(): print(f"    {chdRulename}._addToParent({rulename})")
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

class SmallScriptStep(Step):
    def visit(self, step): return step.visitSmallscript(self)

    def getClosure(self, interpreter):
        interpreter.currentStep(self)
        ssCxt = self.ruleCxt()
        closureCxt = next(ssCxt.getChildren())
        closureStep = closureCxt.accept(interpreter)
        interpreter.currentStep(closureStep)
        return closureStep

class ClosureStep(Step):
    method = Holder().name('method')

    def visit(self, step): return step.visitClosure(self)

    def interpret(self, interpreter):
        # Interpret the rest with a new interpreter.
        closureInterpreter = Interpreter().currentStep(self).method(interpreter.method())
        if interpreter.toDebug(): closureInterpreter.toDebug(true_)
        super().interpret(closureInterpreter)

        # Create method object for this closure.
        method = interpreter.method().createEmpty()
            # new method obj from initiating method e.g. DebugMethod.
        method.toDebug(interpreter.method().toDebug())
        method.loglevel(interpreter.method().loglevel())
        self.method(method)
        method.interpreter(closureInterpreter)
        bplStep = self.getStep('blkparamlst')
        if bplStep.notNil() and bplStep.notEmpty():
            method.params(bplStep.children().keys())
        tsStep = self.getStep('temps')
        if tsStep.notNil() and tsStep.notEmpty():
            method.tempvars(tsStep.children().keys())
        self.runtimeRes(method)

        if interpreter.toDebug():
            print("Instruction List:")
            for instruction in method.interpreter().instructions():
                print(f"  {instruction}")
        return self

    def flatten(self):
        exprs = self.getStep('exprs')   # step, List
        expr = exprs.getStep('expr')
        exprlst = exprs.getStep('exprlst')
        flattenList = List()
        if expr.isNil():
            flattenList.append(exprs)          # closure is a literal step as exprs has no expr.
        else:
            flattenList.append(expr)
            if exprlst.notNil():
                flattenList.extend(exprlst)    # closure has multiple expr vs single expr.
        return flattenList

    # def visitExprs(self, cxt):
    #     exprsStep = Step().retrieve(cxt)
    #     exprsStep.interpret(self)               # process list of expressions
    #
    #     # keep the last expression for closure
    #     children = exprsStep.children()
    #     if children.hasKey('exprlst'):
    #         exprlst = children['exprlst']
    #         if isinstance(exprlst,List):    # exprs can be a single step.
    #             last = exprlst[-1]
    #             children.clear()
    #             children['exprlst'] = last
    #     return exprsStep


class RuntimeStep(Step):
    "Helper class for all steps that have runtime implications."
    def __init__(self): self.toKeep(true_)
    def isRuntime(self): return true_

    def run(self, scope):
        res = self.compileRes()
        self.runtimeRes(res)
        return res

class UnaryHeadStep(RuntimeStep):
    def visit(self, step): return step.visitUnaryHead(self)

    def _addToParent(self, interpreter, parentStep, toKeep):
        if self.children().len() == 1:
            parentStep.addStep(self.ruleName(), self.children().head())
        else:
            parentStep.addStep(self.ruleName(), self)
            if interpreter.toDebug(): print(f"  {self.ruleName()} add to instructions")
            interpreter.instructions().append(self)
        return self

    def invoke(self, scope, obj, unarytail):   # obj can be Python obj
        res = obj
        while unarytail.notNil():
            if unarytail.ruleName() == "unarytail":
                unarymsg = unarytail.getStep('unarymsg')
            else:
                unarymsg = unarytail
            op = unarymsg.compileRes()
            if op.notNil():             # op.isNil() for case like "7;"
                method = getattr(res, op, nil)  # Holder.valueFunc
                if method == nil and isinstance(res, SObject):
                    holder = res.metaclass().holderByName(op)
                    if holder.notNil():
                        method = holder.__get__(res)
                if method == nil: return nil
                if op == "value":           # value() should only be called from within ss.
                    res = method(scope)
                else:
                    res = method()
            unarytail = unarytail.getStep('unarytail')
        return res

    def run(self, scope):
        operand = self.getStep('operand')
        obj = operand.runtimeRes()
        unarytail = self.getStep('unarytail')
        res = obj
        if unarytail.notNil():
            res = self.invoke(scope, obj, unarytail)
        self.runtimeRes(res)
        return res

class BinHeadStep(RuntimeStep):
    operators = Holder().name('operators').type('Map').asClassType()

    def visit(self, step): return step.visitBinHead(self)

    def _addToParent(self, interpreter, parentStep, toKeep):
        if self.children().len() == 1:
            parentStep.addStep(self.ruleName(), self.children().head())
        else:
            parentStep.addStep(self.ruleName(), self)
            if interpreter.toDebug(): print(f"  {self.ruleName()} add to instructions")
            interpreter.instructions().append(self)
        return self

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

    def invoke(self, scope, obj, bintail):   # obj can be Python obj
        operators = self.operators()
        res = obj
        while bintail.notNil():
            if bintail.ruleName() == 'bintail':
                binmsg = bintail.getStep('binmsg')
            else:
                binmsg = bintail
            binop = binmsg.getStep('binop').compileRes()
            unaryhead = binmsg.getStep('unaryhead').runtimeRes()
            method = getattr(res, binop, nil)
            if method == nil:
                if binop in operators:
                    binop = operators[binop]
                method = getattr(res, binop, nil)
                if method == nil: return nil
            res = method(unaryhead)
            bintail = bintail.getStep('bintail')
        return res

    def run(self, scope):
        unaryhead = self.getStep('unaryhead')
        obj = unaryhead.runtimeRes()
        bintail = self.getStep('bintail')
        res = obj
        if bintail.notNil():
            res = self.invoke(scope, obj, bintail)
        self.runtimeRes(res)
        return res

class KwHeadStep(RuntimeStep):
    def visit(self, step): return step.visitKwHead(self)

    def _kwmsg(self, kwmsg):
        kwpairs = kwmsg.children().head()
        if not isinstance(kwpairs, List):
            kwpairs = List().append(kwpairs)
        kwMap = Map()
        for kwpair in kwpairs:
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
                    if param.kind == inspect.Parameter.VAR_POSITIONAL or \
                       param.kind == inspect.Parameter.VAR_KEYWORD or \
                       param.default is not inspect.Parameter.empty :
                        nDefault += 1
                if nArgs > nParam or nArgs < nParam - nDefault: continue
                params = List(signature.parameters.values())
                methods[name] = (nParam, nDefault, item)
        if fullname in methods: return methods[fullname][2]
        if prefix in methods: return methods[prefix][2]
        return nil

    def invoke(self, scope, obj, kwmsg):   # obj can be Python obj
        kwMap = self._kwmsg(kwmsg)
        prefix = kwMap.keys().head()
        fullname = prefix
        if kwMap.len() > 1:
            fullname = "".join([f"{key}__" for key in kwMap.keys()])

        method = nil
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

        # Invoke method through Python protocol
        if method == nil:
            res = nil
            nArgs = kwMap.len()
            method = self._methodLookup(obj, prefix, fullname, nArgs)

        if method != nil:
            if prefix == 'value':
                res = method(scope, *kwMap.values())
            else:
                res = method(*kwMap.values())
        return res

    def run(self, scope):
        unaryhead = self.getStep('unaryhead')
        obj = unaryhead.runtimeRes()
        kwmsg = self.getStep('kwmsg')
        res = obj
        if kwmsg.notNil():
            res = self.invoke(scope, obj, kwmsg)
        self.runtimeRes(res)
        return res

class ChainStep(RuntimeStep):
    def visit(self, step): return step.visitChain(self)

    def invoke(self, scope, obj, msg):
        res = obj
        tails = msg.children().values()
        for tail in tails:
            ruleName = tail.ruleName()
            if ruleName == 'kwmsg':
                res = KwHeadStep().invoke(scope, res, tail)
            elif ruleName == 'bintail':
                res = BinHeadStep().invoke(scope, res, tail)
            elif ruleName == 'unarytail':
                res = UnaryHeadStep().invoke(scope, res, tail)
        return res

    def run(self, scope):
        head = self.getStep('kwhead')
        if head.isNil():
           head = self.getStep('binhead')
        obj = head.runtimeRes()
        res = obj
        msgs = self.getStep('msg')
        if not isinstance(msgs, List):
            msgs = List().append(msgs)
        for msg in msgs:
            res = self.invoke(scope, res, msg)
        self.runtimeRes(res)
        return res

class ArrayStep(RuntimeStep):  # Serving both dynarr & litarr
    def visit(self, step): return step.visitArray(self)

    def _toList(self, steps):
        list = List()
        for step in steps:
            if isinstance(step, Step):
                list.append(step.runtimeRes())
            else:
                subList = self._toList(step)
                list.append(subList)
        return list

    def interpret(self, interpreter):   # for litarr
        super().interpret(interpreter)
        litarrcnt = self.getStep('litarrcnt') # self should be litarr
        if not isinstance(litarrcnt, List):
            if litarrcnt.isNil() or litarrcnt.compileRes().isNil():     # dynarr doesn't have litarrcnt
                litarrcnt = List()
            else:
                litarrcnt = List().append(litarrcnt)
        list = self._toList(litarrcnt)
        self.compileRes(list)
        self.runtimeRes(list)
        return self

    def run(self, scope):
        def toList(steps):
            list = List()
            for step in steps:
                if isinstance(step, Step):
                    list.append(step.runtimeRes())
                else:
                    subList = toList(step)
                    list.append(subList)
            return list

        steps = self.getStep('litarrcnt') # litarr
        if steps.notNil():
            res = self.compileRes()
            self.runtimeRes(res)
            return res
        steps = self.getStep('operand') # dynarr
        if steps.notNil():
            res = toList(steps)
            self.runtimeRes(res)
            return res

class AssignStep(RuntimeStep):
    def visit(self, step): return step.visitAssign(self)

    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.runtimeRes()
        res = self.getStep('expr').runtimeRes()
        refObj.setValue(ref.name(), res)
        self.runtimeRes(res)
        return res

class VarStep(RuntimeStep):
    def visit(self, step): return step.visitVar(self)

    def run(self, scope):
        ref = self.getStep('ref')
        refObj = ref.runtimeRes()
        res = refObj.getValue(ref.name())
        self.runtimeRes(res)
        return res

    def describe(self): return f"{self.getStep('ref').compileRes()}:{self.ruleName()}"

class RefStep(RuntimeStep):
    def visit(self, step): return step.visitRef(self)

    def run(self, scope):
        varname = self.compileRes()
        self.name(varname)
        obj = scope.lookup(varname)
        if obj.isNil(): obj = scope     # if @varname was not defined, consider it in local scope.
        self.runtimeRes(obj)
        return obj

class PrimitiveStep(RuntimeStep):
    def visit(self, step): return step.visitPrimitive(self)

    def interpret(self, interpreter):
        super().interpret(interpreter)
        primkey = self.getStep('primkey').compileRes()
        primtxt = self.getStep('primtxt').compileRes()
        map = Map().setValue(primkey, primtxt)
        self.compileRes(map)
        return self

class Interpreter(SObject, RuleContextVisitor):
    currentStep = Holder().name('currentStep')
    instructions = Holder().name('instructions').type('List')
    method = Holder().name('method')

    def visitWs(self, cxt): return nil
    def visitTerminal(self, tnode): return nil
    def visitPtfin(self, cxt): return nil
    def visitCommon(self, cxt): return Step().retrieve(cxt).interpret(self)
    def visitClosure(self, cxt): return ClosureStep().toKeep(true_).retrieve(cxt).interpret(self)

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

    def visitExprs(self, cxt): return Step().retrieve(cxt).interpret(self)
    def visitUnaryhead(self, cxt): return UnaryHeadStep().retrieve(cxt).interpret(self)
    def visitUnarytail(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitKwhead(self, cxt): return KwHeadStep().retrieve(cxt).interpret(self)
    def visitKwmsg(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitBinhead(self, cxt): return BinHeadStep().retrieve(cxt).interpret(self)
    def visitBintail(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitChain(self, cxt): return ChainStep().retrieve(cxt).interpret(self)
    def visitMsg(self, cxt): return Step().retrieve(cxt).toKeep(true_).interpret(self)
    def visitDynarr(self, cxt): return ArrayStep().retrieve(cxt).interpret(self)
    def visitLitarr(self, cxt): return ArrayStep().retrieve(cxt).interpret(self)
    def visitAssign(self, cxt): return AssignStep().retrieve(cxt).interpret(self)
    def visitVar(self, cxt): return VarStep().retrieve(cxt).interpret(self)
    def visitRef(self, cxt): return RefStep().retrieve(cxt).interpret(self)
    def visitChar(self, cxt): return Step().retrieve(cxt).interpret(self)
    def visitSymbol(self, cxt): return Step().retrieve(cxt).interpret(self)
    def visitPrimitive(self, cxt): return PrimitiveStep().retrieve(cxt).interpret(self)

    def visitBaresym(self, cxt):
        step = Step().retrieve(cxt)
        res = String(step.compileRes()[1:])     # "#abc" -> "abc"
        step.runtimeRes(res)
        return step

    def visitString(self, cxt):
        step = Step().retrieve(cxt)
        res = String(step.compileRes()[1:-1])     # "'abc'" -> "abc"
        step.runtimeRes(res)
        return step

    def visitSsFloat(self, cxt):
        step = Step().retrieve(cxt).interpret(self)
        f = Float(step.compileRes())
        number = Number().value(f)
        step.runtimeRes(number)
        return step

    def visitSsHex(self, cxt):
        step = Step().retrieve(cxt).interpret(self)
        n = Integer(int(step.compileRes(), 16))
        number = Number().value(n)
        step.runtimeRes(number)
        return step

    def visitSsInt(self, cxt):
        step = Step().retrieve(cxt).interpret(self)
        n = Integer(step.compileRes())
        number = Number().value(n)
        step.runtimeRes(number)
        return step

    def visitNum(self, cxt): return Step().retrieve(cxt).interpret(self)
