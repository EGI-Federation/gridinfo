#!/usr/bin/python

import sys
from EntityTest import EntityTest

class LocationTest(EntityTest):

  uniqueid = 'glue2locationid'

  mandatoryAttributes = ['glue2locationid']

  singleValueAttributes = ['glue2locationid', 'glue2locationaddress', 
    'glue2locationplace', 'glue2locationcountry', 'glue2locationpostcode',
    'glue2locationlatitude', 'glue2locationlongitude']
  singleValueAttributes.extend(getattr(EntityTest, 'singleValueAttributes'))

  relations = {
    'glue2locationserviceforeignkey': 'glue2serviceid',
    'glue2locationdomainforeignkey': 'glue2domainid'}
  relations.update(getattr(EntityTest, 'relations'))

  dataTypes = {
    'glue2locationid': 'URI',
    'glue2locationaddress': 'String',
    'glue2locationplace': 'String',
    'glue2locationcountry': 'String',
    'glue2locationpostcode': 'String',
    'glue2locationlatitude': 'Real32',
    'glue2locationlongitude': 'Real32'}
  dataTypes.update(getattr(EntityTest, 'dataTypes'))

if __name__ == "__main__":
  sys.exit(LocationTest().main('glue2location'))

