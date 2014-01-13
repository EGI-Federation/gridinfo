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

    def test_GLUE2StorageShareCapacityTotalSize_OK (self):
        total = 0
        share_stats = ""
        value = True
        for share in ['GLUE2StorageShareCapacityFreeSize',\
                      'GLUE2StorageShareCapacityUsedSize',\
                      'GLUE2StorageShareCapacityReservedSize']:
            if share in self.entry:
                if (share == 'GLUE2StorageShareCapacityReservedSize') and \
                   (self.entry['GLUE2StorageShareCapacityReservedSize'][0] == self.value[0]):
                       share_stats = share_stats + " %s=%s (Not added)" % (share,self.entry[share][0])
                else:
                       total = total + int(self.entry[share][0])
                       share_stats = share_stats + " %s=%s" % (share,self.entry[share][0])
            else:
                share_stats = share_stats + " %s=Not published" % (share)
        low = int(self.value[0]) - (int(self.value[0]) * 0.005)
        low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.005)
        high = high + 1
        share_stats = share_stats + "; %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("ERROR","E018",self.dn,\
                  "GLUE2StorageShareCapacityTotalSize",self.value[0],share_stats)
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )

    def test_GLUE2StorageServiceCapacityTotalSize_OK (self):
        total = 0
        cap_stats = ""
        value = True
        for cap in ['GLUE2StorageServiceCapacityFreeSize',
                    'GLUE2StorageServiceCapacityUsedSize',
                    'GLUE2StorageServiceCapacityReservedSize']:
            if cap in self.entry:
                total = total + int(self.entry[cap][0])
                cap_stats = cap_stats + " %s=%s" % (cap,self.entry[cap][0])
            else:
                cap_stats = cap_stats + " %s=Not published" % (cap)
        low = int(self.value[0]) - (int(self.value[0]) * 0.005)
        low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.005)
        high = high + 1
        cap_stats = cap_stats + " %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("ERROR","E014",self.dn,\
                  "GLUE2StorageServiceCapacityTotalSize",self.value[0],cap_stats)
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )

