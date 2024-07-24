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
    attr11 = Holder().name('attr11').type('String')
    attr12 = Holder().name('attr12').type('Nil')
    attr13 = Holder().name('attr13').type('True_')
    attr14 = Holder().name('attr14').type('False_')

class TestSObj2(TestSObj1):
    attr21 = Holder().name('attr21').type('Number')

class TestSObj3(SObject):
    ss_metas = "TestSObj3, TestSObj1, Metaclass"
    attr31 = Holder().name('attr31').type('List')

class TDD(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_getter_setter(self):
        ### SObject uses builder pattern for its attributes.
        # sobj.name() is the getter return its @name.
        # sobj.name('sobj') is the setter and return sobj itself.
        # SObject also has getValue() and setValue()
        # SObject attribute is created on-demand and can be removed at runtime.
        sobj = SObject()
        self.assertEqual('a SObject', sobj.name())  # default name
        self.assertTrue(not sobj.hasKey('name'))    # @name not yet exists
        ret = sobj.name('sobj')                     # setter always returns obj
        self.assertTrue(sobj.hasKey('name'))        # @name exists
        self.assertEqual('sobj', sobj.name())       # its value is 'sobj'
        self.assertEqual(sobj, ret)                 # return sobj as to follow the builder pattern
        self.assertEqual('sobj', sobj.getValue('name'))  # alternative way to access attribute
        sobj.delValue('name')                       # remove @name
        self.assertTrue(not sobj.hasKey('name'))    # @name removed

        # SObject structure is described by its metaclass which can be defined by Holder through Python class variables or construct programmatically. The use of Python class variable is an option to provide hint to IDE.
        sobjmeta = sobj.metaclass()
        self.assertEqual('SObject', sobj.metaname())
        self.assertEqual('SObject', sobjmeta.name())
        self.assertTrue(sobjmeta.holders().len() > 2)
        self.assertTrue(sobjmeta.holders().keys().includes(['name', 'metaname']))

        # Besides holder defined the attributes, SObject will still try to access other value inside sobject.
        self.assertTrue(not sobj.hasKey('newAttr'))     # newAttr not there
        sobj.setValue('newAttr', 'newValue')            # set some value
        ret = sobj.newAttr()                            # newAttr works like a getter method.
        self.assertEqual('newValue', ret)               # retrieves the same value
        sobj.delValue('newAttr')                        # remove @newAttr from sobj
        self.assertTrue(not sobj.hasKey('newAttr'))     # @newAttr removed

        # Changing @metaname will change sobj metaclass.
        self.assertTrue(not sobj.hasKey('package'))     # sobj doesn't have @package attribute
        sobj.metaname('Metaclass')                      # change its @metaname to Metaclass
        self.assertTrue(not sobj.hasKey('package'))     # @package not exist yet
        ret = sobj.package()                            # but @package available from Metaclass metaclass
        self.assertEqual('Package', ret.metaname())     # empty object is returned by default
        self.assertTrue(sobj.hasKey('package'))         # default value is saved

    @skipUnless('TESTALL' in env, "disabled")
    def test510_context_package(self):
        ### Context holds on to all packages, Package holds on to all metaclasses. It forms a closed system within a runtime.
        # @root is the default context, and root.loadPackage('smallscript') by default i.e. smallscript metaclasses are loaded.

        # Load the package with its metaclasses
        pkg = root.loadPackage('tests.tdd_v0_0')
        tobj1 = TestSObj1()
        meta1 = tobj1.metaclass()
        self.assertTrue(meta1.notNil())

        # tobj1 is an empty object and has these unpopulated attributes defined.
        self.assertTrue(meta1.holders().keys().includes(['attr11', 'attr12', 'attr13', 'attr14']))
        self.assertEqual(List(), tobj1.keys())

        # @attr11 is created by default using holder @type hint.
        self.assertTrue(not tobj1.hasKey('attr11'))
        self.assertEqual('', tobj1.attr11())
        self.assertTrue(tobj1.hasKey('attr11'))
        self.assertTrue(not tobj1.hasKey('attr12'))

        # Using 'Nil', 'True_' & 'False_' hint will not have default value stored unless value is set explicitly. Useful for occassional used attribute e.g. @mutable.
        self.assertEqual(nil, tobj1.attr12())
        self.assertTrue(not tobj1.hasKey('attr12'))
        tobj1.attr12('value2')
        self.assertEqual('value2', tobj1.attr12())

        self.assertEqual(true_, tobj1.attr13())
        self.assertTrue(not tobj1.hasKey('attr13'))
        tobj1.attr13(false_)
        self.assertTrue(tobj1.hasKey('attr13'))
        self.assertEqual(false_, tobj1.attr13())

        self.assertEqual(false_, tobj1.attr14())
        self.assertTrue(not tobj1.hasKey('attr14'))
        tobj1.attr14(false_)
        self.assertTrue(tobj1.hasKey('attr14'))
        self.assertEqual(false_, tobj1.attr14())

        # Now tobj1 has these attributes populated.
        self.assertEqual(['attr11', 'attr12', 'attr13', 'attr14'], tobj1.keys())

        # Find TestSObj1 metaclass by name and create a new instance by metaclass or by context.
        meta2 = root.metaclassByName('TestSObj1')
        self.assertEqual(meta1, meta2)                  # same metaclass
        self.assertEqual('TestSObj1', meta2.name())
        tobj2 = meta2.createEmpty()                     # create a new instance by metaclass
        self.assertTrue(tobj2.notNil())
        tobj2 = root.newInstance('TestSObj1')           # create a new instance by context
        self.assertTrue(tobj2.notNil())

        # SObject supports multiple inheritance, working like traits.
        self.assertEqual(root, tobj2.getContext())      # tobj2 context is root
        self.assertEqual(pkg, tobj2.getPackage())       # tobj2 has the same package
        metaSObj = root.metaclassByName('SObject')
        parents = tobj2.inheritedMetas()
        self.assertEqual([meta2, metaSObj]
                         , parents.values())            # show the class inheritance.

        # tobj2 works the same as tobj1
        self.assertEqual(nil, tobj2.attr12())
        self.assertTrue(not tobj2.hasKey('attr12'))
        ret = tobj2.attr12('value2')
        self.assertEqual('value2', tobj2.attr12())
        self.assertEqual(ret, tobj2)

        ### true_, false_, nil and root are singletons that shared with all contexts.
        aNil = Nil()
        self.assertEqual(nil, aNil)
        aTrue = True_()
        self.assertEqual(true_, aTrue)
        aFalse = False_()
        self.assertEqual(false_, aFalse)

    @skipUnless('TESTALL' in env, "disabled")
    def test610_inheritance(self):
        ### Testing inheritance and sobj.getSuper()
        # Inherited attributes from TestSObj1 and SObject access through sobj2
        sobj2 = TestSObj2().name('tobj2')
        self.assertEqual('TestSObj2', sobj2.metaname())
        self.assertEqual('TestSObj2', sobj2.metaclass().name())
        ret = sobj2.attr21()
        self.assertEqual(0, ret)
        sobj2.attr11('value11').attr21(21)
        self.assertEqual('value11', sobj2.attr11())
        self.assertEqual(21, sobj2.attr21())
        self.assertEqual(['name', 'attr21', 'attr11'], sobj2.keys())

        # sobj2 should have these inherited attributes
        holders = sobj2.inheritedHolders()
        self.assertTrue(holders.keys().includes(['attr21', 'attr11', 'attr12', 'attr13', 'attr14', 'name', 'metaname']))

        # sobj2 could find its parent metaclasses.
        metaTestSObj1 = sobj2.nearestParent()
        self.assertEqual('TestSObj1', metaTestSObj1.name())
        metaSObj = sobj2.nearestParent('SObject')
        self.assertEqual('SObject', metaSObj.name())
        parent = sobj2.nearestParent('Metaclass')
        self.assertEqual(nil, parent)
        metas = sobj2.inheritedMetas().keys()
        self.assertEqual(['TestSObj2', 'TestSObj1', 'SObject'], metas)

        # super masquerade as sobj2 as its parent meta Test1SObj, working as if parent class.
        super = sobj2.getSuper()
        self.assertEqual('tobj2', super.name())
        self.assertEqual('TestSObj1', super.metaname())
        holders = super.inheritedHolders()
        self.assertTrue(holders.keys().includes(['attr11', 'attr12', 'attr13', 'attr14', 'name', 'metaname']))
        self.assertEqual('value11', super.attr11())
        self.assertEqual(nil, super.attr12())
        self.assertEqual(21, super.attr21())    # throu' SObject.__getattr__, using map lookup, not holder
        metas = super.inheritedMetas().keys()
        self.assertEqual(['TestSObj1', 'SObject'], metas)

    @skipUnless('TESTALL' in env, "disabled")
    def test620_inheritance(self):
        ### Testing multiple inheritance and sobj.getSuper()
        sobj3 = root.newInstance('TestSObj3').name('sobj3')
        self.assertEqual('TestSObj3', sobj3.metaname())
        self.assertEqual('TestSObj3', sobj3.metaclass().name())

        ret = sobj3.attr31()
        self.assertEqual([], ret)
        sobj3.attr11('value11').attr31(['hello', 'world'])
        self.assertEqual('value11', sobj3.attr11())
        self.assertEqual(['hello', 'world'], sobj3.attr31())
        self.assertEqual(['metaclass', 'name', 'attr31', 'attr11'], sobj3.keys())

        # sobj3 should have these inherited attributes
        holders = sobj3.inheritedHolders()
        self.assertTrue(holders.keys().includes(
            ['attr31', 'attr11', 'attr12', 'attr13', 'attr14', 'name', 'metaname', 'context', 'package', 'holders']))

        # sobj2 could find its parent metaclasses.
        metaTestSObj1 = sobj3.nearestParent()
        self.assertEqual('TestSObj1', metaTestSObj1.name())
        metaSObj = sobj3.nearestParent('SObject')
        self.assertEqual('SObject', metaSObj.name())
        metaMeta = sobj3.nearestParent('Metaclass')
        self.assertEqual('Metaclass', metaMeta.name())
        metas = sobj3.inheritedMetas().keys()
        self.assertEqual(['TestSObj3', 'TestSObj1', 'SObject', 'Metaclass'], metas)

        # super masquerade as sobj3 as its parent meta Test1SObj, working as if parent class.
        super = sobj3.getSuper()        # nearest is Test1SObj
        self.assertEqual('sobj3', super.name())
        self.assertEqual('TestSObj1', super.metaname())
        holders = super.inheritedHolders()
        self.assertTrue(holders.keys().includes(['attr11', 'attr12', 'attr13', 'attr14', 'name', 'metaname']))
        self.assertEqual('value11', super.attr11())
        self.assertEqual(nil, super.attr12())
        self.assertEqual(['hello', 'world'], super.attr31())    # throu' SObject.__getattr__, using map lookup, not holder
        metas = super.inheritedMetas().keys()
        self.assertEqual(['TestSObj1', 'SObject'], metas)

        # super masquerade as sobj3 as its parent meta Metaclass, working as if parent class.
        super = sobj3.getSuper('Metaclass')
        self.assertEqual('sobj3', super.name())
        self.assertEqual('Metaclass', super.metaname())
        holders = super.inheritedHolders()
        self.assertTrue(holders.keys().includes(['context', 'package', 'factory', 'holders', 'name', 'metaname']))
        self.assertEqual('value11', super.attr11())
        self.assertTrue(not super.hasKey('attr12'))
        self.assertEqual(['hello', 'world'], super.attr31())    # throu' SObject.__getattr__, using map lookup, not holder
        metas = super.inheritedMetas().keys()
        self.assertEqual(['Metaclass', 'SObject'], metas)
        return

    @skipUnless('TESTALL' in env, "disabled")
    def test690_context_package(self):
        ### Create a new package and metaclass dynamically without existing Python class.
        # Create a new context, separated from root. So this separated context would work independently in the same runtime.
        # Create a new test context and package
        cxt = Context().name('test01_tdd')
        cxt.loadPackage('smallscript')      # need to load this first.
        pkg = cxt.newPackage('tmppkg')      # create a temporary package

        # Create new metaclass with two attributes.
        newMeta = pkg.createMetaclass('NewMeta')
        newMeta.parentNames(['Metaclass'])
        newMeta.factory(SObject())
        holders = newMeta.holders()
        holders['attr11'] = Holder().name('attr11').type('String')
        holders['attr12'] = Holder().name('attr12').type('List')

        # Create a new instance. Real obj4 type is Python SObject but behaves like a new type.
        obj4 = cxt.newInstance('NewMeta').name('obj4')
        self.assertEqual(SObject, type(obj4))
        self.assertEqual('NewMeta', obj4.metaname())

        # obj4 works like a normal sobj created from Python class
        self.assertEqual('obj4', obj4.name())
        self.assertEqual('', obj4.attr11())
        obj4.attr11('hello')
        self.assertEqual('hello', obj4.attr11())
        self.assertEqual([], obj4.attr12())
        obj4.attr12().append('world').append('!')
        self.assertEqual(['world','!'], obj4.attr12())

        # Shows the inheritance hierarchy
        parents = obj4.inheritedMetas()
        metaSObj = cxt.metaclassByName('SObject')
        metaMeta = cxt.metaclassByName('Metaclass')
        self.assertEqual([newMeta, metaMeta, metaSObj], parents.values())

        # Shows that SObject, Metaclass are separated from root.
        meta = root.metaclassByName('SObject')
        self.assertEqual(metaSObj.name(), meta.name())
        self.assertNotEqual(metaSObj, meta)
        meta = root.metaclassByName('Metaclass')
        self.assertEqual(metaMeta.name(), meta.name())
        self.assertNotEqual(metaMeta, meta)
        meta = root.metaclassByName('NewMeta')
        self.assertTrue(meta.isNil())

if __name__ == '__main__':
    unittest.main()
