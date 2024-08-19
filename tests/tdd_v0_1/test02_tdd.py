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

class TDD_Interpreter(SmallScriptTest):
    @skipUnless('TESTALL' in env, "disabled")
    def test500_smallscript(self):
        pass
        ### Extend TDD_SObject.test690_context_package from tdd_v0_0/test01_tdd.py
        ### Create a new package and metaclass  with method dynamically without existing Python class.

    @skipUnless('TESTALL' in env, "disabled")
    def test500_primitives(self):
        #### Primitive: parser and run in interpreter.
        ss = "123"; expect = 123
        method = Method().interpret(ss); res = method()
        self.assertEqual(expect, res)
        ss = "'123'"; expect = '123'
        self.assertEqual(expect, Method().interpret(ss)())
        ss = "true"; expect = true_
        self.assertEqual(expect, Method().interpret(ss)())
        ss = "false"; expect = false_
        self.assertEqual(expect, Method().interpret(ss)())
        ss = "nil"; expect = nil
        self.assertEqual(expect, Method().interpret(ss)())
        ss = "context"; expect = rootContext
        context = Method().interpret(ss)()
        self.assertEqual(expect, context)
        ss = "root"; expect = rootContext
        rootScope = Method().interpret(ss)()
        self.assertEqual(expect, rootScope['context'])

    @skipUnless('TESTALL' in env, "disabled")
    def test600_smallscript(self):
        #### SmallScript basic syntax
        # Combine some test cases from TDD_Interpreter test04_interpreter.py
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100).cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = """
        :first :last |
        | tmp1 tmp2 |
        offset := 5.

        "Save the attributes"
        tmp1 := tobj attr11.
        tmp2 := tobj cattr12.

        "Assign new values"
        tobj attr11: '20'.
        tobj cattr12: 'Mr.'.

        "Greeting"
        greeting := 
            tobj cattr12 + ' ' + 
            first + ', ' +
            last + ' (age: ' +
            tobj attr11 + ')'.   

        "Restore variable"
        tobj attr11: tmp1.
        tobj cattr12: tmp2.

        "last value as return value"
        greeting
        """
        greetMethod = Method().interpret(ss)
        greet = greetMethod(scope, 'John', 'Doe')
        expect = "Mr. John, Doe (age: 20)"
        self.assertEqual(expect, greet)

        # temporary variables are saved in scope
        self.assertEqual(100, scope['tmp1'])
        self.assertEqual('200', scope['tmp2'])
        self.assertEqual(5, scope['offset'])

    @skipUnless('TESTALL' in env, "disabled")
    def test700_smallscript(self):
        #### SmallScript advance syntax
        # Combine some test cases from TDD_Interpreter test05_interpreter.py
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(20).cattr12('Mr.')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = """
        :fname :lname |
        
        "Keyword message"
        name := tobj first: fname last: lname.
        
        "Unary messages"
        age := tobj attr11 toString.
        
        "Binary message"
        fullname := tobj cattr12 + ' ' + name.

        "Cascade message"        
        greeting := fullname;
                    + ' (age: ';
                    + age + ')'
        """
        greetMethod = Method().interpret(ss)
        greet = greetMethod(scope, 'John', 'Doe')
        expect = "Mr. John, Doe (age: 20)"
        self.assertEqual(expect, greet)

    @skipUnless('TESTALL' in env, "disabled")
    def test710_smallscript(self):
        #### SmallScript block
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(20).cattr12('Mr.')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = """
        [:fname :lname |
        name := tobj first: fname last: lname.
        age := tobj attr11 toString.
        greeting := 
            tobj cattr12 + ' ' + 
            name + ' (age: ' +
            age + ')']
        """
        greetBlock = Method().interpret(ss)
        greetMethod = greetBlock()
        greet = greetMethod(scope, 'John', 'Doe')
        expect = "Mr. John, Doe (age: 20)"
        self.assertEqual(expect, greet)

    @skipUnless('TESTALL' in env, "disabled")
    def test720_smallscript(self):
        #### SmallScript Literal and Dynamic Array
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(20).cattr12('Mr.')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        ss = """
        :array |
        | fname lname |
        fname := array at: 0.
        lname := array at: 1.
        name := tobj first: fname last: lname.
        age := tobj attr11 toString.
        greeting := 
            tobj cattr12 + ' ' + 
            name + ' (age: ' +
            age + ')'
        """
        greetMethod = Method().interpret(ss)
        array = List().append('John').append('Doe')
        greet = greetMethod(scope, array)
        expect = "Mr. John, Doe (age: 20)"
        self.assertEqual(expect, greet)

        ss = """
        :array |
        | fname lname |
        fname := array at: 0.
        lname := array at: 1.
        name := tobj first: fname last: lname.
        age := tobj attr11.
        
        "Literal Array"
        title := #('Name' 'Age').
        
        "Dynamic Array"
        #{name age title}
        """
        greetMethod = Method().interpret(ss)
        array = List().append('John').append('Doe')
        greet = greetMethod(scope, array)
        expect = ["John, Doe", 20, ["Name", "Age"]]
        self.assertEqual(expect, greet)

