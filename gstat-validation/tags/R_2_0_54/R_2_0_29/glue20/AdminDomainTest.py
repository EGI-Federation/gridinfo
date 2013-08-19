#!/usr/bin/python

import sys
from DomainTest import DomainTest

class AdminDomainTest(DomainTest):

  singleValueAttributes = ['glue2admindomaindistributed',
    'glue2admindomainowner', 'glue2admindomainadmindomainforeignkey']
  singleValueAttributes.extend(getattr(DomainTest, 'singleValueAttributes'))

  relations = {
    'glue2admindomainadmindomainforeignkey': 'glue2domainid'}
  relations.update(getattr(DomainTest, 'relations'))

  dataTypes = {
    'glue2admindomaindistributed': 'ExtendedBoolean_t',
    'glue2admindomainowner': 'String'}
  dataTypes.update(getattr(DomainTest, 'dataTypes'))

if __name__ == "__main__":
  sys.exit(AdminDomainTest().main('glue2admindomain'))

