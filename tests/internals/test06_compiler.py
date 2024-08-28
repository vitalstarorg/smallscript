import unittest
from unittest import skip, skipUnless
from tests.TestBase import SmallScriptTest

from os import environ as env
env['TESTALL'] = '1'

from smallscript.SObject import *
from smallscript.Closure import Script, Closure
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14, DebugClosure

class Test_Compiler1(SmallScriptTest):
    #### Besides test100_smoke, rest of it essentially the same as test04_interpreter.py instead of
    # running in interpreter mode, but running the same SmallScript in compiled mode.

    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Interpreter2').importSingleSObject(DebugClosure)

    @skipUnless('TESTALL' in env, "disabled")
    def test100_smoke(self):
        # A series of simple smoke tests to help the development.
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14()
        tobj.attr11(100)
        tobj.cattr12('200')
        metaclass = tobj.metaclass()
        scope = rootContext.createScope()
        scope['tobj'] = tobj

        # Testing basic code gen for closure require only visitClosure and visitNumber.
        ss = "321"
        closure = Closure().name('testfunc').interpret(ss).toPython()
        res = closure.pysource()
        self.assertEqual("def testfunc(scope):\n  _ = 321\n  return _", res)
        res = closure(scope)
        self.assertEqual(321, res)

        ss = ":param1 :param2| |a b| 123"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope, 12,34)
        self.assertEqual(123, res)

        # Testing visitString()
        ss = "'abc'"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure()
        self.assertEqual('abc', res)

        # Testing parameter passing
        ss = ":param1| param1"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(222)
        self.assertEqual(222, res)

        # Testing assignment and the use of scope for parameters and temp variables.
        ss = ":param1| | a | a := param1; a"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope, 333)
        self.assertEqual(333, res)
        self.assertEqual(333, scope['a'])
        self.assertEqual(333, scope['param1'])

        # Testing unary message
        ss = "tobj attr11"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(100, res)

        # Testing binary message
        ss = ":param1| param1 + 13"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope, 123)
        self.assertEqual(136, res)

        # Testing keyword message
        ss = "tobj attr11: 444"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(444, tobj.attr11())

        ss = "tobj method14: 222 add: 333"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(555, res)

        # Testing subexpression
        ss = "tobj attr11: (22 + 33); tobj attr11"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(55, res)

        # Testing chain
        ss = "tobj | attr11: 7"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(tobj, res)

        ss = "tobj | attr11: 7 | attr11"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(7, res)

        # Testing block
        ss = "[:param1 | param1]"
        block = Closure().name('test').interpret(ss).toPython().compile()
        closure = block(scope)
        res = closure(321)
        self.assertEqual(321, res)

    @skipUnless('TESTALL' in env, "disabled")
    def test520_param_access(self):
        scope = rootContext.createScope()
        ss = ":param1 | param1"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope, 'aString')
        self.assertEqual('aString', res)
        self.assertTrue(scope.hasKey('param1'))
        res = closure(scope, 123)
        self.assertEqual(123, res)

        scope = rootContext.createScope()
        ss = ":param1 :param2| param2"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope, nil, nil)
        self.assertEqual(nil, res)
        self.assertTrue(scope.hasKey('param1'))
        self.assertTrue(scope.hasKey('param2'))

        res = closure(scope, 'str1', 'str2')
        self.assertEqual('str2', res)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))

    @skipUnless('TESTALL' in env, "disabled")
    def test530_assignment(self):
        scope = rootContext.createScope()
        ss = "obj1 := 123"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(123, res)
        self.assertTrue(scope.hasKey('obj1'))
        self.assertEqual(123, scope.getValue('obj1'))

        ss = "obj1 := 'str1'"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual('str1', res)

        scope = rootContext.createScope()
        ss = "_ := obj1 := 123"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(123, res)
        self.assertEqual(123, scope.getValue('obj1'))
        self.assertEqual(123, scope.getValue('_'))

        scope = rootContext.createScope()
        ss = ":param1 :param2| |tmp1| tmp1 := param2"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope, 'str1', 'str2')
        self.assertEqual('str2', res)
        self.assertTrue('str1', scope.getValue('param1'))
        self.assertTrue('str2', scope.getValue('param2'))
        self.assertTrue('str2', scope.getValue('tmp1'))

        res = closure(scope, 'str1', 123)
        self.assertEqual(123, res)
        self.assertTrue(123, scope.getValue('param2'))
        self.assertTrue(123, scope.getValue('tmp1'))

    @skipUnless('TESTALL' in env, "disabled")
    def test600_sobject(self):
        pkg = rootContext.loadPackage('tests')
        tobj = TestSObj14().attr11(123)
        tobj.cattr12('cvalue12')

        scope = rootContext.createScope()
        scope.addObj(tobj)
        ss = "attr11"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(123, res)
        ss = "cattr12"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual('cvalue12', res)

        ss = "attr11 := 321"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual(321, tobj.attr11())
        ss = "cattr12 := 'anotherValue'"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual('anotherValue', tobj.cattr12())

    @skipUnless('TESTALL' in env, "disabled")
    def test700_scope(self):
        # SObject protocol of Scope
        scope = Scope()
        self.assertEqual('', scope.name())
        self.assertEqual('a Scope', scope.describe())
        res = scope.name('scope')
        self.assertEqual('scope', scope.name())
        self.assertEqual(scope, res)

        # Get & set to scope will not affect SObject states e.g. name, metaname, etc.
        self.assertTrue(not scope.hasKey('name'))
        scope.setValue('name', 'sobj')
        self.assertTrue(scope.hasKey('name'))
        self.assertEqual('sobj', scope.getValue('name'))
        self.assertEqual('scope', scope.name())
        scope.delValue('name')
        self.assertTrue(not scope.hasKey('name'))
        self.assertEqual('scope', scope.name())

        scope['attr11'] = 'value11'
        scope['attr12'] = 'value12'
        scope2 = Scope().name('scope2')
        scope2['attr21'] = 'value21'
        scope.addScope(scope2)
        tobj = TestSObj14()
        tobj.attr11('tobj12')
        scope.addObj(tobj)
        res = scope.info()  # smoke test, ignore output
        # res.print()

        scope = rootContext.createScope()
        root = scope['root']
        root['global1'] = nil
        ss = "global1 := 'global value'"
        closure = Closure().interpret(ss).toPython().compile()
        res = closure(scope)
        self.assertEqual('global value', scope['global1'])

if __name__ == '__main__':
    unittest.main()
