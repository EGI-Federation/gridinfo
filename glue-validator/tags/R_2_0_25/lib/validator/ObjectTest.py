import unittest
import validator.utils

class ObjectTest(unittest.TestCase):

    def __init__(self, test_name, ldif_dict):
        unittest.TestCase.__init__(self, test_name)
        self.objects = []
 
        for dn in ldif_dict:
           if 'objectClass' in ldif_dict[dn]:
               for obj in ldif_dict[dn]['objectClass']:
                   if obj not in self.objects:
                      self.objects.append(obj)
 
    def test_mandatory_object_class(self):
        if self.objects:
            status = True
            message = ""
            if  'GLUE2Domain' in self.objects and 'GLUE2Location' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2Domain published','GLUE2Location missing')
                status = False
            if  'GLUE2Domain' in self.objects and 'GLUE2Contact' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2Domain published','GLUE2Contact missing')
                status = False
            if  'GLUE2ComputingService' in self.objects and 'GLUE2Service' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2ComputingService published','GLUE2Service missing')
                status = False
            if  'GLUE2StorageService' in self.objects and 'GLUE2Service' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2StorageService published','GLUE2Service missing')
                status = False
            if  'GLUE2ComputingEndpoint' in self.objects and 'GLUE2Endpoint' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2ComputingEndpoint published','GLUE2Endpoint missing')
                status = False
            if  'GLUE2StorageEndpoint' in self.objects and 'GLUE2Endpoint' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2StorageEndpoint published','GLUE2Endpoint missing')
                status = False
            if  'GLUE2ComputingShare' in self.objects and 'GLUE2Share' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2ComputingShare published','GLUE2Share missing')
                status = False
            if  'GLUE2StorageShare' in self.objects and 'GLUE2Share' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2StorageShare published','GLUE2Share missing')
                status = False
            if  'GLUE2Share' in self.objects and 'GLUE2MappingPolicy' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2Share published','GLUE2MappingPolicy missing')
                status = False
            if  'GLUE2Endpoint' in self.objects and 'GLUE2AccessPolicy' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2Endpoint published','GLUE2AccessPolicy missing')
                status = False
            if  'GLUE2ComputingService' in self.objects and 'GLUE2ComputingManager' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2ComputingService published','GLUE2ComputingManager missing')
                status = False
            if  'GLUE2ComputingManager' in self.objects and 'GLUE2ExecutionEnvironment' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2ComputingManager published','GLUE2ExecutionEnvironment missing')
                status = False
            # Known issue affecting DPM fixed in version 1.8.8 but still affecting many sites
            #if  'GLUE2StorageServiceCapacity' in self.objects and 'GLUE2StorageService' not in self.objects:
            #    message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2StorageServiceCapacity published','GLUE2StorageService missing')
                status = False
            if  'GLUE2StorageShareCapacity' in self.objects and 'GLUE2StorageShare' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2StorageShareCapacity published','GLUE2StorageShare missing')
                status = False
            if  'GLUE2StorageService' in self.objects and 'GLUE2StorageAccessProtocol' not in self.objects:
                message = message + validator.utils.message_generator("ERROR","E025","NA",'GLUE2StorageService published','GLUE2StorageAccessProtocol missing')
                status = False
            self.assertTrue(status, message)

