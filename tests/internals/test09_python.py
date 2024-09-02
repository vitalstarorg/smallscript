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
from tests.TestBase import SmallScriptTest, DebugClosure
from tests.TestSObj14 import TestSObj14

class Test_Package(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Package').importSingleSObject(DebugClosure)

    def setUp(self):
        self.pkg = rootContext.loadPackage('tests')

    @skipUnless('TESTALL' in env, "disabled")
    def test100_smoke(self):
        tobj = TestSObj14().attr11(100).cattr12('200')
        scope = rootContext.createScope()
        scope['tobj'] = tobj

    @skipUnless('TESTALL' in env, "disabled")
    def test200_python_globals(self):
        localVar = 'This is a string'
            # Need to be set before createScope() for scope to recognize this variable.
            # Otherwise, the following test will pass intermittently.
        scope = rootContext.createScope()
        closure = Closure().compile('localVar')
        res = closure(scope)
        self.assertEqual(localVar, res)

        closure = Closure().compile("os getenv: 'SHELL'")
        res = closure(scope)
        self.assertTrue(res.notEmpty())

    @skipUnless('TESTALL' in env, "disabled")
    def test300_primitive_print(self):
        tobj = TestSObj14().attr11(100).cattr12('200')
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        closure = Closure().compile("<python: tobj attr11>")
        res = closure(scope)
        self.assertEqual(100, res)

        ss = f"<print: 'def hello:'>"
        closure = Closure().name('test').interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual("  _ = 'def hello:'", src)
        res = closure(scope)
        self.assertEqual("def hello:", res)
        closure.compile()
        res = closure(scope)
        self.assertEqual("def hello:", res)

        ss = "<print: 'isinstance(' + tobj attr11 asString + ', SObject)' >"
        closure = Closure().name('test').interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual("  _ = 'isinstance(' + scope['tobj'].attr11().asString() + ', SObject)'", src)
        res = closure(scope)
        self.assertEqual("isinstance(100, SObject)", res)
        closure.compile()
        res = closure(scope)
        self.assertEqual("isinstance(100, SObject)", res)

        ss = "<print: tobj attr11; ', str)'>"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual("  _ = scope['tobj'].attr11();', str)'", src)
        res = closure(scope)
        self.assertEqual("100;, str)", res)
        closure.compile()
        res = closure(scope)
        self.assertEqual(100, res)

    @skipUnless('TESTALL' not in env, "disabled")
    def test400_primitive_printf(self):
        pkg = rootContext.loadPackage('tests')
        scope = rootContext.createScope()
        tobj = TestSObj14().attr11(100).cattr12('200')
        scope['tobj'] = tobj

        # not Python compilable
        ss = "<printf: '{}'; 'def hello:'>"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual('  _ = def hello:', src)
        res = closure(scope)
        self.assertEqual("def hello:", res)

        # not Python compilable
        ss = "<printf: 'def hello:'>"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual('  _ = def hello:', src)
        res = closure(scope)
        self.assertEqual("def hello:", res)

        # not Python compilable
        ss = "<printf: 'isinstance(' + tobj attr11 asString + ', str)' >"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual("  _ = isinstance(' + scope['tobj'].attr11().asString() + ', str)", src)
        res = closure(scope)
        self.assertEqual("isinstance(100, str)", res)

        ss = "<printf: '\"{}\"'; 'def hello:'>"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual('  _ = "def hello:"', src)
        res = closure(scope)
        self.assertEqual("def hello:", res)
        closure.compile()
        res = closure(scope)
        self.assertEqual("def hello:", res)

        ss = "<printf: '{}{}{};'; 'isinstance('; tobj attr11 asString; ', str)'>"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual("  _ = isinstance(scope['tobj'].attr11().asString(), str);", src)
        res = closure(scope)
        self.assertEqual("isinstance(100, str);", res)
        closure.compile()
        res = closure(scope)
        self.assertEqual(true_, res)

    @skipUnless('TESTALL' not in env, "disabled")
    def test500_primitive_printf(self):
        pkg = rootContext.loadPackage('tests')
        scope = rootContext.createScope()
        tobj = TestSObj14().attr11(100).cattr12('200')
        scope['tobj'] = tobj

        ss = "<python: 'isinstance('; tobj attr11 asString; ', str)'>"
        closure = Closure().interpret(ss)
        src = closure.toPython().split("\n")[1]
        self.assertEqual("  _ = isinstance(scope['tobj'].attr11().asString(), str)", src)
        res = closure(scope)
        self.assertEqual("isinstance(100, str)", res)
        closure.compile()
        res = closure(scope)
        self.assertEqual(true_, res)