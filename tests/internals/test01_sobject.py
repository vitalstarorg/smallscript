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
from tests.TestBase import *

class Test_SObject(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        # Placeholder for now
        pass

    @skipUnless('TESTALL' in env, "disabled")
    def test100_helpers(self):
        sobj = SObject()
        classnames = sobj._ss_metas(TestSObj1)
        self.assertEqual(['TestSObj1','SObject'], classnames)
        classnames = sobj._ss_metas(TestSObj2)
        self.assertEqual(['TestSObj2','Metaclass'], classnames)
        classnames = sobj._ss_metas(SObject)
        self.assertEqual(['SObject'], classnames)
        return

    @skipUnless('TESTALL' in env, "disabled")
    def test110_errorReturn(self):
        sobj = SObject()
        sobj.undefined('Error!!!')
        ret = sobj.nothing()
        self.assertEqual('Error!!!', ret)

    @skipUnless('TESTALL' in env, "disabled")
    def test120_primitive(self):
        ### Make sure no one can set value or metaclass for primitives.
        obj = root.newInstance('String')
        obj.metaclass(nil)
        self.assertTrue(len(obj.__dict__) == 0)
        obj = root.newInstance('True_')
        obj.metaclass(nil)
        self.assertTrue(len(obj.__dict__) == 0)
        obj = root.newInstance('False_')
        obj.metaclass(nil)
        self.assertTrue(len(obj.__dict__) == 0)
        obj = root.newInstance('Map')
        obj.metaclass(nil)
        self.assertTrue(len(obj) == 0)
        self.assertTrue(len(obj.__dict__) == 0)
        obj = root.newInstance('List')
        obj.metaclass(nil)
        self.assertTrue(len(obj.__dict__) == 0)
        obj = root.newInstance('Number')
        obj.metaclass(nil)
        self.assertTrue(len(obj.__dict__) == 0)
        obj = root.newInstance('Float')
        obj.metaclass(nil)
        self.assertTrue(len(obj.__dict__) == 0)
        return

    @skipUnless('TESTALL' in env, "disabled")
    def test130_asSObj(self):
        obj = root.asSObj("abc")
        self.assertEqual('String', obj.metaname())
        obj = root.asSObj(True)
        self.assertEqual('True_', obj.metaname())
        obj = root.asSObj(False)
        self.assertEqual('False_', obj.metaname())
        obj = root.asSObj([1,2,3])
        self.assertEqual('List', obj.metaname())
        self.assertEqual([1,2,3], obj)
        obj = root.asSObj({'a':1,'b':2,'c':3})
        self.assertEqual('Map', obj.metaname())
        self.assertEqual({'a':1,'b':2,'c':3}, obj)
        obj = root.asSObj(123)
        self.assertEqual('Number', obj.metaname())
        obj = root.asSObj(0.123)
        self.assertEqual('Float', obj.metaname())
        obj = root.asSObj(None)
        self.assertEqual(nil, obj)

        obj = root.asSObj(self)     # no conversion
        self.assertTrue(obj, self)

    @skipUnless('TESTALL' in env, "disabled")
    def test510_package(self):
        ### Loading all SObject from tests
        pkg1 = root.loadPackage('tests')
        testobj1 = root.metaclassByName('TestSObj1').createEmpty()
        ret = testobj1.var1()
        self.assertEqual('', testobj1.var1())
        ret = testobj1.var1('value1')
        self.assertEqual(ret, testobj1)
        ret = testobj1.var1()
        self.assertEqual('value1', ret)
        meta1 = root.metaclassByName('TestSObj11')
        self.assertEqual(pkg1, meta1.package())

        # All SObject can print itself obj info to describe itself.
        testobj1.print(false_)

    @skipUnless('TESTALL' in env, "disabled")
    def test520_packages(self):
        # Reset the context will wipe out all packages and metaclasses and return nil.
        root.reset().loadPackage('smallscript')
        tobj1 = TestSObj1()
        self.assertTrue(tobj1.metaclass().isNil())

        ### Two ways to create SObject 1) Python standard instantiation 2) context.newInstance()
        # sobj will always use root context, and don't need @metaclass object but through @metaname lookup.
        sobj = SObject()
        context = sobj.getContext()
        self.assertEqual(root, context)   # new instance by SObject() will always use root context.
        self.assertTrue(not sobj.hasKey('metaclass'))

        # Reload the same package is a noop
        root.loadPackage('smallscript')

        # sobj1 will have @metaclass
        sobj1 = context.newInstance('SObject')
        self.assertTrue(sobj1.hasKey('metaclass'))


if __name__ == '__main__':
    unittest.main()
