#!/usr/bin/python

import unittest
import DomainTest

class AdminDomainTest(DomainTest.DomainTest):

    def __init__(self, test_name, entry):
        DomainTest.DomainTest.__init__(self, test_name, entry)

        self.SINGLE_VALUED_ATTRIBUTES.extend([ 
                'GLUE2AdminDomainDistributed',
                ])

        self.DATA_TYPES.update({
        'GLUE2AdminDomainDistributed' : 'extended_boolean_t', 
        'GLUE2AdminDomainOwner' : 'string',
        'GLUE2AdminDomainAdminDomainForeignKey' : 'string',
        })

if __name__ == '__main__':

    class AdminDomainTestTest(unittest.TestCase):
        
        def setUp(self):
            self.good_entry = {
                'dn' : ['GLUE2DomainId=mysite.com,o=GLUE'],
                'objectClass' : ['GLUE2Domain', 'GLUE2AdminDomain'], 
                'GLUE2DomainId' : ['site://mysite.com'],
                'GLUE2DomainDescription' : ['Example Grid Site'],
                'GLUE2DomainWWW' : ['http://mysite.com'],
                'GLUE2AdminDomainDistributed' : ['FALSE'],
                'GLUE2AdminDomainOwner' : ['Some organization'],
                'GLUE2AdminDomainAdminDomainForeignKey' : ['mygrid.org'],
                }
          
        def test_good_entry(self):
            '''Test a good entry.'''
            entry = self.good_entry
            suite = unittest.TestSuite()
            test_names = unittest.TestLoader().getTestCaseNames(AdminDomainTest)
            for test_name in test_names:
                suite.addTest(AdminDomainTest(test_name, entry))
            self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())

    suite = unittest.TestLoader().loadTestsFromTestCase(AdminDomainTestTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

