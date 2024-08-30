// Create metaclass
meta := scope getValue: 'package'
            | createMetaclass: #AnotherMeta
                | parentNames: #(#SObject)

                // Create two instance attributes and one class attribute.
                | addAttr: #attr11 type: #String
                | addAttr: #attr12 type: #List
                | addAttr: #cattr12 type: #String classType: true

                // Create two instance methods and two class methods.
                | addMethod: #method14
                    method: [:m14 :arg2 | m14 + arg2]
                | addMethod: #cmethod15
                    method: [:m15 :arg2 | m15 * arg2]
                    classType: true
                | addMethod: #method16
                    method: [:m16 :arg2 | self cattr12 asNumber + self attr11 asNumber + m16 + arg2]
                | addMethod: #cmethod17
                    method: [:m17 :arg2 | self cattr12 asNumber + m17 * arg2]
                    classType: true