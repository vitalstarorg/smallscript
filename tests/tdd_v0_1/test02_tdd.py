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
from tests.TestBase import SmallScriptTest, TestSObj14

from os import environ as env
env['TESTALL'] = '1'

from smallscript.SObject import *
from smallscript.Closure import Script

class TDD(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_antlr(self):
        #### Simple case
        st = "obj := 123"
        script = Script().parse(st)
        self.assertTrue(script.noError())

        #### AST graph in form of text
        res = script.toStringTree()
        self.assertTrue('obj' in res)
        self.assertTrue('123' in res)

        #### AST graph of the syntax can be shown on nbs/antlr.ipynb
        dot = script.dotGraph()
        dot_graph = dot.source.split('\n')
        self.assertEqual('digraph G {', dot_graph[0])

        #### Error case
        st = "obj1 'abc'"
        script.parse(st)
        self.assertTrue(script.hasError())
        errmsg = ("Syntax error at line 1:5: extraneous input ''abc'' expecting <EOF>\n"
                  "obj1 'abc'\n"
                  "     ^")
        self.assertTrue(errmsg, script.prettyErrorMsg())

    @skipUnless('TESTALL' in env, "disabled")
    def test500(self):
        return