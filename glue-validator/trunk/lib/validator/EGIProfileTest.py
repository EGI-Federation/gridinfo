import re
import unittest

class EGIProfileTest(unittest.TestCase):

    def __init__(self, test_name, entry, value, test_class):
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
        self.value = value

    def test_GLUE2EntityValidity_default (self):
        if 'GLUE2EntityCreationTime' not in self.entry:
            status = False
        else:
            status = True
        message = "ERROR: %s should not publish GLUE2EntityValidity since GLUE2EntityCreationTime is not published" %\
                   (self.dn)
        self.assertTrue(status, message)
              
