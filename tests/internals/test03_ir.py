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

class Test_IntermediateRep(unittest.TestCase):

    def test500_method1(self):
        st = ':e :f | obj := 123'
        m = Method().compile(st)

        return

    def test990_hack(self):
        return
        st = "obj := 123"
        script = Script().compile(st)
        ssStep = script.firstStep()
        precompiled = ssStep.precompile()
        # m = Method().compile(st)

        return

if __name__ == '__main__':
    unittest.main()