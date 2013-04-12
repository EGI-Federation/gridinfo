import re
import unittest

class EntryTest(unittest.TestCase):

    def __init__(self, test_name, entry, test_class):
        unittest.TestCase.__init__(self, test_name)
        self.entry = entry
        if 'dn' in entry:
            self.dn = entry['dn'][0]
        else:
            self.dn = None

        if 'objectClass' in entry:
            self.objects = entry['objectClass']
        else:
            self.objects = []

        self.test_class = test_class 
        self.schema = __import__('%s.data' %(test_class,)).data.schema 
        self.types = __import__('%s.types' %(test_class,)).types

    def test_object_class(self):
        '''Verifying the object class'''
        message = "ERROR: The entry %s does not contain any object class" % (self.dn)
        self.assertTrue('objectClass' in self.entry , message)
        if 'objectClass' in self.entry:
            status = True
            message = ""
            for obj in self.entry['objectClass']:
                if not self.types.is_ObjectClass(obj):
                    message = message + ("\n ERROR: The object class %s in %s is not valid") % (obj, self.dn)
                    status = False
            self.assertTrue(status, message)

    def test_mandatory_attributes(self):
        """Verifying the existence of mandatory attributes."""
        status = True
        message = ""
        for obj in self.objects:
            if obj in self.schema:
                for attribute in self.schema[obj]:
                    if attribute == 'GLUE2GroupID' and attribute not in self.entry and 'GLUE2GroupName' not in self.entry:
                        message = message + ("\n WARNING: The mandatory attribute %s "
                                             "is not present in %s") % (attribute, self.dn)
                        status = False
                    elif self.test_class != 'egi-glue2' and self.schema[obj][attribute][2] and attribute not in self.entry:
                        message = message + ("\n The mandatory attribute %s "
                                             "is not present in %s") % (attribute, self.dn)
                        status = False
                            
                    else:
                        if self.schema[obj][attribute][2] == 'Mandatory' and attribute not in self.entry:
                            message = message + ("\n WARNING: The mandatory attribute %s "
                                                 "is not present in %s") % (attribute, self.dn)
                            status = False 
                        elif self.schema[obj][attribute][2] == 'Recommended' and attribute not in self.entry:
                            message = message + ("\n INFO: The recommended attribute %s "
                                                 "is not present in %s") % (attribute, self.dn)
                            status = False
                        elif self.schema[obj][attribute][2] == 'Undesirable' and attribute in self.entry:
                            message = message + ("\n WARNING: The undesirable attribute %s "
                                                 "is present in %s") % (attribute, self.dn)
                            status = False
        self.assertTrue(status, message) 

    def test_single_valued(self):
        """Verifying single-valued attributes only have one value."""
        status = True
        message = ""
        for obj in self.objects:
            if obj in self.schema:
                for attribute in self.schema[obj]:
                    if self.schema[obj][attribute][1] and attribute in self.entry and len(self.entry[attribute]) > 1:
                        message = message + ("\n WARNING: The single value attribute %s "
                                             "has more than one value in %s") % (attribute, self.dn)
                        status = False
        self.assertTrue(status, message)

    def test_data_types(self):
        """Validating data types."""
        status = True
        message = ""
        for obj in self.objects:
            if obj in self.schema:
                for attribute in self.entry:
                    if attribute in self.schema[obj]:
                        data_type = self.schema[obj][attribute][0]
                        for value in self.entry[attribute]:
                            check = getattr(self.types, 'is_' + data_type)
                            if not check(value):  
                                message = message + ("\n WARNING: The field %s with value '%s' "
                                                     "does not follow the type %s in %s") % \
                                                    (attribute, value, data_type, self.dn)
                                status = False
        self.assertTrue(status, message)

    def test_empty_attributes(self):
        """Verifying that attributes are not empty."""
        status = True
        message = ""
        for obj in self.objects:
            if obj in self.schema:
                for attribute in self.entry:
                    if attribute in self.schema[obj]:
	                    for value in self.entry[attribute]:
                                if value == "":
                      	    	    message = message + ("\n WARNING: The attribute %s in %s is empty") % \
                                                        (attribute, self.dn)
        self.assertTrue(status, message)

