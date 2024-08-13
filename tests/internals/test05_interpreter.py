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
        scope = rootContext.createScope()
        ss = "obj2 := 222. obj1 := 111. obj3 := 333"
        method = Method().interpret(ss)
        ret = method(scope)
        self.assertEqual(333, ret)
        self.assertEqual(111, scope.getValue('obj1'))
        self.assertEqual(222, scope.getValue('obj2'))
        self.assertEqual(333, scope.getValue('obj3'))

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
        tobj = TestSObj14().attr11(123)
        tobj.cattr12('cvalue12')

        scope = rootContext.createScope()
        scope['tobj'] = tobj
        # ss = "tobj sobj11 name"
        ss = "tobj sobj11"
        method = Method().interpret(ss)
        ret = method(scope)
        self.assertEqual(333, ret)


        return


if __name__ == '__main__':
    unittest.main()
