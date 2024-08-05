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
from tests.TestBase import *

class Test_IntermediateRep(SmallScriptTest):

    def test500_method1(self):
        return
        st = ':e :f | |a b| obj := 123'
        m = Method().compile(st)
        pkg = root.loadPackage('tests.internals')
        pkg.importMethods()
        tobj = TestSObj4()
        tobj.metaclass().getHolder('method14').print()
        tobj.method14()

        return

    def test990_hack1(self):
        # return
        pkg = root.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()

        # meta.getHolder('method14').print()

        self.assertTrue(not tobj.hasKey('attr11'))
        self.assertEqual('', tobj.attr11())
        self.assertTrue(tobj.hasKey('attr11'))
        tobj.attr11('value11')
        self.assertEqual('value11', tobj.attr11())

        self.assertTrue(not tobj.metaclass().attrs().hasKey('cattr12'))
        self.assertEqual('', tobj.cattr12())
        self.assertTrue(tobj.metaclass().attrs().hasKey('cattr12'))
        tobj.cattr12('value12')
        self.assertEqual('value12', tobj.cattr12())

        # ret = TestSObj14.method14(1, 2)
        # ret = TestSObj14.cmethod15(2, 3)

        # ret = TestSObj14.method14
        # holder1 = TestSObj14.method14.holder
        holder2 = tobj.metaclass().getHolder('method14')
        ret = tobj.method14(1, 2)
        self.assertEqual(3, ret)

        ret = tobj.cmethod15(2, 3)      # class
        self.assertEqual(6, ret)

        ret = TestSObj14.attr11('value11')
        self.assertEqual(nil, ret)
        ret = TestSObj14.cattr12('value12_')
        self.assertEqual(meta.attrs(), ret)
        ret = TestSObj14.cattr12()
        self.assertEqual('value12_', ret)


        tobj.attr11('100')
        ret = tobj.method16(1, 2)
        self.assertEqual(103, ret)
        ret = TestSObj14.method16(1, 2)
        self.assertEqual(nil, ret)
        ret = tobj.method17(3, 2)
        self.assertEqual(6, ret)
        ret = TestSObj14.method17(3, 2)
        self.assertEqual(6, ret)

        return
        ret = TestSObj14.method14(1, 2)
        ret = TestSObj14.cmethod15(2, 3)

        meta.attr11('value11')
        meta.cattr12('value12')
        meta.method14(1,2,3)
        meta.cmethod15(1, 2)
        return

    def test990_hack99(self):
        return
        st = "obj := 123"
        script = Script().compile(st)
        ssStep = script.firstStep()
        precompiled = ssStep.precompile()
        # m = Method().compile(st)
        return

if __name__ == '__main__':
    unittest.main()
