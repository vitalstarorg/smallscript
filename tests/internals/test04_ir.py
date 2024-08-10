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

class Test_IntermediateRep(SmallScriptTest):
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

    @skipUnless('TESTALL' in env, "disabled")
    def test510_local_access(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(123)
        tobj.cattr12('cvalue12')

        # local getOrSet
        # param getOrSet
        # assignment
        # SObj attr: instance and class
        # SObj super: instance and class
        # simple instant method: interpreter vs compiled
        # simple class method: interpreter vs compiled
        # rootScope
            # packages
            # Python globals
        # Create new class with new method in interpreter mode. (Execution)
            # basically SObject mechanics is completed.


    def test600_method1(self):
        return
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(123)
        ss = 'attr11'
        scope = rootContext.createScope()
        scope.objs().append(tobj)
        m = Method().interpret(ss)
        ret = m(scope)


        # ss = ':e :f | |a b| obj := 123'
        # ss = '[:e :f | |a b| obj := 123]'
        ss = ':f | |a| obj := 123'
        m = Method().interpret(ss)
        scope = rootContext.createScope()
        ret = m(scope, 'arg1')
        ret = m('f')
        return
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()
        meta._getHolder('method14').print()
        tobj.method14()

        return

    def test990_hack1(self):
        return
        ss = "[:e :f| | a b | obj := 123]"
        script = Script().parse(ss)

        return

    def test990_hack99(self):
        return
        ss = "obj := 123"
        script = Script().parse(ss)
        ssStep = script.firstStep()
        # precompiler = ssStep.createPrecompiler()

        precompiler = Precompiler()
        ssStep.precompile(precompiler)



        return

if __name__ == '__main__':
    unittest.main()
