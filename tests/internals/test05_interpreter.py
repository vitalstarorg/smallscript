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
from smallscript.Closure import Script, Method
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14

class Test_Interpreter2(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_exprs(self):
        # Multiple expressions test
        scope = rootContext.createScope()
        ss = "obj2 := 222. obj1 := 111. obj3 := 333"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(333, res)
        self.assertEqual(111, scope.getValue('obj1'))
        self.assertEqual(222, scope.getValue('obj2'))
        self.assertEqual(333, scope.getValue('obj3'))

    @skipUnless('TESTALL' in env, "disabled")
    def test510_unaryhead(self):
        # Unary Head tests
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(123)
        tobj.cattr12('cvalue12')

        scope = rootContext.createScope()
        scope['tobj'] = tobj
        ss = "tobj sobj11"              # sobj11 is a SObject defined attribute
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual('TestSObj11', res.metaname())

        ss = "tobj sobj11 name"         # name is a SObject method
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual('a TestSObj11', res)

        ss = "tobj sobj11 toString"     # toString is a pure Python method
        method = Method().interpret(ss)
        res = method(scope)
        self.assertTrue('a TestSObj11:TestSObj11' in res)

        ss = "tobj method18 attr18_1"   # method18 is a method holder, attr18_1 is an attribute.
        method = Method().interpret(ss)
        res = method(scope)
        self.assertTrue('value18.1' in res)

    @skipUnless('TESTALL' in env, "disabled")
    def test520_kwhead(self):
        # Keyword Head tests
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(123)
        tobj.attr11('100')
        tobj.cattr12('200')

        # Simple python method invocation setting name
        scope = rootContext.createScope()
        scope['tobj'] = tobj
        ss = "tobj name: 'aaa'"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(tobj, res)
        self.assertEqual('aaa', tobj.name())
        self.assertTrue('aaa:TestSObj15' in res.toString())

        # Get or set instance and class attributes
        ss = "tobj attr11"
        res = Method().interpret(ss)(scope)
        self.assertEqual('100', res)

        ss = "tobj attr11: 123. tobj attr11"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(123, res)

        ss = "tobj cattr12"
        res = Method().interpret(ss)(scope)
        self.assertEqual('200', res)

        ss = "tobj cattr12: 123. tobj cattr12"
        res = Method().interpret(ss)(scope)
        self.assertEqual(123, res)

        # Invoke SObject instance method, doesn't have to be @arg, anything would work.
        ss = "tobj method16: 2 arg: 3"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(251, res)

        # Invoke SObject class method
        ss = "tobj cmethod17: 2 xxx: 3"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(129, res)

        # Invoke SObject instance method first__last__(first, last)
        ss = "tobj first: 'John' last: 'Doe'"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual("John, Doe", res)

        # first__arg__ not found
        ss = "tobj first: 'John' arg: 'Doe'"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(nil, res)

        # firstname__last__ not found 1st then try firstname(first, last)
        ss = "tobj firstname: 'John' last: 'Doe'"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual("John, Doe (123)", res)

    @skipUnless('TESTALL' in env, "disabled")
    def test530_binhead(self):
        # Binary Head Test
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()

        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "11 + 2 - 3 / 5 * 4"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(8, res)

        ss = "11 + tobj attr11"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(111, res)

        ss = "tobj cattr12: 11 + tobj attr11. tobj cattr12"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(111, res)

        ss = "tobj cattr12 + 89"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(200, res)

        ss = "tobj attr11 + tobj cattr12"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(211, res)

        ss = "tobj first: 'aa' + 'AA' last: 'bb' + 'BB'"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual("aaAA, bbBB", res)

    @skipUnless('TESTALL' in env, "disabled")
    def test540_cascade(self):
        # Cascade test
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()

        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "7;"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(7, res)

        ss = "7; + 3; + 2"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(12, res)

        ss = "2; + 1; + 5"          # Antlr ok, Amber fails
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(8, res)

        ss = "tobj; attr11: 7; attr11; + 2"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(9, res)

        ss = "tobj attr11; + 2"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(9, res)

        tobj.sobj11().attr11(13)
        ss = "tobj; sobj11 attr11"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(13, res)

        ss = "tobj; sobj11 attr11 + 2"              # Amber fails as it is mixed unaryMsg and binMsg
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(15, res)

        ss = "tobj; attr11 + tobj sobj11 attr11"    # Amber fails as it is mixed unaryMsg and binMsg
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(20, res)

        ss = "tobj attr11: 7; attr11; + 2"          # ok
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(9, res)

        ss = "tobj; method14: 7 add: 3; + tobj attr11; + tobj sobj11 attr11 + 2 + 4"
        # ss = "7; + tobj sobj11 attr11"
        method = Method().interpret(ss);
        res = method(scope)
        self.assertEqual(36, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test900_(self):
        return
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(123)
        tobj.cattr12('cvalue12')

        # SObj super: instance and class
        # simple instant method: interpreter vs compiled
        # simple class method: interpreter vs compiled
        # rootScope
            # packages
            # Python globals
        # Create new class with new method in interpreter mode. (Execution)
            # basically SObject mechanics is completed.

    def test_hack(self):
        return
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()

        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "7; + 3; + 2"
        # ss = "tobj; attr11: 7; attr11; + 2"
        # ss = "tobj; method16: 2 arg: 3; name: 'aa'; + 2"

        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(9, res)

        # Cascade
        # ss "7;"
        # ss = "7; + 3"
        # self.assertTrue(script.parse(ss).noError())
        # ss = "2; + 1; + 5" # Antlr ok, Amber fail
        # self.assertTrue(script.parse(ss).noError())
        # ss = "obj1 var1; +3"
        # self.assertTrue(script.parse(ss).noError())
        # ss = "obj1; method4 attr7 + 3"                  # Amber fails as it is mixed unaryMsg and binMsg
        # self.assertTrue(script.parse(ss).noError())
        # ss = "obj1; var1 + obj1 method4 attr7"          # Amber fails as it is mixed unaryMsg and binMsg
        # self.assertTrue(script.parse(ss).noError())
        # ss = "obj1 var2: 7; var2; + 3" # ok
        # self.assertTrue(script.parse(ss).noError())
        # ss = "obj1; method4; method3__var1: 3 var2: 2; + obj1 var1; + 5" # ok
        # self.assertTrue(script.parse(ss).noError())

        return


if __name__ == '__main__':
    unittest.main()
