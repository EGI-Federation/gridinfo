import re
import unittest

class WLCGTest(unittest.TestCase):

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

    def test_GlueCEPolicyMaxCPUTime_default (self):
        message = "ERROR: Entry %s contains default value of 999999999 for GlueCEPolicyMaxCPUTime" % (self.dn)
        if 'GlueCEPolicyMaxCPUTime' in self.entry:
        	self.assertEqual(self.entry['GlueCEPolicyMaxCPUTime'],999999999, message)


