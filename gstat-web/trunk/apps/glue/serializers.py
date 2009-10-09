#!/usr/bin/python
import newserializers
from glue.models import gluesite

class GlueSerializer(newserializers.BaseSerializer):
    def deep(self, obj, *args, **kwargs):
        data = { 
            'id' : obj.uuid,
            'accounting_name' : obj.accounting_name,
            'tier' : obj.wlcg_tier,
            }
        
        return('Glue', data)

newserializers.register(gluesite, GlueSerializer)    
