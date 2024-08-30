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
from tests.TestSObj14 import TestSObj14

from os import environ as env

env['TESTALL'] = '1'

from smallscript.SObject import *
from smallscript.Closure import Script, Closure

class TDD_Package(SmallScriptTest):

    def sysModulesByName(self, moduleName):
        moduleNames = [key for key in sys.modules.keys() if moduleName in key]
        return List(moduleNames)

    @skipUnless('TESTALL' in env, "disabled")
    def test500_load(self):
        #### Based on TDD_Closure.test710_Dynamic_Creation_in_SS() from tdd_0_2/test01_tdd.py

        # Package.load() is Package.unloadSObjects().refreshSources().loadSObjects()
        # unloadSObjects() : it removes all metaclasses in the package from sys.module and package itself.
        # refreshSources(): it compiles and runs .ss files and save the output to corresponding .py files.
        # loadSObjects(): it loads all metaclass from SObjects into memory.
        # So Package.load() will always keep .ss and .py in sync, almost work like Python "import".
        # Package.setAndValidatePath(...) can be any path other than sys.path.

        tpkg = rootContext.getOrNewPackage('testpkg')
        tpkg.findPath("not_a_pkg/testpkg")
        tpkg.load()

        tobj = rootContext.newInstance('AnotherMeta').name('tobj')
        self.assertEqual('AnotherMeta', tobj.metaname())

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
