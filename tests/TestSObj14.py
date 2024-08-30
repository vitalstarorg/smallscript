from smallscript.SObject import SObject, Holder

class TestSObj14(SObject):
    ss_metas = 'TestSObj15'
    attr11 = Holder().name('attr11').type('String')
    sobj11 = Holder().name('sobj11').type('TestSObj11')
    cattr12 = Holder().name('cattr12').type('String').asClassType()
    cattr13 = Holder().name('cattr13').type('String').asClassType()

    @Holder().asClassType()
    def metaInit(scope):
        # self is attrs of the metaclass TestSObj15
        self = scope['self']
        # attrs is SObject and works like Map without needing to define Holder.
        # Having Holder helps access class attribute in Python.
        ret = self.cattr13("value from metaInit")   # access through holder
        self['cattr14'] = "value from metaInit"     # don't have to defined by holder
        return self

    @Holder()
    def method14(scope, m14, arg2):
        return m14 + arg2

    @Holder().asClassType()
    def cmethod15(scope, m15, arg2):
        return m15 * arg2

    @Holder()
    def method16(scope, m16, arg2):
        self = scope['self']
        cattr12 = self.cattr12().asNumber()
        attr11 = self['attr11'].asNumber()
        return cattr12 + attr11 + m16 + arg2

    @Holder().asClassType()
    def cmethod17(scope, m17, arg2):
        self = scope['self']
        ret = self['cattr12'].asNumber()
        return ret + m17 * arg2

    @Holder()
    def method18(scope):
        sobj = SObject().setValue('attr18_1', 'value18.1')
        return sobj

    @Holder()
    def first__last__(scope, first, last):
        self = scope['self']
        self['first'] = first
        self['last'] = last
        return f"{first}, {last}"

    def firstname(self, first, last):
        return f"{first}, {last} ({self.attr11()})"
