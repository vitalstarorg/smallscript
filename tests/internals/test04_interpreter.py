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
from tests.TestBase import SmallScriptTest, TestSObj14, DebugMethod

# These are the basic tests with minimal language implementation.
class Test_Interpreter1(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_method1(self):
        m = Method()
        res = m()
        self.assertEqual(nil, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test500_primitives(self):
        #### Primitive: parser and run in interpreter.
        ss = "123"
        method = Method().interpret(ss)
        res = method()
        self.assertEqual(123, res)
        ss = "'123'"
        self.assertEqual('123', Method().interpret(ss)())
        ss = "true"
        self.assertEqual(true_, Method().interpret(ss)())
        ss = "false"
        self.assertEqual(false_, Method().interpret(ss)())
        ss = "nil"
        self.assertEqual(nil, Method().interpret(ss)())
        ss = "context"
        context = Method().interpret(ss)()
        self.assertEqual(rootContext, context)
        ss = "root"
        rootScope = Method().interpret(ss)()
        self.assertEqual(rootContext, rootScope['context'])

    # @skipUnless('TESTALL' in env, "disabled")
    def test510_local_access(self):
        #### local variable access
        # Variables first introduced will be created in local scope.
        # However, such update might be defined else where, so it is better to be predefined.
        scope = rootContext.createScope()
        ss = "obj := 'aString'"
        res = Method().interpret(ss)(scope)
        self.assertEqual('aString', res)
        self.assertEqual('aString', scope.getValue('obj'))

        # Local variable can be predefined.
        scope = rootContext.createScope()
        ss = "|obj| obj := 'aString'"
        res = Method().interpret(ss)(scope)
        self.assertEqual('aString', res)
        self.assertEqual('aString', scope.getValue('obj'))

    @skipUnless('TESTALL' in env, "disabled")
    def test520_param_access(self):
        scope = rootContext.createScope()
        ss = ":param1 | param1"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(nil, res)
        self.assertTrue(not scope.hasKey('param1'))

        res = method(scope, 'aString')
        self.assertEqual('aString', res)
        self.assertTrue(scope.hasKey('param1'))

        res = method(scope, 123)
        self.assertEqual(123, res)
        res = Method().interpret(ss)(scope)
        self.assertEqual(123, res)  # res is not nil as scope already have param1 assigned

        scope = rootContext.createScope()
        ss = ":param1 :param2| param2"
        method = Method().interpret(ss)
        res = method(scope)
        self.assertEqual(nil, res)
        self.assertTrue(not scope.hasKey('param1'))
        self.assertTrue(not scope.hasKey('param2'))

        res = method(scope, 'str1')
        self.assertEqual(nil, res)
        self.assertTrue(scope.hasKey('param1'))
        self.assertTrue(not scope.hasKey('param2'))

        res = method(scope, 'str1', 'str2')
        self.assertEqual('str2', res)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))

    @skipUnless('TESTALL' in env, "disabled")
    def test530_assignment(self):
        scope = rootContext.createScope()
        ss = "obj1 := 123"
        res = Method().interpret(ss)(scope)
        self.assertEqual(123, res)
        self.assertTrue(scope.hasKey('obj1'))
        self.assertEqual(123, scope.getValue('obj1'))

        ss = "obj1 := 'str1'"
        res = Method().interpret(ss)(scope)
        self.assertEqual('str1', res)

        scope = rootContext.createScope()
        ss = "_ := obj1 := 123"
        res = Method().interpret(ss)(scope)
        self.assertEqual(123, res)
        self.assertEqual(123, scope.getValue('obj1'))
        self.assertEqual(123, scope.getValue('_'))

        scope = rootContext.createScope()
        ss = ":param1 :param2| |tmp1| tmp1 := param2"
        method = Method().interpret(ss)
        res = method(scope, 'str1', 'str2')
        self.assertEqual('str2', res)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))
        self.assertTrue('str2', scope.getValue('tmp1'))

        res = method(scope, 'str1', 123)
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
        res = Method().interpret(ss)(scope)
        self.assertEqual(123, res)
        ss = "cattr12"
        res = Method().interpret(ss)(scope)
        self.assertEqual('cvalue12', res)

        ss = "attr11 := 321"
        res = Method().interpret(ss)(scope)
        self.assertEqual(321, tobj.attr11())
        ss = "cattr12 := 'anotherValue'"
        res = Method().interpret(ss)(scope)
        self.assertEqual('anotherValue', tobj.cattr12())

    @skipUnless('TESTALL' in env, "disabled")
    def test700_scope(self):
        # SObject protocol of Scope
        scope = Scope()
        self.assertEqual('a Scope', scope.name())
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
        res = Method().interpret(ss)(scope)
        self.assertEqual('global value', scope['global1'])

    @skipUnless('TESTALL' in env, "disabled")
    def test800_block(self):
        scope = rootContext.createScope()
        ss = "[:param1 | param1]"
        block = Method().interpret(ss)
        closure = block(scope)
        res = closure(scope, 'aString')
        self.assertEqual('aString', res)

if __name__ == '__main__':
    unittest.main()
