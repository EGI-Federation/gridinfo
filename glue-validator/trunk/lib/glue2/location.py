#!/usr/bin/python

import glue2.common

def validate(entry, log):

    SINGLE_VALUED_ATTRIBUTES = [ 
      'GLUE2LocationId', 
      'GLUE2LocationAddress', 
      'GLUE2LocationPlace', 
      'GLUE2LocationCountry', 
      'GLUE2LocationPostcode',
      'GLUE2LocationLatitude', 
      'GLUE2LocationLongitude'
      ]

    glue2.common.verify_single_valued(SINGLE_VALUED_ATTRIBUTES, entry, log)
    
    MANDATORY_ATTRIBUTES = [
      'GLUE2LocationId',
        ]
    
    glue2.common.verify_mandatory_attributes(MANDATORY_ATTRIBUTES, entry, log)

    DATA_TYPES ={
      'GLUE2LocationId': 'URI',
      'GLUE2LocationAddress': 'String',
      'GLUE2LocationPlace': 'String',
      'GLUE2LocationCountry': 'String',
      'GLUE2LocationPostcode': 'String',
      'GLUE2LocationLatitude': 'Real32',
      'GLUE2LocationLongitude': 'Real32'
      }
    
    glue2.common.verify_data_types(DATA_TYPES, entry, log)

