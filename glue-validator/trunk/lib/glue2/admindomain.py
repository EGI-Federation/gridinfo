#!/usr/bin/python

import glue2.common

def validate(entry, log):

    SINGLE_VALUED_ATTRIBUTES = [ 
        'DN',
        'GLUE2DomainId',
        'GLUE2DomainDescription',
        'GLUE2AdminDomainDistributed',
        ]

    glue2.common.verify_single_valued(SINGLE_VALUED_ATTRIBUTES, entry, log)
    
    MANDATORY_ATTRIBUTES = [
        'GLUE2DomainId',
        ]
    
    glue2.common.verify_mandatory_attributes(MANDATORY_ATTRIBUTES, entry, log)

    DATA_TYPES ={
        'GLUE2DomainId' : 'uri', 
        'GLUE2DomainDescription' : 'string',
        'GLUE2AdminDomainDistributed': 'extended_boolean_t',
        'GLUE2AdminDomainOwner' : 'string',
        'GLUE2AdminDomainAdminDomainForeignKey' : 'uri',
        'GLUE2DomainWWW' : 'url',
        }
    
    glue2.common.verify_data_types(DATA_TYPES, entry, log)

