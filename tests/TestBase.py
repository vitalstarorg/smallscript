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
from smallscript.SObject import *

# WARNING: these test classes shouldn't be defined and loaded from the same test case Python file as the class definition would be load twice, causing inconsistency between the holder in the class definition and metaclass.
class TestSObj1(SObject):
    var1 = Holder().name('var1').type('String')

class TestSObj2(Metaclass):
    ss_metas = "TestSObj2, Metaclass"
    pass

class TestSObj11(SObject):
    attr11 = Holder().name('attr11').type('String')
    attr12 = Holder().name('attr12').type('Nil')
    attr13 = Holder().name('attr13').type('True_')
    attr14 = Holder().name('attr14').type('False_')

class TestSObj12(TestSObj11):
    attr21 = Holder().name('attr21').type('Number')

class TestSObj13(SObject):
    ss_metas = "TestSObj13, TestSObj11, Metaclass"
    attr31 = Holder().name('attr31').type('List')


class TestSObj14(SObject):
    ss_metas = "TestSObj15"
    attr11 = Holder().name('attr11').type('String')
    cattr12 = Holder().name('cattr12').type('String').classType()

    @Holder()
    def method14(scope, arg1, arg2):
        return arg1 + arg2

    @Holder().classType()
    def cmethod15(scope, arg1, arg2):
        return arg1 * arg2

    @Holder()
    def method16(scope, arg1, arg2):
        self = scope['self']
        cattr12 = self.cattr12().asNumber()
        attr11 = self['attr11'].asNumber()
        return cattr12 + attr11 + arg1 + arg2

    @Holder().classType()
    def cmethod17(scope, arg1, arg2):
        self = scope['self']
        ret = self['cattr12'].asNumber()
        return ret + arg1 * arg2

setUpClassDone = false_
class SmallScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global setUpClassDone
        if not setUpClassDone:
            # Global test initialization
            setUpClassDone = true_
