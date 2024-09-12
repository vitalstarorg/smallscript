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

class TDD_PythonExt(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_primitive_LHS(self):
        pkg = sscontext.loadPackage('tests')
        scope = sscontext.createScope()
        tobj = TestSObj14().attr11(100).cattr12('200')
        scope.locals()['tobj'] = tobj

        # Using primitive to generate any python code
        ss = "a := <python: 'scope[\"tobj\"]'>"
        closure = Closure().compile(ss)
        res = closure(scope)
        self.assertEqual(tobj, scope['a'])

        # Using primitive to generate any python code on the LHS.
        ss = "<python: 'scope[\"tobj\"]'> := 123"
        closure = Closure().compile(ss)
        res = closure(scope)
        self.assertEqual(123, scope['tobj'])

    @skipUnless('TESTALL' in env, "disabled")
    def test200_dot_notation(self):
        scope = sscontext.createScope()

        sspkg = sscontext.getOrNewPackage('smallscript')
        ss = "sscontext.packages.smallscript"
        closure = Closure().compile(ss)
        res = closure(scope)
        self.assertEqual(sspkg, res)

        ss = "os.environ.LOG_LEVEL := 'DEBUG'"
        closure = Closure().compile(ss)
        res = closure(scope)
        self.assertEqual('DEBUG', os.environ['LOG_LEVEL'])

        ss = "loglevel := os.environ.LOG_LEVEL"
        closure = Closure().compile(ss)
        res = closure(scope)
        self.assertEqual(os.environ['LOG_LEVEL'], res)
