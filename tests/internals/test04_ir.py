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

class Test_IntermediateRep(SmallScriptTest):
    def test600_method1(self):
        return
        st = ':e :f | |a b| obj := 123'
        m = Method().compile(st)
        pkg = root.loadPackage('tests.internals')
        pkg.importMethods()
        tobj = TestSObj4()
        tobj.metaclass().getHolder('method14').print()
        tobj.method14()

        return

    def test990_hack1(self):
        # return
        pkg = root.loadPackage('tests')
        tobj = TestSObj14()
        meta = tobj.metaclass()


    def test990_hack99(self):
        return
        st = "obj := 123"
        script = Script().compile(st)
        ssStep = script.firstStep()
        precompiled = ssStep.precompile()
        # m = Method().compile(st)
        return

if __name__ == '__main__':
    unittest.main()
