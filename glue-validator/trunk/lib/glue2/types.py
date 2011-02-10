#!/usr/bin/python
import re
import sys
import glue2.data

def is_DN_t(value):
   return is_String(value)

def is_LocalID_t(value):
   return is_String(value)

def is_ObjectClass(value):

   if value in glue2.data.schema:
      return True
   else:
      return False

def is_String( value):
   if value == '':
      return False
   else:
      return True

def is_ExtendedBoolean_t( value):
   value = value.lower()
   if value in ['false', 'true', 'undefined']:
      return True
   else:
      return False
   
def is_URI( value):
   return is_String(value)
   # RFC 3986: http://www.ietf.org/rfc/rfc3986.txt
   # Check URL (subtype of URI)
   uri = "^[a-zA-Z][a-zA-Z0-9+-.]*://[a-zA-Z0-9_.]+(:[0-9]+)*(/[a-zA-Z0-9_]*)*(\?[a-zA-Z0-9+-:@?./]+)?(#[a-zA-Z0-9+-:#@?./]+)?$"
   if re.match(uri, value):
      return True
   else:
      # Check other URIs
      uri = "^[a-zA-Z][a-zA-Z0-9+-.@:]*:[a-zA-Z0-9+-.@:]*$"
      if re.match(uri, value):
         return True
      else:
         return False

def is_URL( value):
   # RFC 1738: http://www.ietf.org/rfc/rfc1738.txt
   # Protocols accepted: http|ftp|https|ftps|sftp
   # Protocols rejected on purpose: gopher|news|nntp|telnet|mailto|file|etc.
   url = "(((http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&amp;%_\./-~-]*)?"
   if re.match(url, value):
      return 1
   else:
      return 0

   
def is_Real32( value):
   # IEE 754-2008: http://en.wikipedia.org/wiki/IEEE_754-2008
   # I just check it is a floating point number
   floatingpoint = "-*[0-9]+(.[0-9]+)*"
   if re.match(floatingpoint, value):
      return True
   else:
      return False

def is_ContactType_t( value):
   value = value.lower()
   if value in ['general', 'security', 'sysadmin', 'usersupport']:
      return True
   else:
      return False

def is_UInt32( value):
   # Check http://en.wikipedia.org/wiki/Integer_(computer_science)
   if re.match("^[0-9]+$", value):
      if int(value) <= sys.maxint:
         return True
      return False

def is_UInt64( value):
   # Check http://en.wikipedia.org/wiki/Integer_(computer_science)
   if re.match("^[0-9]+$", value):
      if long(value) <= 18446744073709551615L:
         return True
      return False

def is_DateTime_t( value):
   # Check http://www.w3.org/TR/xmlschema-2/#dateTime
   dateTime = "^-?[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])T([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z?$"

   if re.match(dateTime, value):
      return True
   return False

def is_Email_t( email):
   if len(email) > 7:
      if re.match("mailto:[ ]*.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
         return True
   return False

def is_QualityLevel_t(value):
   quality_levels = ['development', 'pre-production', 'production', 'testing']
   if value in quality_levels:
      return True
   else:
      return False

def is_InterfaceName_t(value):
   return is_ServiceType_t(value)

def is_PolicyScheme_t(value):
   schemes = ['basic', 'gacl', 'org.glite.standard']
   if value in schemes:
      return True
   else:
      return False

def is_ServiceType_t(value):
   types = [
      'org.glite.wms.WMProxy',
      'org.glite.lb.Server',
      'org.glite.ce.CREAM',
      'org.glite.ce.Monitor',
      'org.glite.rgma.Consumer',
      'org.glite.rgma.Registry',
      'org.glite.rgma.Schema',
      'org.glite.rgma.Browser',
      'org.glite.rgma.PrimaryProducer',
      'org.glite.rgma.SecondaryProducer',
      'org.glite.rgma.OnDemandProducer',
      'org.glite.RTEPublisher',
      'org.glite.voms',
      'org.glite.voms-admin',
      'org.glite.AMGA',
      'org.glite.ChannelManagement',
      'org.glite.FileTransfer',
      'org.glite.FileTransferStats',
      'org.glite.ChannelAgent',
      'org.glite.Delegation',
      'org.glite.KeyStore',
      'SRM',
      'gsiftp',
      'org.edg.gatekeeper',
      'it.infn.GridICE',
      'MyProxy',
      'GUMS',
      'gridmap-file',
      'GridCat',
      'edu.caltech.cacr.monalisa',
      'OpenSSH',
      'xroot',
      'BDII',
      'bdii_site',
      'bdii_top',
      'VOBOX',
      'msg.broker.rest',
      'msg.broker.stomp',
      'msg.broker.stomp-ssl',
      'msg.broker.openwire',
      'msg.broker.openwire-ssl',
      'org.lcg.Frontier',
      'org.lcg.Squid',
      'Nagios',
      'National-NAGIOS',
      'Project-NAGIOS',
      'Regional-NAGIOS',
      'data-location-interface',
      'local-data-location-interface',
      'lcg-file-catalog',
      'lcg-local-file-catalog',
      'pbs.torque.server',
      'pbs.torque.maui',
      'other'
      ]
   if value in types:
      return True
   else:
      return False
    
def is_Capability_t(value):
   types =[   
      'data.access.flatfiles',
      'data.access.relational',
      'data.access.xml',
      'data.management.replica',
      'data.management.storage',
      'data.management.transfer',
      'data.naming.resolver',
      'data.naming.scheme',
      'data.transfer',
      'executionmanagement.candidatesetgenerator',
      'executionmanagement.dynamicvmdeploy',
      'executionmanagement.executionandplanning',
      'executionmanagement.jobdescription',
      'executionmanagement.jobexecution',
      'executionmanagement.jobmanager',
      'executionmanagement.reservation',
      'information.discovery',
      'information.logging',
      'information.model',
      'information.monitoring',
      'information.provenance',
      'security.accounting',
      'security.attributeauthority',
      'security.authentication',
      'security.authorization',
      'security.credentialstorage',
      'security.delegation',
      'security.identymapping'
      ]   
   if value in types:
      return True
   else:
      return False

def is_StorageCapacity_t(value):
   types = [
      'online', 
      'installedonline', 
      'nearline', 
      'installednearline', 
      'offline', 
      'cache'
      ]
   if value in types:
      return True
   else:
      return False

def is_StorageAccessProtocol_t(value):
   types = [
      'afs',
      'dcap',
      'file',
      'gsidcap',
      'gsiftp',
      'gsirfio',
      'http',
      'https',
      'nfs',
      'rfio',
      'root',
      'xrootd'
      ]
   if value in types:
      return True
   else:
      return False

def is_ExpirationMode_t(value):
   types = ['neverexpire', 'releasewhenexpired Support', 'warnwhenexpired']
   if value in types:
      return True
   else:
      return False

if __name__ == '__main__':
   pass
