#!/usr/bin/python

import re
import unittest

class EntityTest(unittest.TestCase):

    SINGLE_VALUED_ATTRIBUTES = [ 
        'dn',
        ]

    MANDATORY_ATTRIBUTES = [
        'dn',
        'objectClass',
        ]

    DATA_TYPES ={
        'objectClass' : 'object_class_t', 
        'dn' : 'dn', 
        'GLUE2EntityId' :'string',
        }

    def __init__(self, test_name, entry):
        unittest.TestCase.__init__(self, test_name)
        self.entry = entry
        if 'dn' in entry:
            self.dn = entry['dn'][0]
        else:
            self.dn = None


    def test_mandatory_attributes(self):
        """Verifying the existence of mandatory attributes."""
        for attribute in self.MANDATORY_ATTRIBUTES:
            message = "The mandatory attribute %s is not present in %s" % (attribute, self.dn)
            self.assertTrue(attribute in self.entry, message)
        
    def test_single_valued(self):
        """Verifying single-valued attributes only have one value."""
        for attribute in self.SINGLE_VALUED_ATTRIBUTES:
            message = "The single value attribute %s has more than one value in %s" % (attribute, self.dn)
            if attribute in self.entry:
                self.assertEqual(len(self.entry[attribute]), 1, message)

    def test_data_types(self):
        """Validating data types."""
        for attribute in self.entry:
            for value in self.entry[attribute]:
                data_type = self.DATA_TYPES[attribute]
                check = getattr(self, 'is_' + data_type)
                message = "The field %s with value %s does not follow the type %s in %s" % (attribute, value, data_type, self.dn)
                self.assertTrue(check(value), message)


    def is_dn(self,value):
        return True

    def is_object_class_t(self, value):
        object_classes = [
            'GLUE2Entity',
            'GLUE2Domain',
            'GLUE2AdminDomain',
            'GLUE2Location',
            'GLUE2Contact',
            'GLUE2Service',
            'GLUE2Endpoint',
            'GLUE2Policy',
            'GLUE2AccessPolicy',
            'GLUE2ComputingService',
            'GLUE2Manager',
            'GLUE2ComputingManager',
            'GLUE2ComputingEndpoint',
            'GLUE2Share',
            'GLUE2ComputingShare',
            'GLUE2MappingPolicy',
            'GLUE2Resource',
            'GLUE2ExecutionEnvironment',
            'GLUE2Benchmark',
            'GLUE2ApplicationEnvironment',
            'GLUE2ToStorageService',
            'GLUE2StorageManager',
            'GLUE2StorageServiceCapacity',
            'GLUE2StorageAccessProtocol',
            'GLUE2StorageEndpoint',
            'GLUE2StorageShare',
            'GLUE2StorageShareCapacity',
            'GLUE2DataStore',
            'GLUE2ToComputingService',
            ]

        if value in object_classes:
            return True
        else:
            return False

    def is_string(self, value):
        if value == '':
            return False
        else:
            return True

    def is_extended_boolean_t(self, value):
        value = value.lower()
        if value in ['false', 'true', 'undefined']:
            return True
        else:
            return False
        
    def is_uri(self, value):
    # RFC 3986: http://www.ietf.org/rfc/rfc3986.txt
    # Check URL (subtype of URI)
        uri = "^[a-zA-Z][a-zA-Z0-9+-.]*://[a-zA-Z0-9_.]+(:[0-9]+)*(/[a-zA-Z0-9_]*)*(\?[a-zA-Z0-9+-:@?./]+)?(#[a-zA-Z0-9+-:#@?./]+)?$"
        if re.match(uri, value):
            return True
        else:
            # Check other URIs
            uri = "^[a-zA-Z][a-zA-Z0-9+-.@:]*:[a-zA-Z0-9+-.@:]*$"
            if re.match(uri, value):
                return True
            else:
                return False

    def is_url(self, value):
     # RFC 1738: http://www.ietf.org/rfc/rfc1738.txt
     # Protocols accepted: http|ftp|https|ftps|sftp
     # Protocols rejected on purpose: gopher|news|nntp|telnet|mailto|file|etc.
     url = "(((http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&amp;%_\./-~-]*)?"
     if re.match(url, value):
         return 1
     else:
         return 0

     def is_real_32(self, value):
         # IEE 754-2008: http://en.wikipedia.org/wiki/IEEE_754-2008
         # I just check it is a floating point number
         floatingpoint = "[0-9]+(.[0-9]+)*"
         if re.match(floatingpoint, value):
             return True
         else:
             return False

    def is_contact_type(self, value):
        value = value.lower()
        if value in ['general', 'security', 'sysadmin', 'usersupport']:
            return True
        else:
            return False

    def is_u_int_64(self, value):
        # Check http://en.wikipedia.org/wiki/Integer_(computer_science)
        if re.match("^[0-9]+$", value):
            if long(value) <= 18446744073709551615L:
                return True
            return False

    def is_datetime_t(self, value):
        # Check http://www.w3.org/TR/xmlschema-2/#dateTime
        dateTime = "^-?[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])T([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z?$"
        if re.match(dateTime, value):
            return True
        return False

    def is_email(self, email):
        if len(email) > 7:
            if re.match("mailto:[ ]*.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return True
            return False

if __name__ == '__main__':

    class EntityTestTest(unittest.TestCase):
        
        def setUp(self):
            self.good_entry = {
                'dn' : ['EntityId=test,o=GLUE2]'],
                'objectClass' : ['GLUE2Entity'],
                'GLUE2EntityId' : ['test'],
                }
          
        def test_good_entryTest(self):
            '''Test a good entry.'''
            entry = self.good_entry
            suite = unittest.TestSuite()
            test_names = unittest.TestLoader().getTestCaseNames(EntityTest)
            for test_name in test_names:
                suite.addTest(EntityTest(test_name, entry))
            self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())
        def test_bad_object_class(self):
            '''Test a bad object class'''
            entry = self.good_entry
            entry['objectClass'] = ['BadObject']
            suite = unittest.TestSuite()
            test_names = unittest.TestLoader().getTestCaseNames(EntityTest)
            for test_name in test_names:
                suite.addTest(EntityTest(test_name, entry))
            self.assertFalse(unittest.TextTestRunner().run(suite).wasSuccessful())
            self.assertEqual(len(unittest.TextTestRunner().run(suite).failures),1)

    suite = unittest.TestLoader().loadTestsFromTestCase(EntityTestTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

