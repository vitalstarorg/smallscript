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
from smallscript.Step import Step
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
    smallscriptCxt = Holder().name('smallscriptCxt')

    def __init__(self): self.reset()
    def reset(self): return self.errorHandler(ScriptErrorListener())

    def compile(self, text=""):
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
        self.smallscriptCxt(ast)
        return self

    def firstStep(self):
        sscxt = self.smallscriptCxt()
        ssStep = Step().name('smallscript').ruleCxt(sscxt)
        return ssStep

    def dotGraph(self):
        listener = DOTGrapher()
        walker = ParseTreeWalker()
        walker.walk(listener, self.smallscriptCxt())
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
        ast = self.smallscriptCxt()
        ret = ast.toStringTree(recog=parser)
        return String(ret)

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

        # 'smallscript': 'String',
        # 'args': 'List',
        # 'runnerList': 'List',
        # 'scope': 'Scope',       # internal scope object from the last runner in runnerList.

        # 'context': 'Context',
        # 'smallscript': 'String',
        # 'args': 'List',
        # 'closure': 'nil',
        # 'pythonscript': 'String',
        # 'pythonerror': 'String',
        # 'pythonfinal': 'String',
        # 'pythonmethod': 'nil',
        # 'methods': 'Map',
class Method(SObject):
    smallscript = Holder().name('smallscript').type('String')
    script = Holder().name('script').type('Script')
    precompiled = Holder().name('precompiled')

    def compile(self, smallscript=""):
        smallscript = self.asSObj(smallscript)
        if smallscript.isEmpty():
            smallscript = self.smallscript()
        script = self.script().compile(smallscript)
        # if script.hasError():
        #     return nil
        ssStep = script.firstStep()
        precompiled = ssStep.precompile()
        self.precompiled(precompiled)
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