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

class LocalSObj14(SObject):
    ss_metas = "LocalSObj15"
    attr11 = Holder().name('attr11').type('String')
    sobj11 = Holder().name('sobj11').type('TestSObj11')
    cattr12 = Holder().name('cattr12').type('String').asClassType()
    cattr13 = Holder().name('cattr13').type('String').asClassType()

    @Holder().asClassType()
    def metaInit(scope):
        # self is attrs of the metaclass LocalSObj15
        self = scope['self']
        # attrs is SObject and works like Map without needing to define Holder.
        # Having Holder helps access class attribute in Python.
        ret = self.cattr13("value from metaInit")   # access through holder
        self['cattr14'] = "value from metaInit"     # don't have to defined by holder
        return self

    @Holder()
    def method14(scope, arg1, arg2):
        return arg1 + arg2

    @Holder().asClassType()
    def cmethod15(scope, arg1, arg2):
        return arg1 * arg2

    @Holder()
    def method16(scope, arg1, arg2):
        self = scope['self']
        cattr12 = self.cattr12().asNumber()
        attr11 = self['attr11'].asNumber()
        return cattr12 + attr11 + arg1 + arg2

    @Holder().asClassType()
    def cmethod17(scope, arg1, arg2):
        self = scope['self']
        ret = self['cattr12'].asNumber()
        return ret + arg1 * arg2

class Test_Method(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_method(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()

        metaName = meta.name()
        self.assertEqual('TestSObj15', metaName)

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
    def test550_metaInit(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()

        self.assertTrue(tobj.metaclass().attrs().hasKey('cattr13'))
        self.assertEqual('value from metaInit', tobj.cattr13())
        self.assertEqual('value from metaInit', tobj.metaclass().attrs()['cattr14'])

    #
    # Testing local import class
    #

    # Originate from Test_Method.test500_method() test02_method.py.
    @skipUnless('TESTALL' in env, "disabled")
    def test700_localSObj(self):
        pkg = rootContext.getOrNewPackage('test02_method').importSingleSObject(LocalSObj14)
        tobj = LocalSObj14()
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

        tobj = TestSObj14()
        meta = tobj.metaclass()

        self.assertTrue(tobj.metaclass().attrs().hasKey('cattr13'))
        self.assertEqual('value from metaInit', tobj.cattr13())
        self.assertEqual('value from metaInit', tobj.metaclass().attrs()['cattr14'])

    # Originate tdd_v0_2/test01_tdd.py.
    @skipUnless('TESTALL' in env, "disabled")
    def test720_localSObj(self):
        ### Access instance and class attributes and methods
        tobj1 = LocalSObj14()            # Python way to instantiate sobject.
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
        tobj2 = rootContext.newInstance('LocalSObj15')
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
        res = LocalSObj14.attr11()               # Class can't access instance attribute
        self.assertEqual(nil, res)
        res = LocalSObj14.attr11('value11')      # Class can't set instance attribute
        self.assertEqual(nil, res)

        res = tobj1.cattr12()
        self.assertEqual('200', res)            # Class attribute cattr12 is '200'
        res = LocalSObj14.cattr12('value12_')    # Set value to class attribute cattr12()
        self.assertEqual(meta1.attrs(), res)    # Class attribute map is returned for set operation
        res = LocalSObj14.cattr12()              # Access class attribute cattr12
        self.assertEqual('value12_', res)

    @skipUnless('TESTALL' in env, "disabled")
    def test730_signature(self):
        method = Method().interpret("arg1 + arg2")
        self.assertEqual("", method.signature())
        method.name('testMethod')
        self.assertEqual("testMethod", method.signature())

        method = Method().interpret(":arg1 | arg1 + 2")
        self.assertEqual("arg1", method.signature())
        method.name('testMethod')
        self.assertEqual("testMethod__arg1__", method.signature())

        method = Method().interpret(":arg1 :arg2 | arg1 + arg2")
        self.assertEqual("arg1__arg2__", method.signature())
        method.name('testMethod')
        self.assertEqual("testMethod__arg1__arg2__", method.signature())

if __name__ == '__main__':
    unittest.main()
