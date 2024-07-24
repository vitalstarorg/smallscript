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

class TestSObj1(SObject):
    var1 = Holder().name('var1').type('String')

class TestSObj2(Metaclass):
    ss_metas = "TestSObj2, Metaclass"
    pass

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
    def test510_package(self):
        ### Loading all SObject from tests
        pkg1 = root.loadPackage('tests.internals')
        testobj1 = root.metaclassByName('TestSObj1').createEmpty()
        ret = testobj1.var1()
        self.assertEqual('', testobj1.var1())
        ret = testobj1.var1('value1')
        self.assertEqual(ret, testobj1)
        ret = testobj1.var1()
        self.assertEqual('value1', ret)
        meta1 = root.metaclassByName('TestSObj1')
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

    # def test990_hack1(self):
    #     # placeholder for hacking
    #     return

if __name__ == '__main__':
    unittest.main()
