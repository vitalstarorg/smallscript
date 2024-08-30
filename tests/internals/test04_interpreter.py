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
from smallscript.Closure import Script, Closure
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, DebugClosure
from tests.TestSObj14 import TestSObj14

# These are the basic tests with minimal language implementation.
class Test_Interpreter1(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_antlr(self):
        #### Simple case
        st = "obj := 123"
        script = Script().parse(st)
        self.assertTrue(script.noError())

        #### AST graph in form of text
        res = script.toStringTree()
        self.assertTrue('obj' in res)
        self.assertTrue('123' in res)

        #### AST graph of the syntax can be shown on nbs/antlr.ipynb
        dot = script.astGraph()
        dot_graph = dot.source.split('\n')
        self.assertEqual('digraph G {', dot_graph[0])

        #### Error case
        st = "obj1 'abc'"
        script.parse(st)
        self.assertTrue(script.hasError())
        errmsg = ("Syntax error at line 1:5: extraneous input ''abc'' expecting <EOF>\n"
                  "obj1 'abc'\n"
                  "     ^")
        self.assertTrue(errmsg, script.prettyErrorMsg())

    @skipUnless('TESTALL' in env, "disabled")
    def test110_empty_method(self):
        m = Closure()
        res = m()
        self.assertEqual(nil, res)

    # @skipUnless('TESTALL' in env, "disabled")
    def test510_local_access(self):
        #### local variable access
        # Variables first introduced will be created in local scope.
        # However, such update might be defined else where, so it is better to be predefined.
        scope = rootContext.createScope()
        ss = "obj := 'aString'"
        res = Closure().interpret(ss)(scope)
        self.assertEqual('aString', res)
        self.assertEqual('aString', scope.getValue('obj'))

        # Local variable can be predefined.
        scope = rootContext.createScope()
        ss = "|obj| obj := 'aString'"
        res = Closure().interpret(ss)(scope)
        self.assertEqual('aString', res)
        self.assertEqual('aString', scope.getValue('obj'))

    @skipUnless('TESTALL' in env, "disabled")
    def test520_param_access(self):
        scope = rootContext.createScope()
        ss = ":param1 | param1"
        closure = Closure().interpret(ss)
        res = closure(scope)
        self.assertEqual(nil, res)
        self.assertTrue(not scope.hasKey('param1'))

        res = closure(scope, 'aString')
        self.assertEqual('aString', res)
        self.assertTrue(scope.hasKey('param1'))

        res = closure(scope, 123)
        self.assertEqual(123, res)
        res = Closure().interpret(ss)(scope)
        self.assertEqual(123, res)  # res is not nil as scope already have param1 assigned

        scope = rootContext.createScope()
        ss = ":param1 :param2| param2"
        closure = Closure().interpret(ss)
        res = closure(scope)
        self.assertEqual(nil, res)
        self.assertTrue(not scope.hasKey('param1'))
        self.assertTrue(not scope.hasKey('param2'))

        res = closure(scope, 'str1')
        self.assertEqual(nil, res)
        self.assertTrue(scope.hasKey('param1'))
        self.assertTrue(not scope.hasKey('param2'))

        res = closure(scope, 'str1', 'str2')
        self.assertEqual('str2', res)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))

    @skipUnless('TESTALL' in env, "disabled")
    def test530_assignment(self):
        scope = rootContext.createScope()
        ss = "obj1 := 123"
        res = Closure().interpret(ss)(scope)
        self.assertEqual(123, res)
        self.assertTrue(scope.hasKey('obj1'))
        self.assertEqual(123, scope.getValue('obj1'))

        ss = "obj1 := 'str1'"
        res = Closure().interpret(ss)(scope)
        self.assertEqual('str1', res)

        scope = rootContext.createScope()
        ss = "_ := obj1 := 123"
        res = Closure().interpret(ss)(scope)
        self.assertEqual(123, res)
        self.assertEqual(123, scope.getValue('obj1'))
        self.assertEqual(123, scope.getValue('_'))

        scope = rootContext.createScope()
        ss = ":param1 :param2| |tmp1| tmp1 := param2"
        closure = Closure().interpret(ss)
        res = closure(scope, 'str1', 'str2')
        self.assertEqual('str2', res)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))
        self.assertTrue('str2', scope.getValue('tmp1'))

        res = closure(scope, 'str1', 123)
        self.assertEqual(123, res)
        self.assertTrue(123, scope.getValue('param2'))
        self.assertTrue(123, scope.getValue('tmp1'))

    @skipUnless('TESTALL' in env, "disabled")
    def test600_sobject(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(123)
        tobj.cattr12('cvalue12')

        scope = rootContext.createScope()
        scope.addObj(tobj)
        ss = "attr11"
        res = Closure().interpret(ss)(scope)
        self.assertEqual(123, res)
        ss = "cattr12"
        res = Closure().interpret(ss)(scope)
        self.assertEqual('cvalue12', res)

        ss = "attr11 := 321"
        res = Closure().interpret(ss)(scope)
        self.assertEqual(321, tobj.attr11())
        ss = "cattr12 := 'anotherValue'"
        res = Closure().interpret(ss)(scope)
        self.assertEqual('anotherValue', tobj.cattr12())

    @skipUnless('TESTALL' in env, "disabled")
    def test700_scope(self):
        # SObject protocol of Scope
        scope = Scope()
        self.assertEqual('', scope.name())
        self.assertEqual('a Scope', scope.describe())
        res = scope.name('scope')
        self.assertEqual('scope', scope.name())
        self.assertEqual(scope, res)

        # Get & set to scope will not affect SObject states e.g. name, metaname, etc.
        self.assertTrue(not scope.hasKey('name'))
        scope.setValue('name', 'sobj')
        self.assertTrue(scope.hasKey('name'))
        self.assertEqual('sobj', scope.getValue('name'))
        self.assertEqual('scope', scope.name())
        scope.delValue('name')
        self.assertTrue(not scope.hasKey('name'))
        self.assertEqual('scope', scope.name())

        scope['attr11'] = 'value11'
        scope['attr12'] = 'value12'
        scope2 = Scope().name('scope2')
        scope2['attr21'] = 'value21'
        scope.addScope(scope2)
        tobj = TestSObj14()
        tobj.attr11('tobj12')
        scope.addObj(tobj)
        res = scope.info()  # smoke test, ignore output
        # res.print()

        scope = rootContext.createScope()
        root = scope['root']
        root['global1'] = nil
        ss = "global1 := 'global value'"
        res = Closure().interpret(ss)(scope)
        self.assertEqual('global value', scope['global1'])

if __name__ == '__main__':
    unittest.main()
