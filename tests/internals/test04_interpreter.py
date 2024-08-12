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

class Test_Interpreter1(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_method1(self):
        m = Method()
        ret = m()
        self.assertEqual(nil, ret)

    @skipUnless('TESTALL' in env, "disabled")
    def test500_primitives(self):
        #### Primitive: parser and run in interpreter.
        ss = "123"
        m = Method().interpret(ss)
        ret = m()
        self.assertEqual(123, ret)
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
        ret = Method().interpret(ss)(scope)
        self.assertEqual('aString', ret)
        self.assertEqual('aString', scope.getValue('obj'))

        # Local variable can be predefined.
        scope = rootContext.createScope()
        ss = "|obj|"
        ret = Method().interpret(ss)(scope)
        self.assertEqual(nil, ret)
        self.assertTrue(scope.hasKey('obj'))
        self.assertEqual(nil, scope.getValue('obj'))

        scope = rootContext.createScope()
        ss = "|obj1 obj2|"
        ret = Method().interpret(ss)(scope)
        self.assertTrue(scope.hasKey('obj1'))
        self.assertTrue(scope.hasKey('obj2'))

        # Predefined local variable will
        scope = rootContext.createScope()
        ss = "|obj| obj := 'aString'"
        ret = Method().interpret(ss)(scope)
        self.assertEqual('aString', ret)
        self.assertEqual('aString', scope.getValue('obj'))

    @skipUnless('TESTALL' in env, "disabled")
    def test520_param_access(self):
        scope = rootContext.createScope()
        ss = ":param1 | param1"
        method = Method().interpret(ss)
        ret = method(scope)
        self.assertEqual(nil, ret)
        self.assertTrue(not scope.hasKey('param1'))

        ret = method(scope, 'aString')
        self.assertEqual('aString', ret)
        self.assertTrue(scope.hasKey('param1'))

        ret = method(scope, 123)
        self.assertEqual(123, ret)
        ret = Method().interpret(ss)(scope)
        self.assertEqual(123, ret)  # ret is not nil as scope already have param1 assigned

        scope = rootContext.createScope()
        ss = ":param1 :param2| param2"
        method = Method().interpret(ss)
        ret = method(scope)
        self.assertEqual(nil, ret)
        self.assertTrue(not scope.hasKey('param1'))
        self.assertTrue(not scope.hasKey('param2'))

        ret = method(scope, 'str1')
        self.assertEqual(nil, ret)
        self.assertTrue(scope.hasKey('param1'))
        self.assertTrue(not scope.hasKey('param2'))

        ret = method(scope, 'str1', 'str2')
        self.assertEqual('str2', ret)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))

    @skipUnless('TESTALL' in env, "disabled")
    def test530_assignment(self):
        scope = rootContext.createScope()
        ss = "obj1 := 123"
        ret = Method().interpret(ss)()
        self.assertEqual(123, ret)
        self.assertTrue(123, scope.getValue('obj1'))

        ss = "obj1 := 'str1'"
        ret = Method().interpret(ss)()
        self.assertEqual('str1', ret)

        scope = rootContext.createScope()
        ss = ":param1 :param2| |tmp1| tmp1 := param2"
        method = Method().interpret(ss)
        ret = method(scope, 'str1', 'str2')
        self.assertEqual('str2', ret)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))
        self.assertTrue('str2', scope.getValue('tmp1'))

        ret = method(scope, 'str1', 123)
        self.assertEqual(123, ret)
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
        ret = Method().interpret(ss)(scope)
        self.assertEqual(123, ret)
        ss = "cattr12"
        ret = Method().interpret(ss)(scope)
        self.assertEqual('cvalue12', ret)

        ss = "attr11 := 321"
        ret = Method().interpret(ss)(scope)
        self.assertEqual(321, tobj.attr11())
        ss = "cattr12 := 'anotherValue'"
        ret = Method().interpret(ss)(scope)
        self.assertEqual('anotherValue', tobj.cattr12())

    @skipUnless('TESTALL' in env, "disabled")
    def test700_scope(self):
        # SObject protocol of Scope
        scope = Scope()
        self.assertEqual('a Scope', scope.name())
        ret = scope.name('scope')
        self.assertEqual('scope', scope.name())
        self.assertEqual(scope, ret)

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
        ret = scope.info()  # smoke test, ignore output
        # ret.print()

        scope = rootContext.createScope()
        root = scope['root']
        root['global1'] = nil
        ss = "global1 := 'global value'"
        ret = Method().interpret(ss)(scope)
        self.assertEqual('global value', scope['global1'])

if __name__ == '__main__':
    unittest.main()
