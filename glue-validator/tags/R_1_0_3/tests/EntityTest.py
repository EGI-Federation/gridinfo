#!/usr/bin/python

import re
import unittest
import glue2.EntryTest

EntryTest = glue2.EntryTest.EntryTest

class EntityTest(unittest.TestCase):
        
    def setUp(self):
        self.good_entry = {
            'dn' : ['EntityId=test,o=GLUE2'],
            'objectClass' : ['GLUE2Entity'],
            'GLUE2EntityId' : ['test'],
            }
          
    def test_good_entryTest(self):
        '''Test a good entry.'''
        entry = self.good_entry
        suite = unittest.TestSuite()
        test_names = unittest.TestLoader().getTestCaseNames(EntryTest)
        for test_name in test_names:
            suite.addTest(EntryTest(test_name, entry))
        self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())

def test_bad_object_class(self):
    '''Test a bad object class'''
    entry = self.good_entry
    entry['objectClass'] = ['BadObject']
    suite = unittest.TestSuite()
    test_names = unittest.TestLoader().getTestCaseNames(EntryTest)
    for test_name in test_names:
        suite.addTest(EntryTest(test_name, entry))
    self.assertFalse(unittest.TextTestRunner().run(suite).wasSuccessful())
    self.assertEqual(len(unittest.TextTestRunner().run(suite).failures),1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(EntityTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

