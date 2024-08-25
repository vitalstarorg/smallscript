import unittest
from unittest import skip, skipUnless
from tests.TestBase import SmallScriptTest

from os import environ as env
env['TESTALL'] = '1'

from smallscript.SObject import *
from smallscript.Closure import Script, Method
from smallscript.Step import *
from tests.TestBase import SmallScriptTest, TestSObj14, DebugMethod

class Test_Interpreter2(SmallScriptTest):
    @classmethod
    def setUpClass(cls):
        pkg = rootContext.getOrNewPackage('Test_Interpreter2').importSingleSObject(DebugMethod)

    @skipUnless('TESTALL' in env, "disabled")
    def test100_closure(self):
        scope = rootContext.createScope()
        ss = "obj2 := 222; obj1 := 111; obj3 := 333"
        method = Method().interpret(ss)
