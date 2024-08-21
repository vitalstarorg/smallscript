# SmallScript - WIP


We are looking for a small script capable of running on top of high level languages e.g. Python, Java, C++ and etc to manipulate high level functions provided by any of these platforms. This script provides a self-contained and platform independent environment to develop common reusable logics that can be executed in different platforms & hosts.


### Motivation
We come across libraries using different architecture and designs. Since they are designed with a specific use case in mind, when we combine several of these libraries, we always need to develop additional adaptors or abstraction layers to hide their implementation or design details to fit them all into one homogenous framework.
 
SmallScript comes to help to provide such a flexible framework to interface or encapsulate a full range of libraries developed with different use cases in mind.


Another side benefit for having a small script like this is to allow us to experiment with different language schemes to explore different interfaces to different libraries. Since the abstract syntax tree AST, intermediate representation IR,  transpiled code and bytecodes are available for deeper examination. These are important artifacts for language research and diagnostics.


### General Design Guideline
- Minimal and expressive language
- Object-oriented language in favor of knowledge representation.
- Late binding and dynamic typing.
- Platform and host language independent


Amongst all languages we used in the past, we are in favor of deriving SmallScript from Smalltalk as it is an elegant language that provides pure object-oriented support. Another attractive benefit is that SmallScript can be written by SmallScript itself. In the far-reaching future, SmallScript can be run by itself without needing an OS as SmallScript can define an OS for it to run. Even though it may not be our near term objective, having this long term vision to guide the development will provide wider possibilities how we want SmallScript to be.

## Install
```sh
pip install smallscript
```

# Sample Use Cases
## Basic SObject use cases  
### SObject attributes are created on demand.
```python
from smallscript.SObject import *

class TestSObj1(SObject):
    attr11 = Holder().name('attr11').type('String')
    attr12 = Holder().name('attr12').type('Nil')
    attr13 = Holder().name('attr13').type('True_')
    attr14 = Holder().name('attr14').type('False_')

sobj = TestSObj1().name('sobj').attr11('hello')
    # Builder pattern: setters always return @self
```
### Every object is SObject, including nil
```python
attr = sobj.attr12()
assert attr == nil  # nil is an sobject

# So we can do this, and make code flows nicely.
if sobj.attr12().isNil():
  sobj.attr12('Some value')
    # BTW type() provides a hint and default value. So we can set any object into it, including non-SObject.

sobj.attr12(print) 
    # 'print' is a python build-in function.
```
### Metaclass fully describes sobject class structure.

```python
metaclass = sobj.metaclass()
check = sobj.metaclass().holders().keys().includes(['name', 'metaname'])
    # Beauty of using builder pattern.
```
### Load a package by root context
```python
pkg = root.loadPackage('tests.tdd_v0_0')
    # @root is the first context contains smallscript core package and metaclasses.
tobj1 = TestSObj1()
meta1 = tobj1.metaclass()
    # After loadPackage(), TestSObj1 will be imported.
```
### Context can be separated

```python
cxt = Context().name('test01_tdd')
cxt.loadPackage('smallscript')  # need to load this first.
pkg = cxt.getOrNewPackage('tmppkg')  # create a temporary package on memory
```
### Dynamically create a new class
```python
# Create new metaclass with two attributes.
newMeta = pkg.createMetaclass('NewMeta')
newMeta.parentNames(['Metaclass'])
newMeta.factory(SObject())
holders = newMeta.holders()
holders['attr11'] = Holder().name('attr11').type('String')
holders['attr12'] = Holder().name('attr12').type('List')

# Create a new instance. Real obj4 type is Python SObject but behaves like a new type.
obj4 = cxt.newInstance('NewMeta').name('obj4')
```

## Basic Closure use cases
### Instance and Class methods  
```python
class TestSObj14(SObject):
    ss_metas = "TestSObj15"
        # ss_metas defines the Metaclass name; otherwise, class name would be used.
    attr11 = Holder().name('attr11').type('String')
        # Instance attribute
    cattr12 = Holder().name('cattr12').type('String').asClassType()
        # Class attribute

    # Make this method using SObject protocol. The first argument is @scope, not @self.
    @Holder()
    def method16(scope, arg1, arg2):
        self = scope['self']
        cattr12 = self.cattr12().asNumber()
        attr11 = self['attr11'].asNumber()
        return cattr12 + attr11 + arg1 + arg2

    # Make this a class method using SObject protocol.
    @Holder().asClassType()
    def cmethod17(scope, arg1, arg2):
        self = scope['self']
        ret = self['cattr12'].asNumber()
        return ret + arg1 * arg2

    # @self can be retrieved from @scope. @scope is the window to both local and global variables.
    @Holder()
    def first__last__(scope, first, last):
        self = scope['self']
        self['first'] = first
        self['last'] = last
        return f"{first}, {last}"

pkg = rootContext.loadPackage('tests')
tobj = TestSObj14()

tobj.metaclass().name()         # 'TestSObj15'
tobj.cattr12('200')             # assign cattr12 class attribute
tobj.cmethod17(2,3)             # 206
tobj.attr11('100')              # assign attr11 instance attribute
tobj.method16(2, 3)             # 305
```
### Dynamic Invocation through SObject system
```python
meta = rootContext.metaclassByName('TestSObj15')
tobj = SObject().metaclass(meta)        # tobj behaves like TestSObj15 through generic SObject.

tobj.metaclass().name()         # 'TestSObj15'
tobj.cattr12('200')             # assign cattr12 class attribute
tobj.cmethod17(2,3)             # 206
tobj.attr11('100')              # assign attr11 instance attribute
tobj.method16(2, 3)             # 305
```

### Fully Dynamic Creation using SObject system
```python
# Create new metaclass with two attributes.
pkg = rootContext.getOrNewPackage('tmppkg')  # create a temporary package
newMeta = pkg.createMetaclass('NewMeta')
newMeta.parentNames(['Metaclass'])
newMeta.factory(SObject())
holders = newMeta.holders()
holders['attr11'] = Holder().name('attr11').type('String')
holders['cattr12'] = Holder().name('cattr12').type('String').asClassType()

# Define instance and class method using SmallScript
method16 = Method().interpret(":arg1 :arg2 | self cattr12 asNumber + self attr11 asNumber + arg1 + arg2")
holders['method16'] = Holder().name('method16').type('Method').method(method16)
cmethod17 = Method().interpret(":arg1 :arg2 | arg1 * arg2 + self cattr12 asNumber")
holders['cmethod17'] = Holder().name('cmethod17').type('Method').method(cmethod17)

tobj = rootContext.newInstance('NewMeta').name('tobj')
tobj.metaclass().name()         # 'NewMeta'
tobj.cattr12('200')             # assign cattr12 class attribute
tobj.cmethod17(2, 3)            # 206
tobj.attr11('100')              # assign attr11 instance attribute
tobj.method16(2, 3)             # 305
```

### Fully Dynamic Creation using SmallScript
This is a critical milestone. From this point on, we have all necessary core functions to develop further libraries using SmallScript completely.

SObject is a complete object system by itself. It is an interface layer between Python and SmallScript which follows Python and SmallScript protocol. In theory, SObject would very much behave like SmallScript in Python language.

All objects are SObject including primitives. **nil** is SObject for **None** in Python, **true_** for **True**, **false_** for **False**, **List** for **list**, **Map** for **dict**, **Number** for both **int** and **float**.

Currently SmallScript is running in interpreter mode. SmallScript will be transpiled to Python in next release than SmallScript will be running close to native speed. 

```python
smallscript = """
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
                | addMethod: #method14 method: [:arg1 :arg2 | arg1 + arg2]
                | addMethod: #cmethod15 method: [:arg1 :arg2 | arg1 * arg2] classType: true
                | addMethod: #method16 method: [:arg1 :arg2 | self cattr12 asNumber + self attr11 asNumber + arg1 + arg2]
                | addMethod: #cmethod17 method: [:arg1 :arg2 | arg1 * arg2 + self cattr12 asNumber] classType: true
"""
scope = rootContext.createScope()
method = Method().interpret(ss)
meta = method(scope)

tobj = rootContext.newInstance('AnotherMeta').name('tobj')
tobj.metaname()                 # 'AnotherMeta'
tobj.cattr12('200')             # assign cattr12 class attribute
tobj.cmethod17(2, 3)            # 206
tobj.attr11('100')              # assign attr11 instance attribute
tobj.method16(2, 3)             # 305
```

# Potential Roadmap
- Implement SmallScript on C/C++
 - This will open the door to access many useful binary libraries and access these functions on demand.
- Implement SmallScript on JVM
 - Similar to C/C++

# Release Note
### v0.1.0 SObject with Closure
- ref: tests/tdd_v0_1/* for details
- Enhance SObject with class attributes.
- Supports both instance and class methods using SObject protocol, not using Python.
- Implemented initial elements of SmallScript.
### v0.0.1 SObject
- ref: tests/tdd_v0_0/* for details
- Provide basic object encapsulation and behavioral inheritance with trait type of multiple inheritance.
- Everything is an SObject including nil.
- Can be mixed with Python code seamlessly.
- Install this basic SObject without needing other features. do this.
```sh
pip install git+https://github.com/vitalstarorg/smallscript@v0.0.1

# or

pip install git+https://github.com/vitalstarorg/smallscript@sobject
```

