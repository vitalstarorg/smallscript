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

import copy
import re
import inspect
import io
import traceback
import tempfile
from graphviz import Digraph

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener

from smallscript.antlr.SmallScriptLexer import SmallScriptLexer as Lexer
from smallscript.antlr.SmallScriptParser import SmallScriptParser as Parser
from smallscript.antlr.SmallScriptListener import SmallScriptListener as Listener
from smallscript.Step import Step, StepVisitor, ClosureStep
from smallscript.SObject import *

class ScriptErrorListener(SObject, ErrorListener):
    errormsg = Holder().name('errormsg')
    def clear(self): return self.errormsg("")
    def hasError(self): return true_ if self.errormsg().notNil() else false_
    def __repr__(self): return f"error: {self.errormsg()}" if self.hasError() else "no error"
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        errmsg = f"Syntax error at line {line}:{column}: {msg}"
        self.errormsg(errmsg)
        return self

class ASTGrapher(Listener):
    def __init__(self):
        self.graph = Digraph('G', format='png')

    def enterEveryRule(self, ctx):
        rule_name = Parser.ruleNames[ctx.getRuleIndex()]
        # node_label = f"{rule_name}: {Trees.getNodeText(ctx, Parser.ruleNames)}"
        node_label = f"{rule_name}: {ctx.getText()}"
        self.graph.node(str(id(ctx)), node_label)

    def exitEveryRule(self, ctx):
        for child in ctx.getChildren():
            self.graph.edge(str(id(ctx)), str(id(child)))

    def visitTerminal(self, node):
        txt = node.getText()
        self.graph.node(str(id(node)), f"'{node.getText()}'", shape='box')

    def exitEveryRule(self, ctx):
        for child in ctx.getChildren():
            self.graph.edge(str(id(ctx)), str(id(child)))

class IRGrapher(StepVisitor):
    currentStep = Holder().name('currentStep')
    childName = Holder().name('childName').type('String')
    instructionIdx = Holder().name('instructionIdx').type('Map')

    def __init__(self):
        self.graph = Digraph('G', format='png')

    def __getattr__(self, item):
        def defaultVisit(step):
            return self.drawOval(step)
        return defaultVisit

    def walkOn(self, name, step, firstStep):
        "Depth-first walk on step."
        if not firstStep and isinstance(step, ClosureStep):
            self.childName(name)
            method = step.method()
            method.irGraph(self)
            return self
        currentStep = self.currentStep()
        children = List()
        # flatten child step in case it is a list.
        for chdName, chdStep in step.children().items():
            if isinstance(chdStep, List):
                children.extend([(chdName, child) for child in chdStep])
            else:
                children.append((chdName, chdStep))
        self.currentStep(step)
        for chdName, chd in children:
            self.walkOn(chdName, chd, false_)
            self.currentStep(step)
        self.currentStep(currentStep)
        self.childName(name)
        step.visit(self)
        return self

    def drawOval(self, step):
        return self.draw(step, 'oval')

    def drawBox(self, step):
        return self.draw(step, 'box')

    def draw3d(self, step):
        return self.draw(step, 'box3d')

    def draw(self, step, shape):
        childName = self.childName()
        currentStep = self.currentStep()
        currentStepId = hex(id(currentStep))
        assert not isinstance(currentStep, List), "currentStep shouldn't be a List."
        assert not isinstance(step, List), "step shouldn't be a List."
        ruleName = step.ruleName()
        compileRes = step.compileRes()
        runtimeRes = step.runtimeRes()
        stepId = hex(id(step))
        if currentStep.notNil():
            label = f"  {childName}"
            self.graph.edge(currentStepId, stepId, label=label)
            # print(f"{currentStepId} --{childName}--> {stepId}")
        index = self.instructionIdx().get(stepId, nil)
        nodeName = f"{ruleName}" if index == nil else f"#{index}\n{ruleName}"
        if compileRes.isNil() or ruleName == 'blk':
            self.graph.node(stepId, f"{nodeName}", shape=shape)
        else:
            self.graph.node(stepId, f"{nodeName}[''{runtimeRes}']", shape=shape)
        return self

    def visitStep(self, step): return self.drawBox(step)
    def visitClosure(self, step): return self.draw3d(step)

class Script(SObject):
    text = Holder().name('text').type('String')
    parser = Holder().name('parser')
    errorHandler = Holder().name('errorHandler')
    smallscriptStep = Holder().name('smallscriptStep').type('SmallScriptStep')

    def __init__(self): self.reset()
    def reset(self): return self.errorHandler(ScriptErrorListener())

    def parse(self, text=""):
        if text == nil:
            text = self.text()
        else:
            self.text(text)
        self.reset()
        text = self.text()
        lexer = Lexer(InputStream(text))
        stream = CommonTokenStream(lexer)
        parser = Parser(stream)
        errorHandler = self.errorHandler()
        lexer.removeErrorListeners()
        lexer.addErrorListener(errorHandler)
        parser.removeErrorListeners()
        parser.addErrorListener(errorHandler)
        ast = parser.smallscript()
        self.parser(parser)
        self.smallscriptStep().retrieve(ast)
        # self.smallscriptCxt(ast)
        return self

    def astGraph(self):
        listener = ASTGrapher()
        walker = ParseTreeWalker()
        walker.walk(listener, self.smallscriptStep().ruleCxt())
        return listener.graph

    def run(self):
        # runner = Runner()
        # walker = ParseTreeWalker()
        # walker.walk(runner, self.tree())
        return self

    def execute(self, context):
        # runner = Runner()
        # runner.script(self)
        # runner.context(context)
        # context.rungraph(nil)   # reset the rungraph
        # context.last_result(context)
        # walker = ParseTreeWalker()
        # walker.walk(runner, self.tree())
        # context.last_result(runner.result())
        return self

    def errormsg(self): return self.errorHandler().errormsg()
    def hasError(self): return self.errorHandler().hasError()
    def noError(self): return not self.hasError()

    def toStringTree(self):
        parser = self.parser()
        ast = self.smallscriptStep().ruleCxt()
        res = ast.toStringTree(recog=parser)
        return String(res)

    def prettyErrorMsg(self):
        errmsg = self.errormsg()
        if errmsg.isNil() or errmsg.isEmpty():
            return "no error found."
        pattern = r"line (\d+):(\d+):"
        match = re.search(pattern, errmsg)
        if match:
            line_num, column_num = match.groups()
            lines = self.text().split('\n')
            line = lines[int(line_num) - 1]
            msg = f"{errmsg}\n{line}\n{' ' * int(column_num)}^"
        else:
            msg = f"{errmsg}\nfind no location to error."
        return msg

    def info(self):
        if self.hasError():
            text = f"smallscript: <error>\n{self.text()}\n\n{self.prettyErrorMsg()}"
        else:
            text = f"smallscript: <no error>\n{self.text()}"
        return text

class SourceFile(SObject):
    filepath = Holder().name('filepath').type('String')

    def __del__(self):
        if self.filepath().notEmpty() and os.path.exists(self.filepath()):
            os.remove(self.filepath())
            self.filepath("")

class Method(SObject):
    "Works as a function encapsulation. Its object context is provided during method invocation."
    smallscript = Holder().name('smallscript').type('String')
    script = Holder().name('script').type('Script')
    interpreter = Holder().name('interpreter').type('Interpreter')
    params = Holder().name('params').type('List')
    tempvars = Holder().name('tempvars').type('List')
    sourceFile = Holder().name('sourceFile').type('SourceFile')
    pysource = Holder().name('pysource').type('String')
    pyfunc = Holder().name('pyfunc')
    pyerror = Holder().name('pyerror')

    # def value(self, *args, **kwargs):
    #     # @self @scope args...
    #     arglst = List(args)
    #     if arglst.isEmpty() or not isinstance(arglst.head(), Scope):
    #         local = self.getContext().createScope()
    #     else:
    #         scope = arglst.head()
    #         local = scope.createScope()
    #         this = scope.objs().head()
    #         local['self'] = this
    #         local.objs().append(this)
    #         arglst.pop(0)
    #     return self.__call__(local, *arglst, **kwargs)

    @Holder()
    def value(scope, *args, **kwargs):
        arglst = List(args)
        this = scope['self']
        return this.run(scope, *arglst, **kwargs)

    def __call__(self, *args, **kwargs):
        arglst = List(args)
        if arglst.isEmpty() or not isinstance(arglst.head(), Scope):
            scope = self.getContext().createScope()
        else:
            scope = arglst.head()
            arglst.pop(0)
        scope['self'] = scope.objs().head()
        return self.run(scope, *arglst)

    def run(self, scope, *params):
        if self.pyfunc() == nil:
            return self._runSteps(scope, *params)
        return self._runPy(scope, *params)

    def _runPy(self, scope, *params):
        "Using a compiled Python func to run this method."
        func = self.pyfunc()
        try:
            res = func(scope, *params)
        except Exception as e:
            # exceptString = traceback.format_exception(type(e), e, None)
            stackTrace = traceback.format_exc()
            self.log(f"pyfunc() execution\n{stackTrace}", 3)
            res = nil
        return res

    def _runSteps(self, scope, *params):
        "Use a precompiler instructions to run this method."
        for param, arg in zip(self.params(), params):
            scope[param] = arg
        for tmp in self.tempvars():
            scope[tmp] = nil
        instructions = self.interpreter().instructions()
        if instructions.isEmpty():
            currentStep = self.interpreter().currentStep()
            if currentStep.isNil(): return nil
            res = currentStep.children().head()
            if isinstance(res, Step) and res.hasKey('runtimeRes'):
                res = res.runtimeRes()
            return res
        res = nil
        for instruction in instructions:
            res = instruction.run(scope)
        return res

    def _getInterpreter(self): return self.interpreter()    # to be overridden
    def visit(self, visitor): return visitor.visitMethod(self)

    def interpret(self, smallscript=""):
        smallscript = self.asSObj(smallscript)
        if smallscript.isEmpty():
            smallscript = self.smallscript()
        script = self.script().parse(smallscript)
        if script.hasError():
            self.log(script.prettyErrorMsg(), 3)
            return nil
        smallscriptStep = script.smallscriptStep()
        interpreter = self._getInterpreter()
        interpreter.method(self)        # interpreter reference this method e.g. toDebug
        closure = smallscriptStep.getClosure(interpreter)
        if closure.notNil():
            method = closure.method()
            self.copyFrom(method)
        return self

    def compile(self, smallscript=""):
        if smallscript == "":
            if self.pyfunc() != nil: return self
            if self.pysource().notNil(): return self._compile()
            if self.interpreter().notNil():
                self.toPython()
                return self._compile()
            if self.smallscript().isNil():
                self.log("Warning: smallscript() is empty and nothing to compile.", Logger.LevelWarning)
                return self
            self.interpret()
        else:
            self.interpret(smallscript)
        self.toPython()
        return self._compile()

    def _compile(self):
        try:
            with tempfile.NamedTemporaryFile(dir="/tmp", suffix='.txt', mode='w', delete=False) as tempsrc:
                tempsrc.write(self.pysource())
                tempsrc.flush()
                self.sourceFile().filepath(tempsrc.name)
                compiled_method = compile(self.pysource(), tempsrc.name, 'exec')
            # compiled_method = compile(self.pysource(), '<string>', 'exec')
        except SyntaxError as e:
            if hasattr(e, 'text'):
                error_line = e.text.strip() if e.text is not None else ""
                caret_position = "^".rjust(e.offset, " ")  # Adjust caret position
                text = f"  File \"{e.filename}\", line {e.lineno}\n    {error_line}\n    {caret_position}{e.msg}"
            else:
                text = f"{e}"
            self.log(self.pysource(), 3)
            self.log(text, 3)
            self.pyerror(text)
        namespace = {}
        exec(compiled_method, namespace)
        pyfunc = namespace[self.name()]
        self.pyfunc(pyfunc)
        return self

    def toPython(self):
        ""
        coder = PythonCoder()
        pythonscript = self.visit(coder)
        self.pysource(pythonscript)
        return self

    def astGraph(self): return self.script().astGraph()

    def irGraph(self, grapher=nil):
        if grapher.isNil():
            grapher = IRGrapher()
        instructions = self.interpreter().instructions()
        instructionIdx = grapher.instructionIdx()
        for i in range(instructions.len()):
            instructionIdx[hex(id(instructions[i]))] = i
        grapher.walkOn('closure', self.interpreter().currentStep(), true_)
        return grapher.graph

    def takePyFunc(self, pyfunc):
        self.pyfunc(pyfunc)
        if pyfunc.__doc__ is not None:
            self.smallscript(pyfunc.__doc__)
        try:
            source = inspect.getsource(pyfunc)
        except Exception as e:
            source = nil
        if source != nil:
            self.pysource(source)
        signature = inspect.signature(pyfunc)
        funcargs = List([String(param.name) for param in signature.parameters.values()])
        funcargs = funcargs[1:]
        self.params(funcargs)
        self.name(pyfunc.__name__)
        return self

    def signature(self, name=""):
        params = self.params()
        pyfunc = self.pyfunc()
        signature = name = String(name)
        if name.isEmpty() and self.hasKey('name'): signature = name = self.name()
        if params.len() == 0:
            if pyfunc != nil: signature = pyfunc.__name__
        elif params.len() == 1:
            if name.notEmpty():
                signature = f"{name}__{params[0]}__"
            else:
                signature = f"{params[0]}"
        elif params.len() > 1:
            params = [f"{param}__" for param in params]
            signature = "".join(params)
            if name.notEmpty(): signature = f"{name}__{signature}"
        return String(signature)

    def unname(self, body=nil):
        if body == nil:
            body = self.getBody()
        if body == "":
            name = "unnamed_0"
        else:
            name = f"unnamed_{body.sha256()}"
        return name

    def getBody(self):
        source = self.pysource()
        if source.isNil() or source.isEmpty():
            return String("")
        body = source.split('\n', 1)[1]     # remove the first line
        return String(body)

    def info(self):
        info = self.script().info()
        return info

class Execution(SObject):
    "Execution provides a context linking a sobject with a method i.e. function encapsulation."
    this = Holder().name('this')
    context = Holder().name('context').type('Context')
    method = Holder().name('method').type('Method')

    def __call__(self, *args, **kwargs):
        method = self.method()
        params = List([self.asSObj(arg) for arg in args])
        scope = self.prepareScope()
        res = method.run(scope, *params)
        return res

    def _findScopeFromFrames(self):
        frame = inspect.currentframe()
        outer_frame = frame.f_back
        scope = nil
        while outer_frame is not None:
            scope = outer_frame.f_locals.get('scope', nil)
            if scope.notNil(): break
            outer_frame = outer_frame.f_back
        return scope

    def prepareScope(self):
        scopeVar = self._findScopeFromFrames()
        if scopeVar.isNil():
            scope = self.getContext().createScope().context(self.context())
        else:
            scope = scopeVar.createScope()
        scope.objs().append(self.this())
        scope.vars().setValue('self', self.this())
        return scope

    def visitSObj(self, sobj): return self.this(sobj)
    def visitMethod(self, method): return self.method(method)

class TextBuffer(SObject):
    delimiter = Holder().name('delimiter').type('String')
    useDelimiter = Holder().name('useDelimiter').type('True_')

    def skipFirstDelimiter(self): self.useDelimiter(false_); return self

    def textIO(self, output=''):
        output = self._getOrSet('output', output, nil)
        if output == nil:
            output = io.StringIO()
            self.setValue('output', output)
        return output

    def write(self, string):
        self.textIO().write(string)
        return self

    def writeWithDelimiter(self, string = ""):
        if not self.useDelimiter():
            self.textIO().write(string)
            self.useDelimiter(true_)
        else:
            self.textIO().write(self.delimiter())
            self.textIO().write(string)
        return self

    def text(self):
        text = self.textIO().getvalue()
        return String(text)

    def indent(self, padding="  "):
        # text = self._deindent()
        text = self.text().split("\n")
        indented = List()
        for line in text:
            if len(line) == 0:
                indented.append("")
            else:
                indented.append(f"{padding}{line}")
        res = "\n".join(indented)
        return String(res)

    def _deindent(self):
        noIndent = self.text()
        if noIndent.notEmpty():
            lines = noIndent.split("\n")
            first = lines[0]
            nspaces = len(first) - len(first.lstrip())
            noIndent = lines if nspaces == 0 else [line[nspaces:] for line in lines]
        return noIndent

class PythonCoder(SObject):
    delimiter = Holder().name('delimiter').type('String')
    methodsSource = Holder().name('methodsSource').type('TextBuffer')

    def firstArg(self, firstArg=''):
        firstArg = self._getOrSet('firstArg', firstArg, nil)
        if firstArg == nil:
            firstArg = 'scope'
            self.setValue('scope', firstArg)
        return firstArg

    def visit(self, step): return step.visit(self)

    def visitStep(self, step):
        value = step.runtimeRes()
        if value.isNil():
            value = step.compileRes()
        res = value.visit(self)
        return res

    def visitMethod(self, method):
        output = TextBuffer().delimiter("\n")
        output.skipFirstDelimiter()

        # params
        if method.params().notEmpty():
            for param in method.params():
                output.writeWithDelimiter(f"scope.vars()['{param}'] = {param}")
        # tempvars
        if method.tempvars().notEmpty():
            output.writeWithDelimiter()
            for tempVar in method.tempvars():
                output.write(f"scope.vars()['{tempVar}'] = ")
            output.write(f"{self.firstArg()}['nil']")
        # expressions
        closure = method.interpreter().currentStep()
        exprList = closure.flatten()
        for step in exprList[:-1]:
            res = step if step.isRuntime() else step.runtimeRes()
            res = res.visit(self)
            output.writeWithDelimiter(f"{res}")
        step = exprList[-1]
        res = step if step.isRuntime() else step.runtimeRes()
        res = res.visit(self)
        if res.startswith("_ = "):
            output.writeWithDelimiter(res)
        else:
            output.writeWithDelimiter(f"_ = {res}")
        output.writeWithDelimiter(f"return _")

        # method signature
        body = TextBuffer().delimiter("\n")
        body.write(self.methodsSource().text())
        body.writeWithDelimiter(output.text())
        final = body.indent('  ')
        name = method.name()
        if name.isEmpty():
            name = method.unname(final)
            method.name(name)
        parameters = ", ".join([self.firstArg()] + method.params())
        source = String(f"def {name}({parameters}):{final}")
        return source

    def visitChain(self, chain):
        operandStep = chain.getStep('kwhead')
        if operandStep.isNil(): operandStep = chain.getStep('binhead')
        operand = operandStep.visit(self)
        output = f"{operand}"
        msgs = chain.getStep('msg')
        if not isinstance(msgs, List):
            msgs = List().append(msgs)
        for msg in msgs:
            tails = msg.children().values()
            for tailStep in tails:
                tail = ""
                ruleName = tailStep.ruleName()
                if ruleName == 'kwmsg':
                    tail = self._visitKwMsg(tailStep)
                elif ruleName == 'bintail':
                    tail = self._visitBinTail(tailStep)
                elif ruleName == 'unarytail':
                    tail = self._visitUnaryTail(tailStep)
                output = f"({output}){tail}"
        return output

    def visitBlock(self, block):
        method = block.compileRes().method()
        source = method.toPython().pysource()
        self.methodsSource().delimiter("\n").writeWithDelimiter(source)
        res = String(f"{self.firstArg()}.newInstance('Method').takePyFunc({method.name()})")
        return res

    def _visitUnaryTail(self, unarytailStep):
        output = TextBuffer()
        while unarytailStep.notNil():
            if unarytailStep.ruleName() == "unarytail":
                unarymsg = unarytailStep.getStep('unarymsg')
            else:
                unarymsg = unarytailStep
            op = unarymsg.compileRes()
            if op.notNil():
                output.write(f".{op}()")
            unarytailStep = unarytailStep.getStep('unarytail')
        return output.text()

    def visitUnaryHead(self, unaryHead):
        operandStep = unaryHead.getStep('operand')
        operand = operandStep.visit(self)
        unarytailStep = unaryHead.getStep('unarytail')
        if unarytailStep.isNil(): return unaryHead
        output = TextBuffer()
        output.write(f"{operand}")
        tail = self._visitUnaryTail(unarytailStep)
        output.write(tail)
        return output.text()

    def _visitBinTail(self, bintailStep):
        output = TextBuffer()
        while bintailStep.notNil():
            binmsgStep = bintailStep.getStep('binmsg') \
                            if bintailStep.ruleName() == 'bintail' \
                            else bintailStep
            binop = binmsgStep.getStep('binop').compileRes()
            output.write(f" {binop}")
            operandStep = binmsgStep.getStep('unaryhead')
            operand = operandStep.visit(self)
            output.write(f" {operand}")
            bintailStep = bintailStep.getStep('bintail')
        return output.text()

    def visitBinHead(self, binhead):
        unaryHeadStep = binhead.getStep('unaryhead')
        unaryHead = unaryHeadStep.visit(self)
        bintailStep = binhead.getStep('bintail')
        if bintailStep.isNil(): return unaryHead
        output = TextBuffer()
        output.write(f"{unaryHead}")
        tail = self._visitBinTail(bintailStep)
        output.write(tail)
        return output.text()

    def _visitKwMsg(self, kwmsg):
        def _kwmsg(kwmsg):
            kwpairs = kwmsg.children().head()
            if not isinstance(kwpairs, List):
                kwpairs = List().append(kwpairs)
            kwMap = Map()
            for kwpair in kwpairs:
                ptkey = kwpair.children()['ptkey'].compileRes()[:-1]
                ptkey = String(ptkey)
                binheadStep = kwpair.children()['binhead']
                binhead = binheadStep.visit(self)
                kwMap[ptkey] = binhead
            return kwMap

        output = TextBuffer()
        kwMap = _kwmsg(kwmsg)
        prefix = kwMap.keys().head()
        fullname = prefix
        if kwMap.len() > 1:
            fullname = "".join([f"{key}__" for key in kwMap.keys()])
        kwOutput = TextBuffer().delimiter(", ").skipFirstDelimiter()
        kwOutput.write(f".{fullname}(")
        for parameter in kwMap.values():
            kwOutput.writeWithDelimiter(parameter.toString())
        kwOutput.write(')')
        output.write(kwOutput.text())
        return output.text()

    def visitKwHead(self, kwhead):
        def _kwmsg(kwmsg):
            kwpairs = kwmsg.children().head()
            if not isinstance(kwpairs, List):
                kwpairs = List().append(kwpairs)
            kwMap = Map()
            for kwpair in kwpairs:
                ptkey = kwpair.children()['ptkey'].compileRes()[:-1]
                binheadStep = kwpair.children()['binhead']
                binhead = binheadStep.visit(self)
                kwMap[ptkey] = binhead
            return kwMap

        unaryheadStep = kwhead.getStep('unaryhead')
        unaryhead = unaryheadStep.visit(self)
        kwmsg = kwhead.getStep('kwmsg')

        output = TextBuffer()
        output.write(f"{unaryhead}")
        msg = self._visitKwMsg(kwmsg)
        output.write(msg)
        return output.text()

    def visitArray(self, arrayStep):
        steps = arrayStep.getStep('litarrcnt') # litarr
        if steps.notNil():
            litarr = arrayStep.compileRes()
            litarrSrc = litarr.visit(self)
            return litarrSrc
        steps = arrayStep.getStep('operand') # dynarr
        if steps.notNil():
            dynaSrc = steps.visit(self)
            return dynaSrc

    def visitAssign(self, assignStep):
        refStep = assignStep.getStep('ref')
        ref = refStep.visit(self)
        exprStep = assignStep.getStep('expr')
        expr = exprStep.visit(self)
        assign = f"{ref} = {expr}"
        return assign

    def visitVar(self, varStep):
        refStep = varStep.getStep('ref')
        var = f"{self.firstArg()}[{refStep.compileRes().asString()}]"
        return String(var)

    def visitRef(self, refStep):
        ref = f"{self.firstArg()}[{refStep.compileRes().asString()}]"
        return String(ref)

    def visitList(self, list):
        output = TextBuffer()
        output.write(f"{self.firstArg()}.newInstance('List')")
        for e in list:
            eSrc = e.visit(self)
            output.write(f".append({eSrc})")
        return output.text()

    def visitMap(self, map):
        output = TextBuffer()
        output.write(f"{self.firstArg()}.newInstance('Map')")
        for k, v in map.items():
            kSrc = k.visit(self)
            vSrc = v.visit(self)
            output.write(f".setValue({kSrc}, {vSrc})")
        return output.text()

    def visitString(self, string): return string.asString()
    def visitNumber(self, number): return String(f"{number.value()}")

    def visitPrimitive(self, primitive):
        map = primitive.compileRes()
        src = map.visit(self)
        return src
