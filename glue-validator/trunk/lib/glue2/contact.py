#!/usr/bin/python                                                              

import glue2.common

def validate():

  SINGLE_VALUED_ATTRIBUTES = [
    'GLUE2LocationId', 
    'GLUE2ContactDetail', 
    'GLUE2ContactType',
    ]

  glue2.common.verify_single_valued(SINGLE_VALUED_ATTRIBUTES, entry, log)

  MANDATORY_ATTRIBUTES = [
    'GLUE2ContactId', 
    'GLUE2ContactDetail',
    'GLUE2ContactType',
    ]

  glue2.common.verify_mandatory_attributes(MANDATORY_ATTRIBUTES, entry, log)

  DATA_TYPES = {
    'GLUE2ContactId': 'uri',
    'GLUE2ContactDetail': 'uri',
    'GLUE2ContactType': 'contact_type'
    }
    
  glue2.common.verify_data_types(DATA_TYPES, entry, log)

