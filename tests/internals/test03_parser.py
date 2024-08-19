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

import unittest
from unittest import skip, skipUnless
from tests.TestBase import SmallScriptTest

from os import environ as env
env['TESTALL'] = '1'

from smallscript.SObject import *
from smallscript.Closure import Script

# Not all language features are implemented e.g. realtime dict, realtime literal.
# Will enhance upon future use cases.
# Here we test some major features.
class Test_Parser(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_smoke(self):
        # Simple case
        ss = "obj := 123"
        script = Script().parse(ss)
        self.assertTrue(script.noError())

        ret = script.toStringTree()
        self.assertTrue('obj' in ret)
        self.assertTrue('123' in ret)

        # Error case
        ss = "obj1 'abc'"
        script.parse(ss)
        self.assertTrue(script.hasError())
        errmsg = ("Syntax error at line 1:5: extraneous input ''abc'' expecting <EOF>\n"
                  "obj1 'abc'\n"
                  "     ^")
        self.assertTrue(errmsg, script.prettyErrorMsg())

    @skipUnless('TESTALL' in env, "disabled")
    def test500_assign_expr(self):
        script = Script()

        # assignment & ExpressionList
        ss = "var1 := 1"
        self.assertTrue(script.parse(ss).noError())
        ss = "var1 := root"
        self.assertTrue(script.parse(ss).noError())
        ss = "var1 := 'abc'"
        self.assertTrue(script.parse(ss).noError())
        ss = "var1 := root. var2 := var1"
        self.assertTrue(script.parse(ss).noError())
        ss = "a := b := 2"
        self.assertTrue(script.parse(ss).noError())
        ss = "var1 := root. var2 := _"
        self.assertTrue(script.parse(ss).noError())

    @skipUnless('TESTALL' in env, "disabled")
    def test510_messages(self):
        script = Script()

        # UnaryHead & UnaryTail
        ss = "obj1 attr3 name"
        self.assertTrue(script.parse(ss).noError())

        # KeywordHead
        ss = "obj1 name: 'abc'"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 method1__firstname: 'John' lastname: 'Doe'"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 attr1: 123. obj1 attr1"
        self.assertTrue(script.parse(ss).noError())

        # BinaryHead
        ss = "obj1 attr1: 1 + 2"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 attr1: 1 + 2 + obj1 var1"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 var1 + 1 + 2"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 var1 + obj1 var2"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 method3__var1: 3 + 4 var2: 2 + 3"
        self.assertTrue(script.parse(ss).noError())

    @skipUnless('TESTALL' in env, "disabled")
    def test520_cascade(self):
        script = Script()

        # Cascade
        ss = "7; + 3"
        self.assertTrue(script.parse(ss).noError())
        ss = "2; + 1; + 5" # Antlr ok, Amber fail
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 var1; +3"
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1; method4 attr7 + 3"                  # Amber fails as it is mixed unaryMsg and binMsg
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1; var1 + obj1 method4 attr7"          # Amber fails as it is mixed unaryMsg and binMsg
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1 var2: 7; var2; + 3" # ok
        self.assertTrue(script.parse(ss).noError())
        ss = "obj1; method4; method3__var1: 3 var2: 2; + obj1 var1; + 5" # ok
        self.assertTrue(script.parse(ss).noError())

    @skipUnless('TESTALL' in env, "disabled")
    def test530_subExpr(self):
        script = Script()

        # Subexpression
        ss = "(obj1 method4 method3__var1: 3 var2: 2) + obj1 var1 + 5"
        self.assertTrue(script.parse(ss).noError())
        ss = "(obj := obj1) var1"
        self.assertTrue(script.parse(ss).noError())
        ss = """(obj1 m1: 1) + (obj2 m2 m3) + 2"""
        self.assertTrue(script.parse(ss).noError())

    @skipUnless('TESTALL' in env, "disabled")
    def test540_block_closure(self):
        script = Script()

        # BlockClosure
        ss = "[ :e | | a | a:= e + 1]" # error, 'a:' parsed as a keyword.
        self.assertTrue(not script.parse(ss).noError())
        ss = "| tmp1 tmp2 | tmp1 := obj1 var1. tmp2 := tmp1 + 3. obj1 var2: tmp2 + 5. obj1 var2"
        self.assertTrue(script.parse(ss).noError())
        ss = "| tmp1 tmp2 | obj1 var1"
        self.assertTrue(script.parse(ss).noError())
        ss = "[2 + 3] value"
        self.assertTrue(script.parse(ss).noError())
        ss = "[ :e | 2 + e] value: 9"
        self.assertTrue(script.parse(ss).noError())
        ss = "b := [ :e | | a | a := e + 3]. b value: 9"
        script.parse(ss)
        self.assertTrue(script.parse(ss).noError())
        ss = 'b := [ :e | | a | a "comment" := [2 + 3] value + e]. b value: 9'
        self.assertTrue(script.parse(ss).noError())
        ss = "[[2 + 3] value + [3 - 2] value]"
        self.assertTrue(script.parse(ss).noError())

    @skipUnless('TESTALL' in env, "disabled")
    def test550_literal_array(self):
        script = Script()

        # LiteralArray
        ss = 'obj1 := $F'
        self.assertTrue(script.parse(ss).noError())
        ss = "#('a' 12 $F #root #(1 2) )"
        self.assertTrue(script.parse(ss).noError())

    @skipUnless('TESTALL' in env, "disabled")
    def test560_edge_case(self):
        script = Script()

        # Integer format
        ss = "abc := -123 + 1.2 + 1.0e-1 + 0x123"
        # ss = "abc := -123 + 1.2 + 1.0e-1"
        self.assertTrue(script.parse(ss).noError())

        # Primitive
        ss = f"<python: 'def hello:'>"
        self.assertTrue(script.parse(ss).noError())

if __name__ == '__main__':
    unittest.main()
