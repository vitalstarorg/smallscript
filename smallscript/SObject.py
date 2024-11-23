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

import io
import sys
import os
import pkgutil
import inspect
import builtins
import importlib
import hashlib
import logging
import traceback
import types
import copy
from pathlib import Path

logger = logging.getLogger('smallscript')
# print(f"=== {logger.getEffectiveLevel()}")

class SObject:
    """
    The base parent for all SObject. SObject setter always return self for chaining multiple updates together.
    """
    def __getattr__(self, item):
        """Intercept attributes and methods access not defined by holders."""
        metaclass = self.metaclass()
        if metaclass.isNil():
            return self.unimplemented(item)

        # look for the holder with fullname e.g. first__last__
        holder = metaclass.holderByName(item)
        if holder.notNil():
            return holder.__get__(self)

        # look for the holder with partial name e.g. first
        partial = item.split('__')
        if len(partial) > 1:
            name = partial[0]
            holder = metaclass.holderByName(name)
            if holder.notNil():
                return holder.__get__(self)
            if hasattr(self, name):
                return getattr(self, name)

        # consider it as an SObject attribute retrieval
        if SObject.hasKey(self, item):
            value = self.getValue(item)
            holder = Holder().obj(value)
            return holder.valueFunc()

        # consider it as an python attribute retrieval
        if item in self.__dict__:
            value = getattr(self, item)
            return value
        elif type(self) is not type:
            klass = type(self)
            if item in klass.__dict__:
                return getattr(klass, item)
            
        return self.unimplemented(item)

    def unimplemented(self, item):
        if SObject.hasKey(self, 'undefined'):
            value = self.getValue('undefined')
            holder = Holder().obj(value)
            return holder.valueFunc()
        return super().__getattribute__(item)

    #### Attributes defined by methods before Holder is functioning
    def metaname(self, metaname=''):
        "Metaclass name."
        if metaname != '':
            return self.setValue('metaname', metaname)
        _metaclass = self._keyName('metaclass')
        if self._has(_metaclass):
            return self._get(_metaclass,nil).name()
        _attrname = self._keyName('metaname')
        if self._has(_attrname):
            return self._get(_attrname, nil)
        res = self._metaname(type(self))
        return res

    def _metaname(self, sClass):
        return self._ss_metas(sClass).head()

    def _ss_metas(self, sClass):
        "Return a list of classnames for class hierarchy."
        # print(f"_ss_metas: {sClass.__name__}")    # diagnoses notebook problem
        if 'ss_metas' in sClass.__dict__:
            # print(f"{sClass.__name__} ss_meta")
            metas = getattr(sClass, 'ss_metas')
            names = [ name.strip() for name in metas.split(',') ]
            return List(names)
        if not issubclass(sClass, SObject):
            # print(f"{sClass.__name__} not subclass SObject")  # nb reports DebugClosure is not SObject
            return List()
        names = List().append(sClass.__name__)
        if sClass != SObject:
            # print(f"{sClass.__name__} sClass != SObject")
            for klass in sClass.__bases__:
                if not issubclass(klass, SObject): continue
                names.append(klass.__name__)
        return names

    def name(self, name=''):
        "Set or get name of this object. In case of set, @self is returned to faciliate builder pattern."
        if name != '':
            return SObject.setValue(self, 'name', String(name))
        attrname = 'name'
        if SObject.hasKey(self, attrname): return SObject.getValue(self, attrname)
        return String()

    def metaclass(self, metaclass = ''):
        "Find the metaclass."
        if metaclass != '':
            return SObject.setValue(self, 'metaclass', metaclass)
        _metaclass = self._keyName('metaclass')
        if self._has(_metaclass):
            return self._get(_metaclass,nil)
        metaname = self.metaname()
        metaclass = sscontext.metaclassByName(metaname)
        return metaclass

    def asSObj(self, pyobj):
        if isinstance(pyobj, SObject): return pyobj
        if isinstance(pyobj, bool): return true_ if pyobj else false_
        if pyobj is None: return nil
        stype = type(pyobj).__name__
        value = pyobj
        # ignoreModules = {'builtins', 'numpy'}
        # ignoreModules = {'builtins'}
        if stype in pytypes:
            pClass = pytypes[stype]
            value = pClass(pyobj)

        # # Python class object
        # elif isinstance(value, type) and value.__module__ not in ignoreModules:
        #     value.ssrun = SObject.ssrun
        # elif isinstance(value, type) and value.__module__ in ignoreModules: pass
        #
        # # Python object
        # elif value.__class__.__module__ in ignoreModules: pass     # ignore object from these modules
        # elif hasattr(value, SObject.ssrun.__name__): pass
        # else:
        #     try:
        #         value.ssrun = types.MethodType(SObject.ssrun, value)
        #     except Exception as e:
        #         self.log(f"fail to set ssrun() to instance of {value.__class__.__module__}: {e}", Logger.LevelWarning)
        return value

    def runThis(self, thisObj):
        "Return an Execution object for apply @thisObj with @self."
        this = self
        if not isinstance(self, SObject):
            from smallscript.core.PythonExt import ObjAdapter
            this = ObjAdapter().object(self)
        obj = this.asSObj(thisObj)
        execution = this.getContext().newInstance('Execution')
        execution.this(this)
        res = obj.visit(execution)
        return res

    def ssrun(self, thisObj, *args, **kwargs):
        "Execute the Execution object from runThis(). @self might not be SObject."
        this = self
        if not isinstance(self, SObject):
            from smallscript.core.PythonExt import ObjAdapter
            this = ObjAdapter().object(self)
        execution = this.runThis(thisObj)
        res = execution(*args, **kwargs)
        return res

    def visit(self, visitor): return visitor.visitSObj(self)
    def getContext(self): return self.metaclass().context()
    def getPackage(self): return self.metaclass().package()

    def nearestParent(self, parentName=''):
        if parentName == '':
            first = self.metaclass().parentNames().head()
            parent = self.getContext().metaclassByName(first)
        else:
            parents = self.inheritedMetas()
            parent = parents.getValue(parentName, nil)
        return parent

    def inheritedMetas(self):
        return self.metaclass()._parentMetaclasses(Map())

    def inheritedHolders(self):
        holders = Map()
        for meta in self.inheritedMetas().values():
            holders.update(meta.holders())
        return holders

    def getSuper(self, parentName=''):
        "Create an instance of its parent metaclass to masquerade this object i.e. limit access only to the parent definition."
        parent = self.nearestParent(parentName)
        parentInstance = parent.createEmpty()    # problematic for Metaclass
        parentInstance.masquerade(self)
        return parentInstance
        # self.createEmpty()    # problematic for Metaclass
        # self.masquerade(self)
        # return parent

    def masquerade(self, sobj=''): return self._getOrSet('masquerade', sobj, nil) # used for @super
    def mutable(self, mutable=''): return self._getOrSet('mutable', mutable, true_) # set mutuable or immatable
    def undefined(self, undefined=''): return self._getOrSet('undefined', undefined, nil)
    def toDebug(self, toDebug=''): return self._getOrSet('toDebug', toDebug, false_)

    def logger(self, logger=''):
        # logger at class level
        metaattrs = self.metaclass().attrs()
        logger = metaattrs._getOrSet('logger', logger, nil)
        if logger.isNil():
            logger = Logger()
            metaattrs.setValue('logger', logger)
        return logger

    def loglevel(self, loglevel=''):
        "Set log level to the logger: DEBUG: 0, INFO: 1, WARNING: 2, ERROR: 3, CRITICAL: 4"
        if loglevel == '': return self.logger().level()
        self.logger().level(loglevel)
        return self

    def log(self, msg, level=0):
        self.logger().log(msg, level)
        return self

    #### Attributes accesses: these are Scope key-value access behavior.
    def __getitem__(self, attname): return self.getValue(attname, nil)
    def __setitem__(self, attname, value): return self.setValue(attname, value)
    def __delitem__(self, attname): return self.delValue(attname)

    def keys(self):
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        return List([obj._varName(keyname) for keyname in obj._keys()])

    def hasKey(self, attname):
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        return obj._has(obj._keyName(attname))

    def delValue(self, attname):
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        return obj._del(obj._keyName(attname))

    def getValue(self, attname, default=None):
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        # need to do this as nil can't be used as default before nil is initialized.
        # nil at runtime in a call has already initialized.
        if default is None: default = nil
        return obj._get(obj._keyName(attname), default)

    def getAsNumber(self, attname, default=0):
        res = self.getValue(attname)
        if res.isNil(): return default
        if isinstance(res, Number): return res.value()
        string = res.toString()
        res = string.asNumber().value()
        return res

    def setValue(self, attname, value):
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        sobj = self.asSObj(value)
        return obj._set(obj._keyName(attname), sobj)

    def copyFrom(self, another):
        if self == another: return self
        for name, holder in self.inheritedHolders().items():
            if not holder.isInstanceAttribute(): continue
            if not another.hasKey(name): continue
            self.setValue(name, another.getValue(name))
        return

    def clone(self):
        instance = self.createEmpty()
        instance.copyFrom(self)
        return instance

    def deepcopy(self): return copy.deepcopy(self)

    def _keys(self): return List(self.__dict__.keys())
    def _has(self, keyname): return keyname in self.__dict__    # slightly faster than vars(self)
    def _get(self, keyname, default): return self.__dict__.get(keyname, default)
    def _set(self, keyname, value): self.__dict__[keyname] = value; return self
    def _del(self, keyname):
        if self._has(keyname):
            del self.__dict__[keyname]
        return self

    def _getOrSet(self, attname, value ='', default =''):  # can't use nil as default
        "Low level SObject getOrSet behavior for initialization."
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        keyname = self._keyName(attname)
        return obj._get(keyname, default) if value == '' else obj._set(keyname, value)

    def _getOrSetDefault(self, attname, defaultType, value =''):
        "Low level SObject getOrSet behavior for initialization and Scope object."
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        keyname = self._keyName(attname)
        if value == '':
            if obj._has(keyname): return self._get(keyname, nil)
            default = self.getContext().newInstance(defaultType)
            obj._set(keyname, default)
            return default
        return obj._set(keyname, value)

    def _varName(self, keyname):
        "Convert internals keyname to public facing name"
        return keyname if len(keyname) <= 3 or keyname[0:3] != 'ss_' else keyname[3:]

    def _keyName(self, attname):
        """Calculate the internals keyname from public facing attname."""
        return attname if len(attname) > 3 and attname[0:3] == 'ss_' else f'ss_{attname}'

    #### Private helper methods
    def _defineHolders(self, holders):
        holders['name'] = Holder().name('name').type('String')
        holders['metaname'] = Holder().name('metaname').type('String')
        holders['mutable'] = Holder().name('mutable').type('True_')
        holders['masquerade'] = Holder().name('masquerade').type('Nil')
        holders['undefined'] = Holder().name('undefined').type('Nil')
        return self

    #### Helper methods
    def __call__(self, *args, **kwargs): return self.createEmpty()
    def createEmpty(self): return type(self)()
    def idDigits(self, n=4): return hex(id(self)).upper()[-n:]
    def isNil(self): return false_
    def notNil(self): return not self.isNil()
    def isDefined(self): return true_
    def notDefined(self): return not self.isDefined()
    def isEmpty(self): return false_
    def notEmpty(self): return not self.isEmpty()
    def toString(self): return String(self)
    def print(self, suppressed=''):
        if suppressed == '': print(self.info())
        # return self

    def _isNil(self, pyobj):
        "This is used deal with heavily customized Python object e.g. numpy array. Or we can use 'pyobj is nil' for identity comparison."
        if not isinstance(pyobj, SObject): return false_
        return pyobj.isNil()

    def info(self, offset=0):
        buffer = io.StringIO()
        padding = " " * offset
        buffer.write(f"{padding}{self.toString()}\n")
        metaclasses = self.inheritedMetas().values()
        for metaclass in metaclasses:
            for holder in metaclass.holders().values():
                name = holder.name()
                if SObject.hasKey(self, name):
                    buffer.write(f"{padding}  {metaclass.name()}.{name} = {SObject.getValue(self, name)}\n")
        output = buffer.getvalue()
        return String(output)

    def describe(self):
        "Description for __repr__ and self.info()"
        if self.name().isEmpty():
            return String(f"a {self.metaname()}")
        return self.name()

    def __repr__(self): return f"{self.describe()}:{self.metaname()} {self.idDigits()}"

class Holder(SObject):
    """
    Holder to an object and can be used to define an attribute. @obj can be both SObject or Python object.
    """
    def type(self, type=''): return self._getOrSet('type', String(type), 'Nil')     # type hint
    def obj(self, obj=''): return self._getOrSet('obj', obj, nil)                   # optional
    def pyfunc(self, func=''): return self._getOrSet('pyfunc', func, nil)           # optional
    def method(self, method=''): return self._getOrSet('method', method, nil)       # optional
    def instanceType(self, instanceType=''): return self._getOrSet('instanceType', instanceType, true_)
    def asClassType(self): return self.instanceType(false_)

    def isInstanceAttribute(self): return self.instanceType() and self.method().isNil()
    def isInstanceMethod(self): return self.instanceType() and self.method().notNil()
    def isClassAttribute(self): return not self.instanceType() and self.method().isNil()
    def isClassMethod(self): return not self.instanceType() and self.method().notNil()

    def valueFunc(self):
        def value():
            return self.obj()
        return value

    def __call__(self, func):
        self.name(func.__name__).type('Closure')
        self.pyfunc(func)
        return self

    def __get__(self, obj, owner = None):  # owner is ignored
        """Implement the descriptor protocol."""
        # WARNING: don't use scope as local variable. It will disrupt scope var lookup.
        original = owner if obj is None else obj
        def getOrSetSObj(original, sobj, value=None):
            attname = self.name()
            res = original
            if value is None:
                if sobj.hasKey(attname):
                    return sobj.getValue(attname)
                else:   # find default value
                    metaclass = sobj.metaclass()
                    type = self.type()
                    if metaclass.notNil():
                        res = metaclass.context().metaclassByName(type).createEmpty()
                        if res is nil or type == 'True_' or type == 'False_':  # don't need to save these default values.
                            return res
                        value = res
                    else:
                        logger.warning(f"Found no metaclass for type '{type}' defined by {sobj.metaname()}.{self.name()}")
                        return nil
            if sobj.mutable():
                sobj.setValue(attname, value)
            return res

        def getOrSet(value=None): return getOrSetSObj(original, obj, value)

        res = nil
        method = self.method()
        if method.isNil():
            if self.instanceType():
                # Instance attribute access
                if obj is None:
                    return nil
                return getOrSet
            if obj is None:
                # Class attribute access from Python class
                obj = self.getContext().metaclassByName(self._metaname(owner)).attrs()
            else:
                # Class attribute access from sobject
                obj = obj.metaclass().attrs()
            return getOrSet
        else:
            if obj is not None:
                if self.instanceType():
                    # Instance method
                    res = obj.runThis(method)
                else:
                    # Class method invoked from sobject
                    res = obj.metaclass().attrs().runThis(method)
            elif owner is not None:
                if not self.instanceType():
                    # Class method invoked from Python class
                    metaclass = self.getContext().metaclassByName(self._metaname(owner))
                    attrs = metaclass.attrs()
                    res = attrs.runThis(method)
        return res

    #### Private helper methods
    def _defineHolders(self, holders):
        holders['type'] = Holder().name('type').type('String')
        holders['obj'] = Holder().name('obj').type('Nil')
        holders['pyfunc'] = Holder().name('pyfunc').type('Nil')
        holders['method'] = Holder().name('method').type('Nil')
        holders['instanceType'] = Holder().name('instanceType').type('True_')
        return self
    def describe(self): return f"{self.name()},{self.type()}"

class Primitive(SObject):
    """Base class for SObject primitives."""
    def metaclass(self, metaclass = ''):
        # Don't allow setting metaclass for primitive
        if metaclass != '': return self
        return super().metaclass()

    def visit(self, visitor): return visitor.visitPrimitive(self)
    def setValue(self, attname, value): return self
    def asString(self): return self.toString()
    def info(self): return self.asString()

class String(str, Primitive):
    """SObject string"""
    def __new__(cls, string = ''): return super(String, cls).__new__(cls, string)
    def __init__(self, value = ''): SObject.__init__(self)
    def __add__(self, val): return String(f"{self}{val}")
    def __eq__(self, val): return super().__eq__(val)
    def __hash__(self): return super().__hash__()
    def visit(self, visitor): return visitor.visitString(self)
    def asNumber(self): return Number().fromString(self)
    def len(self): return len(self)
    def isEmpty(self): return self.len() == 0
    def sha256(self, digits=16): return hashlib.sha256(self.encode()).hexdigest()[0:digits]
    def isSymbol(self): return false_ if self.isEmpty() or self[0] != '#' else true_
    def asString(self): return String(f"'{self[1:]}'") if self.isSymbol() else String(f"'{self}'")
    def toString(self): return self

class True_(Primitive):
    """SObject true class with singleton true_."""
    def __new__(cls):
        global true_
        if not 'true_' in globals():
            true_ = super().__new__(cls)
        return true_

    def __bool__(self): return True     # true_ won't work for 'not', it has to return Python bool
    def createEmpty(self): return self
    def isFalse(self): return false_
    def isTrue(self): return true_
    def asString(self): return "true"
    def describe(self): return "true"

class False_(Primitive):
    """SObject false class with singleton false_."""
    def __new__(cls):
        global false_
        if not 'false_' in globals():
            false_ = super().__new__(cls)
        return false_

    def __bool__(self): return False
    def createEmpty(self): return self
    def isFalse(self): return true_
    def isTrue(self): return false_
    def asString(self): return "false"
    def describe(self): return "false"

true_ = True_()
false_ = False_()

class Nil(Primitive):
    "@nil is a singleton from this class represents nothing."
    def __new__(cls):
        global nil
        if not 'nil' in globals():
            nil = super().__new__(cls)
            # nil.name('nil')
        return nil

    def __call__(self, *args, **kwargs): return nil
    def visit(self, visitor): return visitor.visitNil(self)
    def createEmpty(self): return self
    def isNil(self): return true_
    def _keys(self): return List()
    def _has(self, keyname): return false_
    def _get(self, keyname, default): return nil
    def _set(self, keyname, value): return self
    def _del(self, keyname): return self
    def asString(self): return "nil"
    def describe(self): return self.asString()

nil = Nil()

class Undefined(SObject):
    "@undefined is a singleton for default argument."
    def __new__(cls):
        global undefined
        if not 'undefined' in globals():
            undefined = super().__new__(cls)
        return undefined

    def __call__(self, *args, **kwargs): return undefined
    def isDefined(self): return false_
    def describe(self): return "undefined"

undefined = Undefined()

class List(list, Primitive):
    """SObject list class."""
    def __init__(self, *args):
        list.__init__(self, *args)
        SObject.__init__(self)

    def visit(self, visitor): return visitor.visitList(self)
    def len(self): return len(self)
    def isEmpty(self): return self.len() == 0
    def notEmpty(self): return not self.isEmpty()
    def head(self): return nil if self.isEmpty() else self[0]
    def append(self, obj): super().append(obj); return self
    def add(self, alist): self.extend(alist); return self
    def at(self, index): return self[int(index)]
    def includes(self, aList):
        return all(item in self for item in aList)

class Map(dict, Primitive):
    """SObject map class."""
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        dict.__init__(self, *args)
        SObject.__init__(self)

    def visit(self, visitor): return visitor.visitMap(self)
    def len(self): return len(self)
    def isEmpty(self): return self.len() == 0
    def notEmpty(self): return not self.isEmpty()
    def values(self): return List(super().values())
    def head(self): return nil if self.isEmpty() else self.values().head()
    def keys(self): return List(super().keys())
    def hasKey(self, name): found = name in self; return found
    def setValue(self, name, value): self[name] = self.asSObj(value); return self
    def getValue(self, name, default=nil): res = self.get(name, default); return res
    def delValue(self, name): 
        if self.hasKey(name): del self[name]
        return self

class Metaclass(SObject):
    "Metaclass defines a SObject structure."
    context = Holder().name('context').type('Context')
    package = Holder().name('package').type('Package')
    factory = Holder().name('factory').type('Nil')
    holders = Holder().name('holders').type('Map')
    parentNames = Holder().name('parentNames').type('List')

    def __call__(self): return self.createEmpty()

    def attrs(self):
        keyname = self._keyName('attrs')
        if not self._has(keyname):
            classAttrs = SObject().metaclass(self)
            self._set(keyname, classAttrs)
        else:
            classAttrs = self._get(keyname, nil)
        return classAttrs

    def createEmpty(self):
        """create an empty obj for this metaclass, including Metaclass."""
        factory = self.factory()
        if factory == self:     # only true when self is the metaclass object of MetaClass
            instance = Metaclass()
        else:
            instance = factory.createEmpty()
        instance.metaclass(self)
        return instance

    def addAttr(self, attrname, typeHint, classType=false_):
        holders = self.holders()
        holder = Holder().name(attrname).type(typeHint)
        if classType: holder.asClassType()
        holders[attrname] = holder
        return self

    def addMethod(self, name, closure, classType=false_):
        holders = self.holders()
        # fullname = closure.ssSignature(name)
        ssname = closure.ssSignature()
        holder = Holder().name(name).type('Closure').method(closure)
        if classType: holder.asClassType()
        # holders[fullname] = holder  # fullname
        holders[ssname] = holder    # Smallscript protocol
        holders[name] = holder      # prefix for python protocol
        return self

    def importFrom(self, sClass):
        self._importHolders(sClass)
        self._importMetanames(sClass)
        self._createFactory(sClass)
        return self

    def _importHolders(self, sClass):
        "Extracts all attribute definitions from holder objects."
        holders = Map()
        if sClass == SObject:
            SObject()._defineHolders(holders)
        elif sClass == Holder:
            Holder()._defineHolders(holders)
        else:
            for attname, item in vars(sClass).items():
                if attname.startswith('__'): continue
                if isinstance(item, classmethod) or isinstance(item, staticmethod): continue
                if inspect.isfunction(item):
                    if hasattr(item, 'holder'):
                        holder = item.holder
                        holders[attname] = holder.name(attname)
                    continue
                if isinstance(item, Holder):
                    holders[attname] = item.name(attname)
                    continue
        self.setValue('holders', holders)
        return self

    def _importMetanames(self, sClass):
        "Determine metaclass name and its parent names from ss_metas first then its Python class hierarchy."
        metanames = self._ss_metas(sClass)
        self.name(metanames.pop(0))
        self.setValue('parentNames',metanames)
        return self

    def _createFactory(self, sClass):
        if sClass == SObject: factory = SObject()
        elif sClass == Nil: factory = nil
        elif sClass == Metaclass: factory = self
        else: factory = sClass()
        self.setValue('factory', factory)
        return self

    def _getHolder(self, name): return self.holders()[name] if name in self.holders() else nil

    def holderByName(self, name):
        holders = self.holders()
        if name in holders:
            return holders[name]
        context = self.context()
        for parentName in self.parentNames():
            parent = context.metaclassByName(parentName)
            if parent.notNil():     # parent might not be ready
                holder = parent.holderByName(name)
                if holder.notNil():
                    return holder
        return nil

    def _parentMetaclasses(self, parentMap):
        parentMap[self.name()] = self
        context = self.context()
        for parentName in self.parentNames():
            parent = context.metaclassByName(parentName)
            if parent.isNil(): continue
            parent._parentMetaclasses(parentMap)
        return parentMap

    def toPython(self):
        classname = self.name()

        metas = List().append(classname)
        for parent in self.parentNames():
            if parent == 'SObject': continue
            metas.append(parent)
        metas = ", ".join(metas)

        attributes = List()
        methods = Map()         # use it as ordered Set
        for holder in self.holders().values():
            if holder.method().isNil():
                attributes.append(holder)
            else:
                methods[holder] = 1

        source = self.getContext().newInstance('TextBuffer')
        source.delimiter("\n").skipFirstDelimiter()
        source.writeLine("#### Generated file\n")
        source.writeLine("from smallscript.SObject import *\n")
        source.writeLine(f"class {classname}(SObject):")

        attrSource = self.getContext().newInstance('TextBuffer')
        attrSource.delimiter("\n").skipFirstDelimiter()
        attrSource.writeLine(f"ss_metas = '{metas}'")
        for attrHolder in attributes:
            attrDef = f"{attrHolder.name()} = Holder().name('{attrHolder.name()}')"
            if attrHolder.type().notNil():
                attrDef = f"{attrDef}.type('{attrHolder.type()}')"
            if not attrHolder.instanceType():
                attrDef = f"{attrDef}.asClassType()"
            attrSource.writeLine(attrDef)
        attrSource.writeLine()

        methodSource = self.getContext().newInstance('TextBuffer')
        methodSource.delimiter("\n").skipFirstDelimiter()
        for methodHolder in methods.keys():
            method = methodHolder.method()
            if methodHolder.instanceType():
                methodSource.writeLine("@Holder()")
            else:
                methodSource.writeLine("@Holder().asClassType()")
            # name = method.ssSignature()
            name = methodHolder.name()
            namedMethod = method.toNamedPython("    ", name)
            methodSource.writeLine(namedMethod)

        source.writeLine(attrSource.indent("    "))
        source.writeLine(methodSource.indent("    ", true_))
        return source.text()

    def asString(self): return self.toPython()

class Package(SObject):
    "Package to a set of metaclass loaded from files, or created dynamically."
    context = Holder().name('context').type('Context')
    metaclasses = Holder().name('metaclasses').type('Map')
    path = Holder().name('path').type('String')

    #### Metaclass definition import: limited SObject features before initialization.
    def importSingleSObject(self, sClass):
        # from importSObjects()
        metaname = self._metaname(sClass)
        metaclass = self.createMetaclass(metaname)
        metaclass.importFrom(sClass)

        # from importMethods()
        for holder in metaclass.holders().values():
            if holder.type() == 'Closure' and holder.pyfunc() is not nil:
                method = self.context().newInstance('Closure')
                holder.method(method)
                pyfunc = holder.pyfunc()
                method.takePyFunc(pyfunc)

        # from initClasses()
        holder = metaclass.holderByName('metaInit')
        if holder.isNil(): return self
        method = holder.method()
        exeContext = metaclass.attrs().runThis(method)
        res = exeContext()
        return self

    def listSObjects(self):
        "List SObjects from named Python package."
        package_name = self.name()
        package = importlib.import_module(package_name)
        sobjs = List()
        for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            if module_name in sys.modules:
                module = sys.modules[module_name]
            else:
                module = importlib.import_module(module_name)
            for name, pyClass in inspect.getmembers(module, inspect.isclass):
                # filter those class defined in this module, not imported within the module.
                if pyClass.__module__ == module.__name__ and issubclass(pyClass, SObject):
                    sobjs.append(pyClass)
        return sobjs

    def importSObjects(self):
        "Import SObject definitions from Python package."
        sClasses = self.listSObjects()
        for sClass in sClasses:
            metaname = self._metaname(sClass)
            metaclass = self.createMetaclass(metaname)
            metaclass.importFrom(sClass)
        return self

    def importMethods(self):
        "Import Method definitions from SObject class."
        for metaclass in self.metaclasses().values():
            for holder in metaclass.holders().values():
                if holder.type() == 'Closure' and holder.pyfunc() is not nil:
                    method = self.context().newInstance('Closure')
                    holder.method(method)
                    pyfunc = holder.pyfunc()
                    method.takePyFunc(pyfunc)
        return self

    def initClasses(self):
        "Invoke all ss_metaInit() if defined."
        for metaclass in self.metaclasses().values():
            holder = metaclass.holderByName('metaInit')
            if holder.isNil(): continue
            method = holder.method()
            exeContext = metaclass.attrs().runThis(method)
            scope = nil # defined here to stop Execution._findScopeFromFrames() beyond this point.
            res = exeContext()
        return self

    def createMetaclass(self, metaname):
        "Create an initial metaclass."
        context = self.getValue('context')
        if not self.hasKey('metaclasses'):  # init metaclasses
            metaclasses = Map()
            self.setValue('metaclasses', metaclasses)
            if self.name() == 'smallscript':
                # create a placeholder for Metaclass metaclass
                metametaclass = Metaclass().name(Metaclass.__name__)
                metametaclass.metaclass(metametaclass).setValue('package', self).setValue('context', context)
                metaclasses[Metaclass.__name__] = metametaclass
        else:
            metaclasses = self.getValue('metaclasses')

        metametaclass = context.metaclassByName(Metaclass.__name__)
        if metaname in metaclasses:
            return metaclasses[metaname]
        metaclass = Metaclass().name(metaname).\
                        metaclass(metametaclass).\
                        setValue('package', self).\
                        setValue('context', context).\
                        factory(SObject())          # default factory, will be rewritten _createFactory()
        metaclasses[metaname] = metaclass
        return metaclass

    def metaclassByName(self, metaname):
        "Lookup metaclass in this package."
        classes = self.getValue('metaclasses', Map())
        res = classes.get(metaname, nil)
        return res

    def newInstance(self, metaname):
        "Create an sobject."
        metaclass = self.metaclassByName(metaname)
        instance = metaclass.createEmpty()
        return instance

    def isEmpty(self):
        if not self.hasKey('metaclasses'): return true_
        return self.metaclasses().isEmpty()

    #### Package loading and unloading.
    def setAndValidatePath(self, pathname=""):
        "Validate and set the path to @path."
        pathname = self.path() if pathname == "" else pathname
        if pathname == "": return false_
        path = Path(pathname)
        if path.exists() and self._initPath(path).exists():
            self.path(String(path))
            return true_
        self.path(String())
        return false_

    def findPath(self, pkgname=""):
        "Find package according the sys.path. @path will be set if found and valid."
        res = pkgpath = String()
        if pkgname == "": pkgname = self.name()
        if pkgname != "":
            for p in sys.path:
                path = Path(p)
                ppath = List(path.glob(f"{pkgname}/"))
                if ppath.notEmpty():
                    pkgpath = String(ppath.head())
                    break
        res = self.setAndValidatePath(pkgpath)
        if not res:
            self.log(f"Validation failed for path '{pkgpath}', probably __init__.py not found.", Logger.LevelInfo)
        return res

    def _loadSObjects(self):
        self.importSObjects()
        self.importMethods()
        self.initClasses()
        return self

    def loadSObjects(self):
        "Load the metaclasses from SObjects defined in this package."
        self.log(f"Loading SObjects from '{self.name()}'", Logger.LevelInfo)
        if self.path().isEmpty(): return self
        pkgName = self.name()
        initFile = self._initPath(self.path())
        spec = importlib.util.spec_from_file_location(pkgName, initFile)
        package = importlib.util.module_from_spec(spec)
        sys.modules[pkgName] = package
        spec.loader.exec_module(package)
        self._loadSObjects()
        return self

    def unloadSObjects(self):
        "Unload the metaclasses from this package, and SObject found from sys.modules, leaving this package object empty."
        self.log(f"Unloading SObjects from '{self.name()}'", Logger.LevelInfo)
        self.metaclasses(Map())
        # self.getContext().removePackage(self.name())

        ssmodules = [key for key in sys.modules.keys() if key.startswith(self.name())]
        for ss in ssmodules:
            if ss in sys.modules:
                self.log(f"sys.modules['{ss}'] deleted.", Logger.LevelInfo)
                del sys.modules[ss]
        return self

    def reloadSObjects(self):
        "unloadSObjects() and loadSObjects from pacakge source."
        self.unloadSObjects();
        return self.loadSObjects()

    def refreshSources(self, forced=false_):
        "Generate the .py sources from updated .ss sources."
        self.log(f"Refreshing SmallScript package '{self.name()}'.", Logger.LevelInfo)
        ssnames = self.listFilenames("*.ss")
        for name in ssnames:
            sspath = Path(self.path()) / f"{name}.ss"
            pypath = Path(self.path()) / f"{name}.py"
            if pypath.exists():
                ssmtime = sspath.stat().st_mtime
                pymtime = pypath.stat().st_mtime
                if ssmtime < pymtime and not forced:   # ss has not been modified since last compilation.
                    return self
            self.log(f"Generate {name}.py by running {name}.ss.", Logger.LevelInfo)
            closure = self.getContext().newInstance('Closure')
            txt = self.readFile(sspath)
            closure.compile(txt)
            scope = self.getContext().createScope().setValue('package', self)
            res = closure(scope)
            txt = res.asString()
            self.writeFile(pypath, txt)
        return self

    def load(self, forced=false_):
        "Load SObjects from sources. Regenerate py sources if necessary."
        self.log(f"Loading SmallScript package '{self.name()}'.", Logger.LevelInfo)
        self.unloadSObjects();
        self.refreshSources(forced);
        return self.loadSObjects()

    #### Helper methods
    def _initPath(self, pkgpath): return Path(pkgpath) / "__init__.py"
    def isLoaded(self): return true_ if self.name() in sys.modules else false_
    def notLoaded(self): return not self.isLoaded()

    #### File I/O
    def listFilePaths(self, pattern="*"):
        filepaths = List()
        if self.path().isNil():
            return filepaths
        path = Path(self.path())
        for p in path.glob(pattern):
            filepaths.append(String(p))
        return filepaths

    def listFilenames(self, pattern="*"):
        filenames = List()
        if self.path().isNil():
            return filenames
        path = Path(self.path())
        for p in path.glob(pattern):
            filenames.append(String(p.stem))
        return filenames

    def readFile(self, pathname):
        output = ""
        path = Path(self.path()) / pathname
        if path.exists() and not path.is_dir():
            try:
                output = path.read_text()
            except Exception as e:
                stackTrace = traceback.format_exc()
                self.log(f"Read '{path}' error: {stackTrace}", Logger.LevelWarning)
        return String(output)

    def writeFile(self, pathname, text):
        path = Path(self.path()) / pathname
        try:
            path.write_text(text)
        except Exception as e:
            stackTrace = traceback.format_exc()
            self.log(f"Write '{path}' error: {stackTrace}", Logger.LevelWarning)
            return nil
        return self

    def _deleteFile(self, pathname):
        path = Path(self.path()) / pathname
        try:
            path.unlink()
        except Exception as e:
            stackTrace = traceback.format_exc()
            self.log(f"Delete '{path}' error: {stackTrace}", Logger.LevelWarning)
            return nil
        return self

    def _touchFile(self, pathname):
        path = Path(self.path()) / pathname
        path.touch(exist_ok=True)
        return self

class Context(SObject):
    """
    It provides context for SS methods to function. It provides access to other resources e.g. packages, execution scopes, etc. @root is the root context has maximum access to all resources. Customized context can be created for some executions.
    """
    packages = Holder().name('packages').type('Map')
    rootScope = Holder().name('rootScope').type('Scope')
    FirstArg = Holder().name('FirstArg').type('String').asClassType()

    @Holder().asClassType()
    def metaInit(scope):
        self = scope['self']
        self.FirstArg('scope')
        return self

    def loadPackage(self, pkgname):
        "Load metaclasses from a SObject package."
        pkg = self.getOrNewPackage(pkgname)
        if pkg.isEmpty(): pkg._loadSObjects()
        return pkg

    def getOrNewPackage(self, pkgname):
        pkgs = self.getValue('packages')
        if pkgs.isNil():
            pkgs = Map()
            self.setValue('packages', pkgs)
        if pkgname in pkgs:
            return pkgs[pkgname]
        pkg = Package().name(pkgname).context(self)
        pkgs[pkg.name()] = pkg
        return pkg

    def metaclassByName(self, metaname):
        "Find metaclass in last-in-first-out by name. Later package can override earlier package to allow deferred implementation."
        pkgs = self.getValue('packages', Map())
        res = nil
        for pkg in pkgs.values()[::-1]:
            metaclass = pkg.metaclassByName(metaname)
            if metaclass.notNil():
                res = metaclass
                break
        return res

    def packageByMetaname(self, metaname):
        "Find the containing package for a metaclass name."
        res = nil
        for pkg in self.packages().values()[::-1]:
            metaclass = pkg.metaclassByName(metaname)
            if metaclass.notNil():
                res = pkg
                break
        return res

    def asSObj(self, pyobj):
        "Overriden SObject.asSObj() to injects ssrun() into pyobj"
        sobj = super().asSObj(pyobj)
        if isinstance(sobj, SObject): return sobj

        value = sobj
        ignoreModules = {'builtins', 'numpy'}

        # Python class object
        if isinstance(value, type) and value.__module__ not in ignoreModules:
            value.ssrun = SObject.ssrun
        elif isinstance(value, type) and value.__module__ in ignoreModules: pass

        # Python object
        elif value.__class__.__module__ in ignoreModules: pass     # ignore object from these modules
        elif hasattr(value, SObject.ssrun.__name__): pass
        else:
            try:
                value.ssrun = types.MethodType(SObject.ssrun, value)
            except Exception as e:
                self.log(f"fail to set ssrun() to instance of {value.__class__.__module__}: {e}", Logger.LevelWarning)
        return value

    def newInstance(self, metaname):
        "Create an sobject."
        metaclass = self.metaclassByName(metaname)
        instance = metaclass.createEmpty()
        return instance

    def reset(self):
        self.setValue('packages', Map())  # Reset all packages
        return self

    def createScope(self):
        from smallscript.core.PythonExt import PyGlobals
        rootScope = self.rootScope()
        if not rootScope.locals().hasKey('root'):
            rootScope.name('rootScope')
            rootScope['true'] = true_
            rootScope['false'] = false_
            rootScope['nil'] = nil
            rootScope['context'] = self.getContext()
            rootScope['root'] = rootScope
            pyscope = PyGlobals().name("pybuiltins").locals(vars(builtins))
            rootScope.addScope(pyscope)
        scope = Scope()
        scope.setValue('scope', scope)
        scope.parent(rootScope)

        # Add calling locals & globals into scope object. Looks like they are snapshots.
        frame = inspect.currentframe()
        outer_frame = frame.f_back
        pyscope = PyGlobals().name("pyglobals").locals(outer_frame.f_globals)
        scope.addScope(pyscope)
        pyscope = PyGlobals().name("pylocals").locals(outer_frame.f_locals)
        scope.addScope(pyscope)
        return scope

    def interpret(self, smallscript):
        closure = self.newInstance('Closure')
        closure.interpret(smallscript)
        if closure.script().hasError(): return nil
        return closure

    def compile(self, smallscript):
        closure = self.newInstance('Closure')
        closure.compile(smallscript)
        if closure.script().hasError(): return nil
        return closure

class Scope(SObject):
    """
    Scope object defines the variable lookup.
    """
    #### Attributes that can't use Holder as Scope overridden major protocols.
    def locals(self, locals=''): return self._getOrSetDefault('locals', 'Map', locals)
    def scopes(self, scopes=''): return self._getOrSetDefault('scopes', 'List', scopes)
    def objs(self, objs=''):  return self._getOrSetDefault('objs', 'List', objs)
    def parent(self, parent=''):  return self._getOrSet('parent', parent, nil)
    def context(self, context=''): return self._getOrSet('context', context, nil)

    #### Add scopes, objs, and locals
    def setSelf(self, obj): self.setValue('self', obj); return self
    def addScope(self, scope): self.scopes().insert(0, scope); return self

    def addVars(self, map):
        varScope = Scope()
        varScope.locals(map)
        self.addScope(varScope)

    def addObj(self, obj):
        self.objs().insert(0, obj)
        self.setSelf(obj)
        return self

    #### Override SObject get and set behavior
    def keys(self):
        # if super().hasKey('masquerade'): return super().keys()
        return self.locals().keys()

    def hasKey(self, attname):
        # if super().hasKey('masquerade'): return super().hasKey(attname)
        return self.locals().hasKey(attname)

    def delValue(self, attname):
        # if super().hasKey('masquerade'): return super().delValue(attname)
        if self.locals().hasKey(attname):
            del self.locals()[attname]
        return self

    def getValue(self, attname, default=nil):
        ref = self.lookup(attname)
        if ref == undefined: return default
        return ref.getValue(attname)
        # return self.locals().getValue(attname, default)

    def setValue(self, attname, value):
        ref = self.lookup(attname)
        if ref == undefined:
            self.locals().setValue(attname, self.asSObj(value))
        else:
            ref.setValue(attname, self.asSObj(value))
        return self

    #### Scope behavior
    def createScope(self):
        scope = Scope().parent(self)
        scope.locals().setValue('scope', scope)
        return scope

    def newInstance(self, type):
        instance = self.getContext().newInstance(type)
        return instance

    def lookup(self, key, default=undefined):
        "Return a sobject contains the @key from self, scopes and parent scope."
        # if self.hasKey(key): return self
        if self.locals().hasKey(key): return self.locals()
        classAttrs = self.metaclass().attrs()
        if classAttrs.hasKey(key): return classAttrs
        for obj in self.objs():
            if obj.hasKey(key): return obj
            classAttrs = obj.metaclass().attrs()
            if classAttrs.hasKey(key): return classAttrs
        obj = self.parent()
        while obj.notNil():
            # if obj.hasKey(key): return obj
            # if obj.locals().hasKey(key): return obj
            obj1 = obj.lookup(key, undefined)
            if obj1 != undefined: return obj1
            obj = obj.parent()
        for scope in self.scopes():
            if scope.hasKey(key): return scope
        if self == self.getContext().rootScope():
            # If this is a rootScope(), try to find it as Metaclass name.
            pkg = self.getContext().packageByMetaname(key)
            if pkg.notNil(): return pkg.metaclasses()
        return default

    #### Helpers
    def info(self, offset=0):
        buffer = io.StringIO()
        padding = " " * offset
        buffer.write(f"{padding}{self.toString()}\n")
        for key in self.keys():
            buffer.write(f"{padding}  {key} = {self.getValue(key).toString()}\n")
        for scope in self.scopes():
            buffer.write(scope.info(2))
        for obj in self.objs():
            buffer.write(f"{padding}  obj:")
            buffer.write(obj.info(2))
            buffer.write(f"{padding}  obj.class:")
            buffer.write(obj.metaclass().attrs().info(2))
        if self.parent().notNil():
            buffer.write(f"{padding}parent = {self.parent().toString()}\n")
        output = buffer.getvalue()
        return String(output)

class Number(Primitive):
    def value(self, value=''):
        if value != '' and not isinstance(value, SObject):
            if isinstance(value, int):
                value = Integer(value)
            elif isinstance(value, float):
                value = Float(value)
            else:
                value = Number().fromString(String(value))
        return self._getOrSet('number', value, 'Integer')

    def __init__(self, number=0):
        if not isinstance(number, SObject):
            if isinstance(number, int):
                number = Integer(number)
            elif isinstance(number, float):
                number = Float(number)
            else:
                self.fromString(String(number))
                return
        self.value(number)

    def visit(self, visitor): return visitor.visitNumber(self)
    def __int__(self): return int(self.value())
    def __index__(self): return int(self.value())
    def __float__(self): return float(self.value())
    def __abs__(self): return abs(self.value())

    def __floordiv__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val // self.value()
        else:
            res = self.value() // val
        return res

    def __add__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val + self.value()
        else:
            res = self.value() + val
        return res

    def __radd__(self, val): return self.__add__(val)
    def __rsub__(self, val): return self.__sub__(val)
    def __rmul__(self, val): return self.__mul__(val)
    def __rtruediv__(self, val): return self.__truediv__(val)

    def __mul__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val * self.value()
        else:
            res = self.value() * val
        return res

    def __truediv__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val / self.value()
        else:
            res = self.value() / val
        return res

    def __eq__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val == self.value()
        else:
            res = self.value() == val
        return res

    def __gt__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val <= self.value()
        else:
            res = self.value() > val
        return res

    def __lt__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val >= self.value()
        else:
            res = self.value() < val
        return res

    def __ge__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val < self.value()
        else:
            res = self.value() >= val
        return res

    def __le__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val > self.value()
        else:
            res = self.value() <= val
        return res

    def __mod__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val % self.value()
        else:
            res = self.value() % val
        return res

    def __sub__(self, val):
        if isinstance(val, Number): val = val.value()
        if isinstance(val, Float):
            res = val - self.value()
        else:
            res = self.value() - val
        return res

    def fromString(self, string):
        number = Number()
        if '.' in string:
            number.value(Float(string))
        else:
            number.value(Integer(string))
        return number

    def __hash__(self): return self.value().__hash__()
    def __str__(self): return self.toString()
    def asSObj(self, pyobj): return Number(pyobj)
    def asNumber(self): return self
    def asFloat(self): return float(self.value())
    def asInt(self): return int(self.value())
    def asString(self): return self.toString()
    def toString(self): return String(self.value())
    def __repr__(self): return self.toString()

class Integer(int, Primitive):
    def __new__(cls, number = 0): return super(Integer, cls).__new__(cls, number)
    def __init__(self, value = 0): SObject.__init__(self)

    def __floordiv__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__floordiv__(val)
        return Number().value(res)

    def __add__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__add__(val)
        return Number().value(res)

    def __mul__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__mul__(val)
        return Number().value(res)

    def __truediv__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__truediv__(val)
        return Number().value(res)

    def __eq__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__eq__(val)
        return res

    def __gt__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__gt__(val)
        return res

    def __lt__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__lt__(val)
        return res

    def __mod__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__mod__(val)
        return Number().value(res)

    def __sub__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__sub__(val)
        return Number().value(res)

    def __hash__(self): return super().__hash__()
    def asSObj(self, pyobj): return Integer(pyobj)
    def asString(self): return String(f"{self}")
    def describe(self): return String(f"{self} {hex(self)}")

class Float(float, Primitive):
    def __new__(cls, number = 0): return super(Float, cls).__new__(cls, number)
    def __init__(self, value = 0): SObject.__init__(self)

    def __floordiv__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__floordiv__(val)
        return Number().value(res)

    def __add__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__add__(val)
        return Number().value(res)

    def __mul__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__mul__(val)
        return Number().value(res)

    def __truediv__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__truediv__(val)
        return Number().value(res)

    def __eq__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__eq__(val)
        return res

    def __gt__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__gt__(val)
        return res

    def __lt__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__lt__(val)
        return res

    def __mod__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__mod__(val)
        return Number().value(res)

    def __sub__(self, val):
        if isinstance(val, Number): val = val.value()
        res = super().__sub__(val)
        return Number().value(res)

    def __hash__(self): return super().__hash__()

    def asSObj(self, pyobj): return Float(pyobj)
    def asString(self): return String(f"{self}")
    def describe(self): return f"{self}f"

class Logger(SObject):
    LevelDebug = 0; LevelInfo = 1; LevelWarning = 2; LevelError = 3; LevelCritical = 4
    level = Holder().name('level').type('Integer')

    def log(self, msg, level=0):
        frame = inspect.currentframe().f_back.f_back
        if frame is not None:
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            msg = f"{msg} - {filename} line {lineno}"

        if level >= self.level():
            if level == self.LevelDebug: logger.debug(msg); return self
            if level == self.LevelInfo: logger.info(msg); return self
            if level == self.LevelWarning: logger.warning(msg); return self
            if level == self.LevelError: logger.error(msg); return self
            if level == self.LevelCritical: logger.critical(msg); return self
        return self

pytypes = Map(str = String, int = Number, float = Number, dict = Map, list = List)

sscontext = Context().name('sscontext').reset()
sscontext.loadPackage('smallscript') # This global root context is the first Context object got created.