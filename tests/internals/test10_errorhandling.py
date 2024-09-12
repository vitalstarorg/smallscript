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

from smallscript.Closure import Script, Closure
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, DebugClosure

class Test_Compiler2(SmallScriptTest):
    #### It is essentially the same as test05_interpreter.py instead of
    # running in interpreter mode, but running the same SmallScript in compiled mode.
    # One exception is SmallScript arithmetics is different in Python.

    @classmethod
    def setUpClass(cls):
        pkg = sscontext.getOrNewPackage('Test_Compiler2').importSingleSObject(DebugClosure)

    @skipUnless('TESTALL' in env, "disabled")
    def test100_compile1(self):
        ss = "self wte wpe lnorm1: 0 | attn: 0 | sum lnorm2: 0 | ffn: 0 | sum x"
        closure = DebugClosure().interpret(ss)
        self.assertTrue(closure.isNil())
        closure = DebugClosure().compile(ss)
        self.assertTrue(closure.isNil())
