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
import xxhash
import logging
import traceback
from pathlib import Path

class SObject:
    """
    The base parent for all SObject. SObject setter always return self for chaining multiple updates together.
    """
    def __getattr__(self, item):
        """Intercept attributes and methods access not defined by holders."""
        metaclass = self.metaclass()
        if metaclass.isNil():
            return self.unimplemented(item)
        holder = metaclass.holderByName(item)
        if holder.notNil():
            return holder.__get__(self)
        if self.hasKey(item):
            value = self.getValue(item)
            holder = Holder().obj(value)
            return holder.valueFunc()
        return self.unimplemented(item)

    def unimplemented(self, item):
        if self.hasKey('undefined'):
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
        ret = self._metaname(type(self))
        return ret

    def _metaname(self, sClass):
        return self._ss_metas(sClass).head()

    def _ss_metas(self, sClass):
        "Return a list of classnames for class hierarchy."
        if 'ss_metas' in sClass.__dict__:
            metas = getattr(sClass, 'ss_metas')
            names = [ name.strip() for name in metas.split(',') ]
            return List(names)
        if not issubclass(sClass, SObject):
            return List()
        names = List().append(sClass.__name__)
        if sClass != SObject:
            for klass in sClass.__bases__:
                if not issubclass(klass, SObject): continue
                names.append(klass.__name__)
        return names

    def name(self, name=''):
        "Set or get name of this object. In case of set, @self is returned to faciliate builder pattern."
        if name != '':
            return SObject.setValue(self, 'name', String(name))
        attrname = 'name'
        if self.hasKey(attrname): return SObject.getValue(self, attrname)
        return String(f"a {self.metaname()}")

    def metaclass(self, metaclass = ''):
        "Find the metaclass."
        if metaclass != '':
            return SObject.setValue(self, 'metaclass', metaclass)
        _metaclass = self._keyName('metaclass')
        if self._has(_metaclass):
            return self._get(_metaclass,nil)
        metaname = self.metaname()
        metaclass = root.metaclassByName(metaname)
        return metaclass

    def runThis(self, thisObj):
        obj = self.asSObj(thisObj)
        execution = self.getContext().newInstance('Execution')
        # execution.localGlobals()
        execution.this(self)
        # self.visit(execution)
        ret = obj.visit(execution)
        return ret

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

    def masquerade(self, sobj=''): return self.getOrSet('masquerade', sobj, nil) # used for @super
    def mutable(self, mutable=''): return self.getOrSet('mutable', mutable, true_) # set mutuable or immatable
    def undefined(self, undefined=''): return self.getOrSet('undefined', undefined, nil) #

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

    def setValue(self, attname, value):
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        sobj = self.asSObj(value)
        return obj._set(obj._keyName(attname), sobj)

    def getOrSet(self, attname, value ='', default =''):  # can't use nil as default
        masq = self._keyName('masquerade')
        obj = self._get(masq, nil) if self._has(masq) else self
        keyname = self._keyName(attname)
        return obj._get(keyname, default) if value == '' else obj._set(keyname, value)

    def _keys(self): return List(self.__dict__.keys())
    def _has(self, keyname): return keyname in self.__dict__    # slightly faster than vars(self)
    def _get(self, keyname, default): return self.__dict__.get(keyname, default)
    def _set(self, keyname, value): self.__dict__[keyname] = value; return self
    def _del(self, keyname):
        if self._has(keyname):
            del self.__dict__[keyname]
        return self


    def _varName(self, keyname):
        "Convert internals keyname to public facing name"
        return keyname if len(keyname) <= 3 or keyname[0:3] != 'ss_' else keyname[3:]

    def _keyName(self, attname):
        """Calculate the internals keyname from public facing attname."""
        return attname if len(attname) > 3 and attname[0:3] == 'ss_' else f'ss_{attname}'

    #### Private helper methods
    def _addHolders(self, holders):
        holders['name'] = Holder().name('name').type('String')
        holders['metaname'] = Holder().name('metaname').type('String')
        holders['mutable'] = Holder().name('mutable').type('True_')
        holders['masquerade'] = Holder().name('masquerade').type('Nil')
        holders['undefined'] = Holder().name('undefined').type('Nil')
        return self

    #### Helper methods
    def __call__(self, *args, **kwargs): return self.createEmpty()
    def createEmpty(self): return type(self)()

    def asSObj(self, pyobj):
        if isinstance(pyobj, SObject): return pyobj
        if isinstance(pyobj, bool): return true_ if pyobj else false_
        if pyobj is None: return nil
        stype = type(pyobj).__name__
        value = pyobj
        if stype in pytypes:
            pClass = pytypes[stype]
            value = pClass(pyobj)
        return value

    def lastDigits(self, n=4): return hex(id(self)).upper()[-n:]
    def isNil(self): return false_
    def notNil(self): return not self.isNil()
    def isEmpty(self): return false_
    def notEmpty(self): return not self.isEmpty()
    def toString(self): return String(self)
    def print(self, suppressed=''):
        if suppressed == '': print(self.info())
        return self

    def info(self, offset=0):
        buffer = io.StringIO()
        # padding = " " * offset
        buffer.write(f"{self.toString()}\n")
        metaclasses = self.inheritedMetas().values()
        for metaclass in metaclasses:
            for holder in metaclass.holders().values():
                name = holder.name()
                if self.hasKey(name):
                    buffer.write(f"  {metaclass.name()}.{name} = {SObject.getValue(self, name)}\n")
        output = buffer.getvalue()
        return String(output)

    def describe(self): return self.name()  # description of this object
    def __repr__(self): return f"{self.describe()}:{self.metaname()} {self.lastDigits()}"

class Holder(SObject):
    """
    Holder to an object and can be used to define an attribute. @obj can be both SObject or Python object.
    """
    def type(self, type=''): return self.getOrSet('type', String(type), 'Nil')     # type hint
    def obj(self, obj=''): return self.getOrSet('obj', obj, nil)                   # optional
    def pyfunc(self, func=''): return self.getOrSet('pyfunc', func, nil)           # optional
    def method(self, method=''): return self.getOrSet('method', method, nil)       # optional
    def instanceType(self, instanceType=''): return self.getOrSet('instanceType', instanceType, true_)
    def classType(self): return self.instanceType(false_)

    def valueFunc(self):
        def value():
            return self.obj()
        return value

    def __call__(self, func):
        self.name(func.__name__).type('Method')
        self.pyfunc(func)
        return self

    def __get__(self, obj, owner = None):  # owner is ignored
        """Implement the descriptor protocol."""
        def getOrSetSObj(sobj, value=None):
            attname = self.name()
            ret = sobj
            if value is None:
                if sobj.hasKey(attname):
                    return sobj.getValue(attname)
                else:   # find default value
                    metaclass = sobj.metaclass()
                    if metaclass.notNil():
                        type = self.type()
                        ret = metaclass.context().metaclassByName(type).createEmpty()
                        if ret == nil or type == 'True_' or type == 'False_':  # don't need to save these default values.
                            return ret
                        value = ret
                    else:
                        logging.warning(f"Found no metaclass for type '{type}' defined by {sobj.metaname()}.{self.name()}")
                        return nil
            if sobj.mutable():
                sobj.setValue(attname, value)
            return ret

        def getOrSet(value=None): return getOrSetSObj(obj, value)

        ret = nil
        method = self.method()
        if method.isNil():
            if self.instanceType():
                if obj is None:
                    return nil
                return getOrSet
            if obj is None:
                obj = self.getContext().metaclassByName(self._metaname(owner)).attrs()
            else:
                obj = obj.metaclass().attrs()
            return getOrSet
        else:
            if obj is not None:
                if self.instanceType():
                    ret = obj.runThis(method)
                else:
                    ret = obj.metaclass().attrs().runThis(method)
                return ret
            if owner is not None:
                if not self.instanceType():
                    metaclass = self.getContext().metaclassByName(self._metaname(owner))
                    obj = metaclass.attrs()
                    ret = obj.runThis(method)
        return ret

    #### Private helper methods
    def _addHolders(self, holders):
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
        # return metaclass(metaclass)
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
    def asNumber(self): return Number(int(self))
    def len(self): return len(self)
    def isEmpty(self): return self.len() == 0
    def visit(self, visitor): return visitor.visitString(self)
    def xxHash(self): return 0 if self.isEmpty() else xxhash.xxh64(self).intdigest()
    def asString(self): return String(f"'{self}'")
    def toString(self): return self

class Nil(SObject):
    """nil is a singleton from this class represents nothing."""
    def __new__(cls):
        global nil
        if not 'nil' in globals():
            nil = super().__new__(cls)
            nil.name('nil')
        return nil

    def __call__(self, *args, **kwargs):
        return nil

    def createEmpty(self): return self
    def isNil(self): return true_

nil = Nil()

class True_(Primitive):
    """SObject true class with singleton true_."""
    def __new__(cls):
        global true_
        if not 'true_' in globals():
            true_ = super().__new__(cls)
        return true_

    def __bool__(self): return True # true_ won't work for 'not', it has to return Python bool
    def createEmpty(self): return self
    def isFalse(self): return false_
    # def isTrue(self): return true_ if self == true_ else false_ # only @true.is_true will return true.
    def isTrue(self): return true_
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
    def describe(self): return "false"

true_ = True_()
false_ = False_()

class List(list, Primitive):
    """SObject list class."""
    def __init__(self, *args):
        list.__init__(self, *args)
        SObject.__init__(self)

    def len(self): return len(self)
    def isEmpty(self): return self.len() == 0
    def notEmpty(self): return not self.isEmpty()
    def head(self): return nil if self.isEmpty() else self[0]
    def append(self, obj): super().append(obj); return self
    def add(self, alist): self.extend(alist); return self
    def includes(self, aList):
        return all(item in self for item in aList)

class Map(dict, Primitive):
    """SObject map class."""
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        dict.__init__(self, *args)
        SObject.__init__(self)

    def len(self): return len(self)
    def isEmpty(self): return self.len() == 0
    def notEmpty(self): return not self.isEmpty()
    def keys(self): return List(super().keys())
    def hasKey(self, name): found = name in self; return found
    def setValue(self, name, value): self[name] = value; return self
    def getValue(self, name, default=nil): ret = self.get(name, default); return ret
    def values(self): return List(super().values())
    def head(self): return nil if self.isEmpty() else self.values().head()

class Metaclass(SObject):
    "Metaclass defines a SObject structure."
    context = Holder().name('context').type('Context')
    package = Holder().name('package').type('Package')
    factory = Holder().name('factory').type('Nil')
    holders = Holder().name('holders').type('Map')
    parentNames = Holder().name('parentNames').type('List')
    attrs = Holder().name('attrs').type('SObject')

    def createEmpty(self):
        """create an empty obj for this metaclass, including Metaclass."""
        factory = self.factory()
        if factory == self:     # only true when self is the metaclass object of MetaClass
            instance = Metaclass()
        else:
            instance = factory.createEmpty()
        instance.metaclass(self)
        return instance

    def importFrom(self, sClass):
        self._importHolders(sClass)
        self._importMetanames(sClass)
        self._createFactory(sClass)
        return self

    def _importHolders(self, sClass):
        "Extracts all attribute definitions from holder objects."
        holders = Map()
        if sClass == SObject:
            SObject()._addHolders(holders)
        elif sClass == Holder:
            Holder()._addHolders(holders)
        else:
            for attname, item in vars(sClass).items():
                if attname.startswith('__'): continue
                if isinstance(item, classmethod) or isinstance(item, staticmethod): continue
                if inspect.isfunction(item):
                    if hasattr(item, 'holder'):
                        holder = item.holder
                        holders[attname] = holder.name(attname)
                        continue
                    # signature = inspect.signature(var)
                    # params = List(signature.parameters.values())
                    # if params.notEmpty() and params.head().name == self.cxtName():
                    #     attrMap[attname] = var
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

    def getHolder(self, name): return self.holders()[name] if name in self.holders() else nil

    def holderByName(self, attrname):
        holders = self.holders()
        if attrname in holders:
            return holders[attrname]
        context = self.context()
        for parentName in self.parentNames():
            parent = context.metaclassByName(parentName)
            holder = parent.holderByName(attrname)
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

class Package(SObject):
    "Package to a set of metaclass loaded from files, or created dynamically."
    context = Holder().name('context').type('Context')
    metaclasses = Holder().name('metaclasses').type('Map')
    path = Holder().name('path').type('Nil')

    #### Metaclass definition import: limited SObject features before initialization.
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
                if holder.type() == 'Method' and holder.pyfunc() != nil:
                    method = self.context().newInstance('Method')
                    holder.method(method)
                    pyfunc = holder.pyfunc()
                    method.takePyFunc(pyfunc)
        return self

    def createMetaclass(self, metaname):
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
                        setValue('context', context)
        metaclasses[metaname] = metaclass
        return metaclass

    def metaclassByName(self, metaname):
        classes = self.getValue('metaclasses', Map())
        ret = classes.get(metaname, nil)
        return ret

    def isEmpty(self):
        if not self.hasKey('metaclasses'): return true_
        return self.metaclasses().isEmpty()

class Context(SObject):
    """
    It provides context for SS methods to function. It provides access to other resources e.g. packages, execution scopes, etc. @root is the root context has maximum access to all resources. Customized context can be created for some executions.
    """
    packages = Holder().name('packages').type('Map')

    def loadPackage(self, pkgname):
        "Load metaclasses from a SObject package."
        pkg = self.newPackage(pkgname)
        if pkg.isEmpty():
            pkg.importSObjects()
            pkg.importMethods()
        return pkg

    def newPackage(self, pkgname):
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
        ret = nil
        for pkg in pkgs.values()[::-1]:
            metaclass = pkg.metaclassByName(metaname)
            if metaclass.notNil():
                ret = metaclass
                break
        return ret

    def newInstance(self, metaname):
        "Create an sobject."
        metaclass = self.metaclassByName(metaname)
        instance = metaclass.createEmpty()
        return instance

    def reset(self):
        self.setValue('packages', Map())  # Reset all packages
        return self

class Scope(SObject):
    """
    Scope object defines the variable lookup.
    """
    def vars(self, vars=''): return self.getOrSet('vars', vars, nil)
    def context(self, context=''): return self.getOrSet('context', context, nil)
        # Can't use Holder for these as Scope overridden major protocols.

    def keys(self):
        # if super().hasKey('masquerade'): return super().keys()
        return self.vars().keys()

    def hasKey(self, attname):
        # if super().hasKey('masquerade'): return super().hasKey(attname)
        return self.vars().hasKey(attname)

    def delValue(self, attname):
        # if super().hasKey('masquerade'): return super().delValue(attname)
        if self.vars().hasKey(attname):
            del self.vars()[attname]
        return self

    def getValue(self, attname, default=nil):
        if super().hasKey('masquerade'): return super().getValue(attname, default)
        return self.vars().getValue(attname, default)

    def setValue(self, attname, value):
        if super().hasKey('masquerade'): return super().setValue(attname, value)
        vars = self.vars()
        if vars.isNil():
            vars = Map()
            self.vars(vars)
        return vars.setValue(attname, value)

class Number(int, Primitive):
    def __new__(cls, number = 0): return super(Number, cls).__new__(cls, number)
    def __init__(self, value = 0): SObject.__init__(self)
    def __floordiv__(self, val): res = super().__floordiv__(val); return res
    def __add__(self, val): res = super().__add__(val); return Number(res)
    def __mul__(self, val): res = super().__mul__(val); return Number(res)
    def __truediv__(self, val): res = super().__truediv__(val); return Number(res)
    def __eq__(self, val): res = super().__eq__(val); return res
    def __gt__(self, val): res = super().__gt__(val); return res
    def __lt__(self, val): res = super().__lt__(val); return res
    def __mod__(self, val): res = super().__mod__(val); return Number(res)
    def __sub__(self, val): res = super().__sub__(val);  return Number(res)
    def __hash__(self): return super().__hash__()
    def asObj(self, pyobj): return Number(pyobj)
    def toString(self): return String(self)

class Float(float, Primitive):
    def __new__(cls, number = 0): return super(Float, cls).__new__(cls, number)
    def __init__(self, value = 0): SObject.__init__(self)
    def __floordiv__(self, val): res = super().__floordiv__(val); return res
    def __add__(self, val): res = super().__add__(val); return Float(res)
    def __mul__(self, val): res = super().__mul__(val); return Float(res)
    def __truediv__(self, val): res = super().__truediv__(val); return Float(res)
    def __eq__(self, val): res = super().__eq__(val); return res
    def __gt__(self, val): res = super().__gt__(val); return res
    def __lt__(self, val): res = super().__lt__(val); return res
    def __mod__(self, val): res = super().__mod__(val); return Float(res)
    def __sub__(self, val): res = super().__sub__(val); return Float(res)
    def __hash__(self): return super().__hash__()
    def asObj(self, pyobj): return Float(pyobj)
    def toString(self): return String(self)

pytypes = Map(str = String, int = Number, float = Float, dict = Map, list = List)

root = Context().name('root').reset()
root.loadPackage('smallscript') # This global root context is the first Context object got created.