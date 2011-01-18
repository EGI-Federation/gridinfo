
OBJECTS = [ 
    'admindomain',
    ]

for object_class in OBJECTS:
    __import__('glue2.%s' % (object_class,))

