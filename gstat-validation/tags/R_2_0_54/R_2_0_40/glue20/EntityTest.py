#!/usr/bin/python

import sys
from GLUE20UnitTest import GLUE20UnitTest

class EntityTest(GLUE20UnitTest):

  uniqueid = ''

  mandatoryAttributes= []

  singleValueAttributes = ['glue2entitycreationtime', 'glue2entityvalidity', 
    'glue2entityname']

  relations = {'glue2entityextensionforeignkey': 'glue2extensionid'}

  dataTypes = {
    'glue2entitycreationtime': 'DateTime_t',
    'glue2entityvalidity': 'UInt64',
    'glue2entityname': 'String'}

if __name__ == "__main__":
  sys.exit(EntityTest().main('glue2entity'))

