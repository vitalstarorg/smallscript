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
from smallscript.Closure import Script, Method
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14, DebugMethod

# Use this to test individual failed test cases.
# This won't run when "all tests" is run.
class Test_Diagnostics(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Interpreter2').importSingleSObject(DebugMethod)

    @skipUnless('TESTALL' not in env, "disabled")
    def test100_hack(self):
        scope = rootContext.createScope()

        ss = "#( #root #(1 2))"
        method = Method().interpret(ss); res = method(scope)
        self.assertListEqual(['root', [1,2]], res)

        ss = "#()"
        method = Method().interpret(ss); res = method(scope)
        self.assertListEqual([], res)

        ss = "#(#AAA)"
        method = Method().interpret(ss); res = method(scope)
        self.assertListEqual(['AAA'], res)

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
