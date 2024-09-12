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

from smallscript.SObject import *
from smallscript.antlr.SmallScriptVisitor import SmallScriptVisitor

class ObjAdapter(SObject):
    "Make SObject follows Python dot notation for attribute access. Not yet supports method access."
    def object(self, object=""):   # can be either Python or SObject object
        res = self._getOrSet('object', object, 'Nil')
        if object != "":
            isSObj = true_ if isinstance(object, SObject) else false_
            self.isSObject(isSObj)
            return self
        return res

    def isSObject(self, isSObject=''): return self._getOrSet('isSObject', isSObject, true_)

    def getRef(self, attrname):
        obj = self
        parts = attrname.split('.')
        for part in parts[:-1]:
            obj = obj._getValue(part)
            if obj is nil: return nil
            obj = ObjAdapter().object(obj)
        return obj

    def getValue(self, attrname):
        last = attrname.rsplit('.',1)[-1]
        obj = self.getRef(attrname)
        if obj is nil: return nil
        res = obj._getValue(last)
        return res

    def setValue(self, attrname, value):
        last = attrname.rsplit('.',1)[-1]
        obj = self.getRef(attrname)
        if obj is nil: return nil
        res = obj._setValue(last, value)
        return res

    def _getValue(self, attrname):
        pyobj = sobj = self.object()
        if not self.isSObject():
            if hasattr(pyobj, 'get'):
                res = pyobj.get(attrname, nil)      # make it work for a dict with a default
            else:
                res = getattr(pyobj, attrname, nil) # access the pyobj attribute
            return res
        res = sobj.getValue(attrname)
        return res

    def _setValue(self, attrname, value):
        pyobj = sobj = self.object()
        if not self.isSObject():
            if hasattr(pyobj, '__setitem__'):
                pyobj[attrname] = value             # make it work for a dict.
            else:
                res = setattr(pyobj, attrname, value)
            return pyobj
        res = sobj.setValue(attrname, value)
        return res

    def __getattr__(self, attrname):
        """Intercept attributes and methods access not defined by holders."""
        return self.getValue(attrname)

    def __setattr__(self, attrname, value):
        """Intercept attributes and methods access not defined by holders."""
        return self.setValue(attrname, value)

class PyGlobals(Scope):
    "Interfacing scope on Python global dictionary which keeps track of global namespace at realtime."

    # Disable the following scope protocol.
    def scopes(self, scopes=''): return self if scopes != '' else List()
    def objs(self, objs=''):  return self if objs != '' else List()
    def parent(self, parent=''):  return self if parent != '' else nil
    def setSelf(self, obj): return self
    def addScope(self, scope): return self

    # Redefine these protocols.
    def keys(self): return self.locals().keys()
    def hasKey(self, attname): return attname in self.locals()

    def delValue(self, attname):
        if self.hasKey(attname):
            del self.locals()[attname]
        return self

    def getValue(self, attname, default=nil):
        return self.locals()[attname] if self.hasKey(attname) else default

    def setValue(self, attname, value): self.locals()[attname] = value; return self
    def lookup(self, key, default=nil): return self if self.hasKey(key) else default

class RuleContextVisitor(SmallScriptVisitor):
    def visitCommon(self, cxt): return cxt.getText()
    def visitSmallscript(self, cxt): return self.visitCommon(cxt)
    def visitClosure(self, cxt): return self.visitCommon(cxt)
    def visitTemps(self, cxt): return self.visitCommon(cxt)
    def visitTempvar(self, cxt): return self.visitCommon(cxt)
    def visitBlkparamlst(self, cxt): return self.visitCommon(cxt)
    def visitBlkparam(self, cxt): return self.visitCommon(cxt)
    def visitExpr(self, cxt): return self.visitCommon(cxt)
    def visitExprs(self, cxt): return self.visitCommon(cxt)
    def visitUnaryhead(self, cxt): return self.visitCommon(cxt)
    def visitUnarytail(self, cxt): return self.visitCommon(cxt)
    def visitUnarymsg(self, cxt): return self.visitCommon(cxt)
    def visitUnaryop(self, cxt): return self.visitCommon(cxt)
    def visitOperand(self, cxt): return self.visitCommon(cxt)
    def visitKwhead(self, cxt): return self.visitCommon(cxt)
    def visitKwmsg(self, cxt): return self.visitCommon(cxt)
    def visitKwpair(self, cxt): return self.visitCommon(cxt)
    def visitBinhead(self, cxt): return self.visitCommon(cxt)
    def visitBintail(self, cxt): return self.visitCommon(cxt)
    def visitBinmsg(self, cxt): return self.visitCommon(cxt)
    def visitBinop(self, cxt): return self.visitCommon(cxt)
    def visitChain(self, cxt): return self.visitCommon(cxt)
    def visitPtfin(self, cxt): return self.visitCommon(cxt)
    def visitMsg(self, cxt): return self.visitCommon(cxt)
    def visitSubexpr(self, cxt): return self.visitCommon(cxt)
    def visitChar(self, cxt): return self.visitCommon(cxt)
    def visitBaresym(self, cxt): return self.visitCommon(cxt)
    def visitPrimitive(self, cxt): return self.visitCommon(cxt)
    def visitAssign(self, cxt): return self.visitCommon(cxt)
    def visitVar(self, cxt): return self.visitCommon(cxt)
    def visitRef(self, cxt): return self.visitCommon(cxt)
    def visitString(self, cxt): return self.visitCommon(cxt)
    def visitWs(self, cxt): return self.visitCommon(cxt)
    def visitTerminal(self, tnode): return self.visitCommon(tnode)
    def visitNum(self, cxt): return self.visitCommon(cxt)
    def visitSsFloat(self, cxt): return self.visitCommon(cxt)
    def visitSsHex(self, cxt): return self.visitCommon(cxt)
    def visitSsInt(self, cxt):return self.visitCommon(cxt)
    def visitExprlst(self, cxt): return self.visitCommon(cxt)
    def visitBlk(self, cxt): return self.visitCommon(cxt)
    def visitPtkey(self, cxt): return self.visitCommon(cxt)
    def visitLiteral(self, cxt): return self.visitCommon(cxt)
    def visitRtlit(self, cxt): return self.visitCommon(cxt)
    def visitDyndict(self, cxt): return self.visitCommon(cxt)
    def visitDynarr(self, cxt): return self.visitCommon(cxt)
    def visitParselit(self, cxt): return self.visitCommon(cxt)
    def visitPrimkey(self, cxt): return self.visitCommon(cxt)
    def visitPrimtxt(self, cxt): return self.visitCommon(cxt)
    def visitSymbol(self, cxt): return self.visitCommon(cxt)
    def visitLitarr(self, cxt): return self.visitCommon(cxt)
    def visitLitarrcnt(self, cxt): return self.visitCommon(cxt)
    def visitBarelitarr(self, cxt): return self.visitCommon(cxt)
    def visitKeywords(self, cxt): return self.visitCommon(cxt)
    def visitErrorNode(self, errnode): return self.visitCommon(errnode)
