#!/usr/bin/python

import unittest
import EntityTest

class DomainTest(EntityTest.EntityTest):

    def __init__(self, test_name, entry):
        EntityTest.EntityTest.__init__(self, test_name, entry)

        self.SINGLE_VALUED_ATTRIBUTES.extend([ 
                'GLUE2DomainId',
                'GLUE2DomainDescription',
                ])

        self.MANDATORY_ATTRIBUTES.extend([
                'GLUE2DomainId',
                ])

        self.DATA_TYPES.update({
        'GLUE2DomainId' : 'uri', 
        'GLUE2DomainDescription' : 'string',
        'GLUE2DomainWWW' : 'url',
        })

if __name__ == '__main__':

    class DomainTestTest(unittest.TestCase):
        
        def setUp(self):
            self.good_entry = {
                'dn' : ['GLUE2DomainId=mysite.com,o=GLUE'],
                'objectClass' : ['GLUE2Domain', 'GLUE2AdminDomain'], 
                'GLUE2DomainId' : ['site://mysite.com'],
                'GLUE2DomainDescription' : ['Example Grid Site'],
                'GLUE2DomainWWW' : ['http://mysite.com'],
                }
          
        def test_good_entry(self):
            '''Test a good entry.'''
            entry = self.good_entry
            suite = unittest.TestSuite()
            test_names = unittest.TestLoader().getTestCaseNames(DomainTest)
            for test_name in test_names:
                suite.addTest(DomainTest(test_name, entry))
            self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())

    suite = unittest.TestLoader().loadTestsFromTestCase(DomainTestTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

