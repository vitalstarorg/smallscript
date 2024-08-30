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
from smallscript.Closure import Script, Closure
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14, DebugClosure

class Test_Package(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Package').importSingleSObject(DebugClosure)

    def setUp(self):
        self.pkg = rootContext.loadPackage('tests')
        self.tobj = TestSObj14().attr11(100).cattr12('200')
        self.metaclass = self.tobj.metaclass()
        self.scope = rootContext.createScope()
        self.scope['tobj'] = self.tobj

    def sysModulesByName(self, moduleName):
        moduleNames = [key for key in sys.modules.keys() if moduleName in key]
        return List(moduleNames)

    @skipUnless('TESTALL' in env, "disabled")
    def test100_smoke(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(100).cattr12('200')
        metaclass = tobj.metaclass()    # Real metaname is TestSObj15. TestSObj14 is Python name.
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        # Closure.getBody() remove decorator and method signature from method source.
        c17 = rootContext.metaclassByName('TestSObj15').holderByName('cmethod17').method()
        pysource = c17.pysource()
        self.assertTrue("@Holder" in pysource)
        self.assertTrue("def " in pysource)
        body = c17.getBody("")
        self.assertTrue("@Holder" not in body)
        self.assertTrue("def " not in body)

        source = c17.toNamedPython("    ", c17.name())

        return

    @skipUnless('TESTALL' in env, "disabled")
    def test200_findPath(self):
        # Testing findPath() and listFiles()
        self.assertTrue(self.sysModulesByName('tests').notEmpty())      # loaded
        self.assertTrue(self.sysModulesByName('internals').notEmpty())  # loaded
        self.assertTrue(self.sysModulesByName('testpkg').isEmpty())     # not loaded

        pkg = rootContext.getOrNewPackage('testpkg')
        self.assertTrue(not pkg.findPath("NoSuchPath"))           # not found
        self.assertTrue(not pkg.findPath("not_a_pkg"))            # not a package
        self.assertTrue(pkg.findPath("tests"))                    # found
        self.assertTrue(pkg.findPath("internals"))                # found
        self.assertTrue(pkg.findPath("not_a_pkg/testpkg"))        # found

        self.assertEqual(1, pkg.listFilePaths("__init*.py").len())

    @skipUnless('TESTALL' in env, "disabled")
    def test300_load(self):
        tpkg = rootContext.getOrNewPackage('testpkg')
        tpkg.findPath("not_a_pkg/testpkg")
            # Python wouldn't be able to find testpkg as it is out of PYTHONPATH unless specified.
            # Otherwise Python will help us to discover package so we can't really test Package class.
        self.assertTrue(self.sysModulesByName('testpkg').isEmpty())     # package not loaded
        tpkg.loadSObjects()
        self.assertTrue(self.sysModulesByName('testpkg').notEmpty())    # package loaded

        # Following could would run but IDE shown compilation error as testpkg was imported behind the scene.
        # from testpkg.TestObj import AnotherMeta
        # obj = AnotherMeta()

        obj = tpkg.newInstance('AnotherMeta')
        self.assertTrue(isinstance(obj, SObject))
        self.assertEqual('AnotherMeta', obj.metaname())

        tpkg.unloadSObjects()
        self.assertTrue(tpkg.notLoaded())

    @skipUnless('TESTALL' in env, "disabled")
    def test500_readSS_writePy(self):
        #### Based on TDD_Closure.test710_Dynamic_Creation_in_SS() from tdd_0_2/test01_tdd.py
        tpkg = rootContext.getOrNewPackage('testpkg')
        tpkg.findPath("not_a_pkg/testpkg")
        self.assertTrue(tpkg.path().notEmpty())         # tpkg is a validate package

        # Read and compile the class definition in ss file.
        filename = "TestObj"
        ss = tpkg.readFile(f"{filename}.ss")
        scope = rootContext.createScope().setValue('package', tpkg)
        closure = Closure().compile(ss)
        # closure.pysource().print()
        meta = closure(scope)
        # meta.toPython().print()

        # Write the Python source to python file.
        self.assertTrue(tpkg.notLoaded())               # package should have not loaded
        tpkg._deleteFile(f"{filename}.py")
        source = meta.asString()
        tpkg.writeFile(f"{filename}.py", source)

        # Load the SS package and create AnotherMeta instance defined by ss file.
        tpkg.unloadSObjects()       # unload this testpkg first
        anotherMeta = tpkg.metaclassByName('AnotherMeta')
        self.assertTrue(anotherMeta.isNil())
        tpkg.loadSObjects()
        self.assertTrue(tpkg.isLoaded())
        anotherMeta = tpkg.metaclassByName('AnotherMeta')
        self.assertTrue(anotherMeta.notNil())

        # Dynamically modify the metaclass, and rewrite the Python file.
        closure = Closure().compile("'hello'")
        anotherMeta.addMethod('method18', closure)
        anotherObj = anotherMeta()
        self.assertEqual('hello', anotherObj.method18())
        source = anotherMeta.toPython()
        tpkg.writeFile(f"{filename}.py", source)

        # Reload the SS package, without needing to compile ss file again.
        tpkg.reloadSObjects()
        anotherMeta = tpkg.metaclassByName('AnotherMeta')
        anotherObj = anotherMeta.createEmpty()
        res = anotherObj.method18()
        self.assertEqual('hello', res)

        tpkg.unloadSObjects()

    def test600_refresh(self):
        tpkg = rootContext.getOrNewPackage('testpkg')
        tpkg.findPath("not_a_pkg/testpkg")
        tpkg._touchFile("TestObj.ss")
        tpkg.refreshSources()
        return

    def test900_hack(self):
        metaclass = rootContext.metaclassByName('TestSObj15')
        metaclass.toPython()    # only SObject definitions are regconized.