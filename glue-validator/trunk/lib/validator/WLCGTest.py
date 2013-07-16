import re
import unittest
import datetime
import time
import validator.utils

#----------------------------------------------------------------------------------------------
class WLCGTest(unittest.TestCase):

    def __init__(self, test_name, entry, value, test_class):

        unittest.TestCase.__init__(self, test_name)
        self.entry = entry
        if 'dn' in entry:
            self.dn = entry['dn'][0]
        else:
            self.dn = None

        self.types = __import__('%s.types' %(test_class,)).types

        self.value = value

#----------------------------------------------------------------------------------------------

    def test_GLUE2ComputingShareMaxCPUTime_OK (self):
        message = validator.utils.message_generator("INFO","I029",self.dn,"GLUE2ComputingShareMaxCPUTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

