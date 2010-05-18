#!/usr/bin/python

import sys
from EntityTest import EntityTest

class ContactTest(EntityTest):

  uniqueid = 'glue2contactid'

  mandatoryAttributes = ['glue2contactid', 'glue2contactdetail',
    'glue2contacttype']

  singleValueAttributes = ['glue2locationid', 'glue2contactdetail', 
    'glue2contacttype']
  singleValueAttributes.extend(getattr(EntityTest, 'singleValueAttributes'))

  relations = {
    'glue2contactserviceforeignkey': 'glue2serviceid',
    'glue2contactdomainforeignkey': 'glue2domainid'}
  relations.update(getattr(EntityTest, 'relations'))

  dataTypes = {
    'glue2contactid': 'URI',
    'glue2contactdetail': 'URI',
    'glue2contacttype': 'ContactType'}
  dataTypes.update(getattr(EntityTest, 'dataTypes'))

if __name__ == "__main__":
  sys.exit(ContactTest().main('glue2contact'))

