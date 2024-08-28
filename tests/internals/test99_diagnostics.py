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
# This won't run when "all_tests" is run
#  $ TESTALL=1 python -m unittest discover -s .

# @skip
class Test_Diagnostics(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Interpreter2').importSingleSObject(DebugMethod)

    @skipUnless('TESTALL' not in env, "disabled")
    def test100_hack(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = ":fullname | | tmp1 | tmp1 := fullname | + ', ' | + 'hello'"
        # ss = ":param1| param1 + 13"
        method = Method().name("test").interpret(ss)
        method.toPython()
        method.pysource().print()
        method.compile()
        res = method(scope, "John")
        self.assertEqual("John, hello", res)
        return

    @skip
    @skipUnless('TESTALL' not in env, "disabled")
    def test200_hack(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        def unnamed_b87a5abe86f2f8c9(scope):
            def unnamed_54d7d3621cab5729(scope, e):
                scope.vars()['e'] = e
                _ = 2 + scope["e"]
                return _

            _ = scope.newInstance('Method').takePyFunc(unnamed_54d7d3621cab5729).value(9)
            return _
        unnamed = Method().takePyFunc(unnamed_b87a5abe86f2f8c9)
        res = unnamed(scope)

        ss = "[ :e | 2 + e] value: 9"
        method = Method().interpret(ss)
        method.toPython()
        method.pysource().print()
        method.compile()
        res = method(scope)
        return

    @skip
    @skipUnless('TESTALL' not in env, "disabled")
    def test300_hack(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj
        # ss = "tobj | method14: 7 add: 3 | attr11 name | + tobj sobj11 attr11 + 2 + 4"

        # This is generated by method.pysource().print() below for easier debugging
        # as PyCharm needed to be restarted before it can debug into a generated tmp file.
        def test(scope):
            def unnamed_296d5eab92dbf300(scope):
                _ = 7 + scope["outer"]
                return _

            scope.vars()['outer'] = scope['nil']
            scope["outer"] = 13
            _ = scope.newInstance('Method').takePyFunc(unnamed_296d5eab92dbf300).value()
            return _

        unnamed = Method().takePyFunc(test)
        res = unnamed(scope)

        ss = ":param | | outer| outer := 13; [7 + outer] value + param"
        # ss = ":param | param"
        method = Method().name("test").interpret(ss)
        method.toPython()
        method.pysource().print()
        method.compile()
        res = method(scope, 5)
        self.assertEqual(25, res)
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

    @skip
    def test600_compile(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = f":param | param"
        method = Method().name('test').interpret(ss)
        method.toPython().pysource().print()
        method.compile()
        res = method(scope)
        return

    #### More Tests
    # SObj super: instance and class
    # packages
    # Python globals
