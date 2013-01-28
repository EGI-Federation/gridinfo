import re
import unittest

class EGIProfileTest(unittest.TestCase):

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

        self.schema = __import__('%s.data' %(test_class,)).data.schema 
        self.types = __import__('%s.types' %(test_class,)).types

    def test_mandatory_attributes(self):
        """Verifying the existence of mandatory attributes."""
        for obj in self.objects:
            if obj in self.schema:
                for attribute in self.schema[obj]:
                    if self.schema[obj][attribute][2] == 'Mandatory':
                        message = "WARNING: The mandatory attribute %s is not present in %s" % (attribute, self.dn)
                        self.assertTrue(attribute in self.entry, message)
                    elif self.schema[obj][attribute][2] == 'Recommended':
                        message = "INFO: The recommended attribute %s is not present in %s" % (attribute, self.dn)
                        self.assertTrue(attribute in self.entry, message)
      

