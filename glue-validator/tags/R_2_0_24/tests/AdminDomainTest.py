#!/usr/bin/python

import unittest
import DomainTest
import glue2.EntryTest
EntryTest = glue2.EntryTest.EntryTest

class AdminDomainTest(unittest.TestCase):
        
    def setUp(self):
        self.good_entry = {
            'dn' : ['GLUE2DomainId=site:mysite.com,o=GLUE'],
            'objectClass' : ['GLUE2Domain', 'GLUE2AdminDomain'], 
            'GLUE2DomainID' : ['site://mysite.com'],
            'GLUE2DomainDescription' : ['Example Grid Site'],
            'GLUE2DomainWWW' : ['http://mysite.com'],
            'GLUE2AdminDomainDistributed' : ['FALSE'],
            'GLUE2AdminDomainOwner' : ['Some organization'],
            'GLUE2AdminDomainAdminDomainForeignKey' : ['grid:mygrid.org'],
            }
          
    def test_good_entry(self):
        '''Test a good entry.'''
        entry = self.good_entry
        suite = unittest.TestSuite()
        test_names = unittest.TestLoader().getTestCaseNames(EntryTest)
        for test_name in test_names:
            suite.addTest(EntryTest(test_name, entry))
        self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(AdminDomainTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

