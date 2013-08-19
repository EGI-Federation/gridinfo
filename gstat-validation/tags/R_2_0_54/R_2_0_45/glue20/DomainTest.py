#!/usr/bin/python

import sys
from EntityTest import EntityTest

class DomainTest(EntityTest):

  uniqueid = 'glue2domainid'

  mandatoryAttributes = ['glue2domainid']

  singleValueAttributes = ['glue2domainid', 'glue2domaindescription', 'glue2domainwww']
  singleValueAttributes.extend(getattr(EntityTest, 'singleValueAttributes'))

  dataTypes = {
    'glue2domainid': 'URI',
    'glue2domaindescription': 'String',
    'glue2domainwww': 'URL'}
  dataTypes.update(getattr(EntityTest, 'dataTypes'))

if __name__ == "__main__":
  sys.exit(DomainTest().main('glue2domain'))

