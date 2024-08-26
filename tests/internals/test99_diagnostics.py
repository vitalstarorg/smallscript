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

from unittest import skip, skipUnless

from os import environ as env

from smallscript.SObject import *
from smallscript.Closure import Method
# from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14, DebugMethod

# Use this to test individual failed test cases.
# This won't run when "all tests" is run.
class Test_Diagnostics(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Interpreter2').importSingleSObject(DebugMethod)

    # @skipUnless('TESTALL' not in env, "disabled")
    # def test100_hack(self):
    #     pkg = rootContext.loadPackage('tests')
    #     tobj = TestSObj14()
    #     tobj.attr11(100)
    #     tobj.cattr12('200')
    #     metaclass = tobj.metaclass()
    #     scope = rootContext.createScope()
    #     scope['tobj'] = tobj
    #
    #     ss = f"<python: 'def hello:'>"
    #     method = Method().interpret(ss)
    #     method.toPython().pysource().print()
    #     method.compile()
    #     res = method(scope)
    #     return

    @skipUnless('TESTALL' not in env, "disabled")
    def test200_hack(self):
        def unnamed_b362c57d9738671d(scope):
            def unnamed_3a990f8976cd0a1a(scope, e):
                scope.vars()['e'] = e
                _ = 2 + scope['e']
                return _

            _ = scope.newMethod().takePyFunc(unnamed_3a990f8976cd0a1a).value(9)
            return _

        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        unnamed = Method().takePyFunc(unnamed_b362c57d9738671d)
        res = unnamed(scope)
        return

        ss = "[ :e | 2 + e] value: 9"
        method = Method().interpret(ss)
        method.toPython()
        method.pysource().print()

        return

    @skipUnless('TESTALL' not in env, "disabled")
    def test300_hack(self):
        def unnamed_93c1ff468efbfac0(scope):
            def unnamed_b10200f5b89d10a9(scope):
                _ = 7 + scope['outer']
                return _

            scope.vars()['outer'] = scope['nil']
            scope['outer'] = 13
            _ = scope.newInstance('Method').takePyFunc(unnamed_b10200f5b89d10a9).value()
            return _

        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj
        # ss = "tobj | method14: 7 add: 3 | attr11 name | + tobj sobj11 attr11 + 2 + 4"

        # unnamed = Method().takePyFunc(unnamed_93c1ff468efbfac0)
        # res = unnamed(scope)
        # return

        ss = "| outer| outer := 13; [7 + outer] value"
        # ss = ":param | param"
        method = Method().interpret(ss)
        method.toPython()
        method.pysource().print()
        method.compile()
        res = method(scope)
        self.assertEqual(20, res)
        return

    @skip
    def test500_DebugMethod(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "123 + 1.2"; expect = 124.2
        method = DebugMethod()
        # method.toDebug(true_).loglevel(0)
        method.interpret(ss)
        # method.toDebug(true_).loglevel(0)
        res = method(scope)
        self.assertEqual(expect, res)
        return

    #### More Tests
    # SObj super: instance and class
    # simple instant method: interpreter vs compiled
    # simple class method: interpreter vs compiled
    # rootScope
    # packages
    # Python globals
    # Create new class with new method in interpreter mode. (Execution)
    # basically SObject mechanics is completed.
