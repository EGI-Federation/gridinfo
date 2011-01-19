
OBJECTS = [ 
    'Entity',
    'Domain',
    'AdminDomain',
    ]

for object_class in OBJECTS:
    __import__('glue2.%sTest' % (object_class,))

