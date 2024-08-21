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
# env['TESTALL'] = '1'

from smallscript.SObject import *
from smallscript.Closure import Script, Method
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14, DebugMethod

class Test_Interpreter2(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Interpreter2').importSingleSObject(DebugMethod)

    @skipUnless('TESTALL' in env, "disabled")
    def test500_exprs(self):
        # Multiple expressions test
        scope = rootContext.createScope()
        ss = "obj2 := 222; obj1 := 111; obj3 := 333"
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

        ss = "tobj sobj11 describe"         # name is a SObject method
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

        ss = "tobj attr11: 123; tobj attr11"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(123, res)

        ss = "tobj cattr12"
        res = Method().interpret(ss)(scope)
        self.assertEqual('200', res)

        ss = "tobj cattr12: 123; tobj cattr12"
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

        ss = "tobj cattr12: 11 + tobj attr11; tobj cattr12"
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
    def test540_chain(self):
        # Chain test
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "7 |"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(7, res)

        ss = "7 | + 3 | + 2"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(12, res)

        ss = "2 | + 1 | + 5"          # Antlr ok, Amber fails
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(8, res)

        ss = "tobj | attr11: 7 | attr11 | + 2"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(9, res)

        ss = "tobj attr11 | + 2"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(9, res)

        tobj.sobj11().attr11(13)
        ss = "tobj | sobj11 attr11"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(13, res)

        ss = "tobj | sobj11 attr11 + 2"              # Amber fails as it is mixed unaryMsg and binMsg
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(15, res)

        ss = "tobj | attr11 + tobj sobj11 attr11"    # Amber fails as it is mixed unaryMsg and binMsg
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(20, res)

        ss = "tobj attr11: 7 | attr11 | + 2"          # ok
        method = Method().interpret(ss);
        res = method(scope)
        self.assertEqual(9, res)

        ss = "tobj | method14: 7 add: 3 | + tobj attr11 | + tobj sobj11 attr11 + 2 + 4"
        # ss = "7 | + tobj sobj11 attr11"
        method = Method().interpret(ss);
        res = method(scope)
        self.assertEqual(36, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test550_subexpr(self):
        # Subexpression test
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14(); tobj.attr11(100); tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "(7 + 3)"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(10, res)

        ss = "(tobj method14: 7 add: 3)"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(10, res)

        ss = "(tobj method14: 7 add: 3) + tobj attr11 + 5"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(115, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test600_block_closure(self):
        # block closure test
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "| tmp1 tmp2 | tmp1 := tobj attr11; tmp2 := tmp1 + 3; tobj cattr12: tmp2 + 5; tobj cattr12"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(108, res)

        ss = "| tmp1 tmp2 | tobj attr11"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(100, res)

        ss = "[2 + 3] value"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(5, res)

        ss = "[ :e | 2 + e] value: 9"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(11, res)

        # closure is a functional can be assigned to a variable.
        ss = "b := [ :e | | a | a := e + 3]; b value: 9"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(12, res)

        #  b.value(...) is always run under a new scope.
        ss = "b := [ :e | | a | a := e + 3]; b value: 9; b value: 10"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(13, res)

        # closure can be nested.
        ss = """
            // comment
            b := [ :e | | a | a := [2 + 3] value + e]; b value: 9;
            '''heredoc comment'''
            """
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(14, res)

        # Block would return unexecuted closure. Method object works as a block.
        ss = "[[2 + 3] value + [3 - 2] value]"
        method = Method().interpret(ss); block = method(scope)
        res = block()   # execute "[2 + 3] value + [3 - 2] value"
        self.assertEqual(6, res)

        # Nested closure can access outer scope variable
        ss = "| outer| outer := 13; [7 + outer] value"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(20, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test700_literal_array(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = 'obj1 := $F'
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual('$F', scope['obj1'])

        ss = 'obj1 := #F'
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual('F', scope['obj1'])

        ss = "#()"
        method = Method().interpret(ss); res = method(scope)
        self.assertListEqual([], res)

        ss = "#(#AAA)"
        method = Method().interpret(ss); res = method(scope)
        self.assertListEqual(['AAA'], res)

        ss = "#( #root #(1 2))"
        method = Method().interpret(ss); res = method(scope)
        self.assertListEqual(['root', [1,2]], res)

        ss = "#( 'a' 12 $F #root #(1 2) #(1 #root) )"
        method = Method().interpret(ss); res = method(scope)
        expect = List().append('a').append(12).append('$F').append('root')\
                .append([1,2]).append([1, 'root'])
        self.assertListEqual(expect, res)

        ss = "#{ 'a' 12 $F true 'root' #(1 2) #{1 #root} root }"
        method = Method().interpret(ss); res = method(scope)
        expect = List().append('a').append(12).append('$F').append(true_).append('root')\
                .append([1,2]).append([1,'root']).append(rootContext.rootScope())
        self.assertEqual(expect, res)

        ss = "#(-123 1.2 1.0e-1 0x123)"
        expect = [-123, 1.2, 0.1, 291]
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(expect, res)

        ss = "#(-123 1.2 1.0e-1 0x123)"
        expect = [-123, 1.23, 0.1, 291]
        method = Method().interpret(ss); res = method(scope)
        self.assertNotEqual(expect, res)

        ss = "123 + 1.2"; expect = 124.2
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(expect, res)

        ss = "-123 + 1.2 + 1.0e-1 + 0x123"
        expect = 169.3
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual(expect, res)

        ss = f"<python: 'def hello:'>"
        method = Method().interpret(ss); res = method(scope)
        self.assertEqual({'python:': "'def hello:'"}, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test800_parsing_errors(self):
        # Parsing errors
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14(); tobj.attr11(100); tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = "1+2-3"                            # need to fix the grammar
        method = Method().loglevel(4).interpret(ss)
        self.assertEqual(nil, method)
            # extraneous input '-3' expecting
            # 1+2-3
            #    ^

        ss = "|obj|"
        method = Method().loglevel(4).interpret(ss)
        self.assertEqual(nil, method)
            # | obj1 |
            #         ^

        ss = "|obj1 obj2|"
        method = Method().loglevel(4).interpret(ss)
        self.assertEqual(nil, method)
            # | obj1 obj2 |
            #              ^

        ss = "[ :e | | a | a:= e + 1]"          # error, 'a:' parsed as a keyword.
        method = Method().loglevel(4).interpret(ss)
        self.assertEqual(nil, method)
            # [: e | | a | a:= e + 1]
            #              ^

if __name__ == '__main__':
    unittest.main()
