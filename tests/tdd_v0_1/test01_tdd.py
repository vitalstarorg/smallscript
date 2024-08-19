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
from smallscript.Closure import Method

class TDD_Method(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_Instance_Class(self):
        ### Access instance and class attributes and methods
        tobj1 = TestSObj14()            # Python way to instantiate sobject.
        meta1 = tobj1.metaclass()       # Access the metaclass

        self.assertTrue(meta1._getHolder('attr11').isInstanceAttribute())
        self.assertTrue(meta1._getHolder('cattr12').isClassAttribute())
        self.assertTrue(meta1._getHolder('method14').isInstanceMethod())
        self.assertTrue(meta1._getHolder('cmethod15').isClassMethod())
        self.assertTrue(meta1._getHolder('method16').isInstanceMethod())
        self.assertTrue(meta1._getHolder('cmethod17').isClassMethod())

        self.assertEqual('TestSObj15', meta1.name())

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

    @skipUnless('TESTALL' not in env, "disabled")
    def test600_Dynamic_Invocation(self):
        #### SObject attributes protocol, not through Python
        # Same as Test_Method.test500_method(), but totally SObject protocol.
        pkg = rootContext.loadPackage('tests')
        meta = rootContext.metaclassByName('TestSObj15')
        tobj = SObject().metaclass(meta)

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

        #### SObject methods protocol, not through Python
        res = tobj.method14(2,3)       # accessing instance method method14().
        self.assertEqual(5, res)
        res = tobj.cmethod15(2,3)      # accessing class method cmethod15().
        self.assertEqual(6, res)
        tobj.cattr12('200')            # accessing class attribute catt12.
        res = tobj.cmethod17(2,3)      # accessing class method that accesses cattr12
        self.assertEqual(206, res)
        tobj.attr11('100')             # set an instance attribute attr11.
        res = tobj.method16(2,3)       # accessing instance method that accesses attr11.
        self.assertEqual(305, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test700_Dynamic_Creation(self):
        ### Create a new package and metaclass like TestSObj15 dynamically without using Python class.
        # Basically doing the test600_Dynamic_Invocation() above with dynamically created class
        # with attributes and methods.
        # Based on TDD_SObject.test690_context_package()

        # Create a new context, separated from root. So this separated context would work independently in the same runtime.
        # Create a new test context and package
        cxt = Context().name('v0_1_test01_tdd')
        cxt.loadPackage('smallscript')      # need to load this first.
        pkg = cxt.newPackage('tmppkg')      # create a temporary package

        # Create new metaclass with two attributes.
        newMeta = pkg.createMetaclass('NewMeta')
        newMeta.parentNames(['Metaclass'])
        newMeta.factory(SObject())
        holders = newMeta.holders()
        holders['attr11'] = Holder().name('attr11').type('String')
        holders['attr12'] = Holder().name('attr12').type('List')
        holders['cattr12'] = Holder().name('cattr12').type('String').asClassType()

        # Define instance and class method using SmallScript
        method14 = Method().interpret(":arg1 :arg2 | arg1 + arg2")
        holders['method14'] = Holder().name('method14').type('Method').method(method14)
        cmethod15 = Method().interpret(":arg1 :arg2 | arg1 * arg2")
        holders['cmethod15'] = Holder().name('cmethod15').type('Method').method(cmethod15).asClassType()
        method16 = Method().interpret(":arg1 :arg2 | self cattr12 asNumber + self attr11 asNumber + arg1 + arg2")
        holders['method16'] = Holder().name('method16').type('Method').method(method16)
        cmethod17 = Method().interpret(":arg1 :arg2 | arg1 * arg2 + self cattr12 asNumber")
        holders['cmethod17'] = Holder().name('cmethod17').type('Method').method(cmethod17)

        tobj = cxt.newInstance('NewMeta').name('tobj')
        self.assertEqual(SObject, type(tobj))
        self.assertEqual('NewMeta', tobj.metaname())

        res = tobj.method14(2,3)            # accessing instance method method14().
        self.assertEqual(5, res)
        res = tobj.cmethod15(2,3)      # accessing class method cmethod15().
        self.assertEqual(6, res)
        tobj.cattr12('200')            # accessing class attribute catt12.
        res = tobj.cmethod17(2,3)      # accessing class method that accesses cattr12
        self.assertEqual(206, res)
        tobj.attr11('100')             # set an instance attribute attr11.
        res = tobj.method16(2,3)       # accessing instance method that accesses attr11.
        self.assertEqual(305, res)