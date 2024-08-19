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
from graphviz import Digraph
import logging

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees

from smallscript.antlr.SmallScriptLexer import SmallScriptLexer as Lexer
from smallscript.antlr.SmallScriptParser import SmallScriptParser as Parser
from smallscript.antlr.SmallScriptListener import SmallScriptListener as Listener
# from smallscript.Step import Step, Precompiler
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

class DOTGrapher(Listener):
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

class Script(SObject):
    text = Holder().name('text').type('String')
    parser = Holder().name('parser')
    errorHandler = Holder().name('errorHandler')
    smallscriptStep = Holder().name('smallscriptStep').type('SmallScriptStep')
    # smallscriptCxt = Holder().name('smallscriptCxt')

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

    def dotGraph(self):
        listener = DOTGrapher()
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

        # 'context': 'Context',
        # 'smallscript': 'String',
        # 'closure': 'nil',
        # 'pythonscript': 'String',
        # 'pythonerror': 'String',
        # 'pythonfinal': 'String',
        # 'pythonmethod': 'nil',
        # 'methods': 'Map',
class Method(SObject):
    "Works as a function encapsulation. Its object context is provided during method invocation."
    smallscript = Holder().name('smallscript').type('String')
    script = Holder().name('script').type('Script')
    interpreter = Holder().name('interpreter').type('Interpreter')
    params = Holder().name('params').type('List')
    tempvars = Holder().name('tempvars').type('List')
    pyfunc = Holder().name('pyfunc')
    pysource = Holder().name('pysource')

    def value(self, *args, **kwargs):
        # @self @scope args...
        arglst = List(args)
        if arglst.isEmpty() or not isinstance(arglst.head(), Scope):
            local = self.getContext().createScope()
        else:
            scope = arglst.head()
            local = scope.createScope()
            this = scope.objs().head()
            local['self'] = this
            local.objs().append(this)
            arglst.pop(0)
        return self.__call__(local, *arglst, **kwargs)

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
        for param, arg in zip(self.params(), params):
            scope[param] = arg
        for tmp in self.tempvars():
            scope[tmp] = nil
        if self.pyfunc() == nil:
            return self._runSteps(scope, *params)
        return self._runPy(scope, *params)

    def _runPy(self, scope, *params):
        "Using a compiled Python func to run this method."
        func = self.pyfunc()
        try:
            res = func(scope, *params)
        except Exception as e:
            logging.error("pyfunc() execution", exc_info=True)
            res = nil
        return res

    def _runSteps(self, scope, *params):
        "Use a precompiler instructions to run this method."
        instructions = self.interpreter().instructions()
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

    def takePyFunc(self, pyfunc):
        self.pyfunc(pyfunc)
        if pyfunc.__doc__ is not None:
            self.smallscript(pyfunc.__doc__)
        try:
            source = inspect.getsource(pyfunc)
        except Exception as e:
            # logging.error("OSError, can't get source", exc_info=True)
            source = nil
        if source != nil:
            self.pysource(source)
        signature = inspect.signature(pyfunc)
        funcargs = List([String(param.name) for param in signature.parameters.values()])
        funcargs = funcargs[1:]
        self.params(funcargs)
        self.name(pyfunc.__name__)
        return self

    def compileThis(self, smallscript = ""):
        """Try to compile to python func whatever is available."""
        # script = self.asObj(smallscript)
        # if script.notEmpty():
        #     self.smallscript(script)
        # if self.smallscript().notEmpty():
        #     self.encode()
        # if self.closure().not_nil():
        #     # method may acquire closure first, so refill the smallscript in return.
        #     if self.smallscript().isEmpty():
        #         self.smallscript(self.closure().smallscript())
        #     self.args(self.closure().args())
        #     self.decode()
        # if self.pythonscript().notEmpty():
        #     self.compile()
        return self

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

    def prepareScope(self):
        scope = self.getContext().createScope().context(self.context())
        scope.objs().append(self.this())
        scope.setValue('self', self.this())
        return scope

    def visitSObj(self, sobj): return self.this(sobj)
    def visitMethod(self, method): return self.method(method)

