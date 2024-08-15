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

class Test_Method(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_method(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()

        # Instance attribute behavior
        self.assertTrue(not tobj.hasKey('attr11'))
        self.assertEqual('', tobj.attr11())
        self.assertTrue(tobj.hasKey('attr11'))
        tobj.attr11('value11')
        self.assertEqual('value11', tobj.attr11())

        # Class attribute behavior
        self.assertTrue(not tobj.metaclass().attrs().hasKey('cattr12'))
        self.assertEqual('', tobj.cattr12())
        self.assertTrue(tobj.metaclass().attrs().hasKey('cattr12'))
        ret = tobj.cattr12('value12')
        self.assertEqual(meta.attrs(), ret)
        self.assertEqual('value12', tobj.cattr12())

    @skipUnless('TESTALL' in env, "disabled")
    def test600_metaInit(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()

        self.assertTrue(tobj.metaclass().attrs().hasKey('cattr13'))
        self.assertEqual('value from metaInit', tobj.cattr13())
        self.assertEqual('value from metaInit', tobj.metaclass().attrs()['cattr14'])

if __name__ == '__main__':
    unittest.main()
