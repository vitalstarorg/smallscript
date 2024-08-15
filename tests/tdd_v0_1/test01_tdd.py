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
from tests.TestBase import SmallScriptTest, TestSObj14

from os import environ as env
env['TESTALL'] = '1'

from smallscript.SObject import *

class TDD_SObject(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_sobject(self):
        pkg = rootContext.loadPackage('tests')

        # Test SObject.copyFrom
        tobj1 = TestSObj14()            # Python way to instantiate sobject.
        tobj1.attr11('value11')
        tobj2 = TestSObj14()
        self.assertTrue(not tobj2.hasKey('attr11'))
        tobj2.copyFrom(tobj1)
        self.assertTrue(tobj2.hasKey('attr11'))
        self.assertTrue('value11', tobj2.attr11())

    @skipUnless('TESTALL' in env, "disabled")
    def test600_method(self):
        ### Access instance and class attributes and methods
        tobj1 = TestSObj14()            # Python way to instantiate sobject.
        meta1 = tobj1.metaclass()       # Access the metaclass

        self.assertTrue(meta1._getHolder('attr11').isInstanceAttribute())
        self.assertTrue(meta1._getHolder('cattr12').isClassAttribute())
        self.assertTrue(meta1._getHolder('method14').isInstanceMethod())
        self.assertTrue(meta1._getHolder('cmethod15').isClassMethod())
        self.assertTrue(meta1._getHolder('method16').isInstanceMethod())
        self.assertTrue(meta1._getHolder('cmethod17').isClassMethod())

        res = tobj1.method14(2,3)       # accessing instance method method14().
        self.assertEqual(5, res)
        res = tobj1.cmethod15(2,3)      # accessing class method cmethod15().
        self.assertEqual(6, res)
        tobj1.cattr12('200')            # accessing class attribute catt12.
        res = tobj1.cmethod17(2,3)      # accessing class method that accesses cattr12
        self.assertEqual(206, res)
        tobj1.attr11('100')             # set an instance attribute attr11.
        res = tobj1.method16(2,3)       # accessing instance method that accesses attr11.
        self.assertEqual(305, res)

        ### Instantiate the same obj through name defined by ss_metas, instead of class name.
        # Same tests as above.
        tobj2 = rootContext.newInstance('TestSObj15')
        meta2 = tobj2.metaclass()
        res = tobj2.method14(2, 3)
        self.assertEqual(5, res)
        res = tobj2.cmethod15(2, 3)
        self.assertEqual(6, res)
        tobj2.cattr12('200')
        res = tobj2.cmethod17(2, 3)
        self.assertEqual(206, res)
        tobj2.attr11('100')
        res = tobj2.method16(2, 3)
        self.assertEqual(305, res)

        ### Access class attributes using Python
        res = tobj1.attr11()
        self.assertEqual('100', res)            # Instance attribute attr11() is '100'
        res = TestSObj14.attr11()               # Class can't access instance attribute
        self.assertEqual(nil, res)
        res = TestSObj14.attr11('value11')      # Class can't set instance attribute
        self.assertEqual(nil, res)

        res = tobj1.cattr12()
        self.assertEqual('200', res)            # Class attribute cattr12 is '200'
        res = TestSObj14.cattr12('value12_')    # Set value to class attribute cattr12()
        self.assertEqual(meta1.attrs(), res)    # Class attribute map is returned for set operation
        res = TestSObj14.cattr12()              # Access class attribute cattr12
        self.assertEqual('value12_', res)
