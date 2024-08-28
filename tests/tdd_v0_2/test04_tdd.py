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
from smallscript.Closure import Script, Method


class TDD_Package(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test100_smoke(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()     # Real metaname is TestSObj15. TestSObj14 is Python name.
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        # Method.getBody() remove decorator and method signature from method source.
        c17 = rootContext.metaclassByName('TestSObj15').holderByName('cmethod17').method()
        pysource = c17.pysource()
        self.assertTrue("@Holder" in pysource)
        self.assertTrue("def " in pysource)
        body = c17.getBody()
        self.assertTrue("@Holder" not in body)
        self.assertTrue("def " not in body)

        source = c17.toNamedPython(c17.ssSignature())
        return

    @skipUnless('TESTALL' in env, "disabled")
    def test500_smoke(self):
        #### Based on TDD_Method.test710_Dynamic_Creation_in_SS() from tdd_0_2/test01_tdd.py
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = """
        // Create metaclass
        meta := scope getValue: 'context' 
                | getOrNewPackage: 'tmppkg'
                    | createMetaclass: #AnotherMeta
                        | parentNames: #(#SObject)

                        // Create two instance attributes and one class attribute.
                        | addAttr: #attr11 type: #String
                        | addAttr: #attr12 type: #List
                        | addAttr: #cattr12 type: #String classType: true

                        // Create two instance methods and two class methods.
                        | addMethod: #method14 method: [:m14 :arg2 | m14 + arg2]
                        | addMethod: #cmethod15 method: [:m15 :arg2 | m15 * arg2] classType: true
                        | addMethod: #method16 method: [:m16 :arg2 | self cattr12 asNumber + self attr11 asNumber + m16 + arg2]
                        | addMethod: #cmethod17 method: [:m17 :arg2 | m17 * arg2 + self cattr12 asNumber] classType: true
        """
        scope = rootContext.createScope()
        method = Method().compile(ss)
        # method.pysource().print()
        meta = method(scope)

        meta.toPython().print()

        m17 = meta.holderByName("cmethod17").method()
        m17.pysource().print()

        c17 = rootContext.metaclassByName('TestSObj15').holderByName('cmethod17').method()

        return