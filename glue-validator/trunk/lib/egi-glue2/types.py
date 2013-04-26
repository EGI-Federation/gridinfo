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
   # Protocols accepted: see is_allowed_URL_Schema
   # Protocols rejected on purpose: gopher|news|nntp|telnet|mailto|file|etc.
   url = "(?:(?:([a-z0-9+.-]+)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&amp;%_\./-~-]*)?"
   m = re.match(url,value)
   if m is None:
      return False
   return is_allowed_URL_Schema(m.group(1))

def is_allowed_URL_Schema(value):
   types = [
      'http',
      'ftp',
      'https',
      'ftps',
      'sftp',
      'gsiftp',
      'xroot',
      'dcap',
      'gsidcap',
      'httpg',
      'ldap',
      'voms',
      'myproxy',
      'lfc'
      ]
   if value in types:
      return True
   else:
      return False
   
   
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

def is_Int32( value):
   # Check http://en.wikipedia.org/wiki/Integer_(computer_science)
   if re.match("^(?:[-+])?[0-9]+$", value):
      if -sys.maxint <= int(value) <= sys.maxint:
         return True
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
   interfaces = [
      'ogf.bes',
      'ogf.srm',
      'org.ogf.bes',
      'org.ogf.glue.emies.activitycreation',
      'org.ogf.glue.emies.activitymanagement',
      'org.ogf.glue.emies.resourceinfo',
      'org.ogf.glue.emies.activityinfo',
      'org.ogf.glue.emies.delegation',
      'org.glite.Argus.PDP',
      'org.glite.Argus.PAP',
      'org.glite.Argus.PEP',
      'org.glite.ce.ApplicationPublisher',
      'org.nordugrid.ldapglue1',
      'org.nordugrid.wsrfglue2',
      'org.nordugrid.ldapglue2',
      'org.nordugrid.gridftpjob',
      'org.nordugrid.ldapng'
      ]
   if value in interfaces:
       return True
   else:
       return is_ServiceType_t(value) or is_allowed_URL_Schema(value)

def is_JobDescription_t(value):
   descriptions = [
      'condor',
      'egee:jdl',
      'emies:adl',
      'globus:rsl',
      'nordugrid:xrsl',
      'ogf:jsdl:1.0'
      ]
   if value in descriptions:
       return True
   else:
       return False

def is_PolicyScheme_t(value):
   schemes = ['basic', 'gacl', 'org.glite.standard']
   if value in schemes:
      return True
   else:
      return False

def is_ServiceType_t(value):
   types = [
      'APEL',
      'BDII',
      'bdii_site',
      'bdii_top',
      'CE',
      'egi.GRIDVIEW',
      'egi.GSTAT',
      'egi.MetricsPortal',
      'egi.NetworkPortal',
      'egi.OpsPortal',
      'eu.egi.AccountingPortal',
      'eu.egi.APELRepository',
      'eu.egi.GGUS',
      'eu.egi.GOCDB',
      'eu.egi.MSGBroker',
      'gLExec',
      'gLite-APEL',
      'MDS-GIIS',
      'MyProxy',
      'ngi.OpsPortal',
      'OpenSSH',
      'org.dcache.storage',
      'org.glite.AMGA',
      'org.glite.Argus',
      'org.glite.argus',
      'org.glite.ce.CREAM',
      'org.glite.ce.Monitor',
      'org.glite.ChannelAgent',
      'org.glite.ChannelManagement',
      'org.glite.Delegation',
      'org.glite.FiremanCatalog',
      'org.glite.FileTransfer',
      'org.glite.FileTransferStats',
      'org.glite.fts',
      'org.glite.KeyStore',
      'org.glite.lb',
      'org.glite.lb.Server',
      'org.glite.Metadata',
      'org.glite.rgma.Registry',
      'org.glite.rgma.Schema',
      'org.glite.rgma.Browser',
      'org.glite.rgma.PrimaryProducer',
      'org.glite.rgma.SecondaryProducer',
      'org.glite.rgma.OnDemandProducer',
      'org.glite.RTEPublisher',
      'org.glite.SEIndex',
      'org.glite.voms',
      'org.glite.voms-admin',
      'org.glite.wms',
      'org.glite.wms.WMProxy',
      'org.irods.irods3',
      'org.lcg.Frontier',
      'org.lcg.Squid',
      'org.nordugrid.arex',
      'org.nordugrid.execution.arex',
      'org.nordugrid.information.egiis',
      'org.nordugrid.storage',
      'org.nordugrid.isis',
      'org.ogf.bes.BESFactory',
      'org.ogf.bes.BESManagement',
      'org.ogf.glue.emir',
      'pbs.torque.server',
      'pbs.torque.maui',
      'SGAS',
      'UI',
      'eu.unicore.USE',
      'unicore6.Registry',
      'unicore6.ServiceOrchestrator',
      'unicore6.StorageFactory',
      'unicore6.StorageManagement',
      'unicore6.TargetSystemFactory',
      'unicore6.UVOSAssertionQueryService',
      'unicore6.WorkflowFactory',
      'VOBOX',
      'xroot',
      'SRM',
      'data-location-interface',
      'edu.caltech.cacr.monalisa',
      'GridCat',
      'gridmap-file',
      'gsiftp',
      'GUMS',
      'it.infn.GridICE',
      'lcg-file-catalog',
      'lcg-local-file-catalog',
      'local-data-location-interface',
      'msg.broker.rest',
      'msg.broker.stomp',
      'msg.broker.stomp-ssl',
      'msg.broker.openwire',
      'msg.broker.openwire-ssl',
      'Nagios',
      'National-NAGIOS',
      'org.edg.gatekeeper',
      'org.lcg.Frontier',
      'org.lcg.Squid',
      'Project-NAGIOS',
      'Regional-NAGIOS',
      'other'
      ]
   if value in types:
      return True
   else:
      return False
    
def is_Capability_t(value):
   types = [   
      'data.access.flatfiles',
      'data.access.relational',
      'data.access.xml',
      'data.access.sessiondir',
      'data.access.stageindir',
      'data.access.stageoutdir',
      'data.management.replica',
      'data.management.storage',
      'data.management.transfer',
      'data.naming.resolver',
      'data.naming.scheme',
      'data.transfer',
      'data.transfer.cepull',
      'data.transfer.cepull.ftp',
      'data.transfer.cepush',
      'data.transfer.cepush.srm',
      'executionmanagement.candidatesetgenerator',
      'executionmanagement.dynamicvmdeploy',
      'executionmanagement.executionandplanning',
      'executionmanagement.jobdescription',
      'executionmanagement.jobexecution',
      'executionmanagement.jobmanager',
      'executionmanagement.reservation',
      'executionmanagement.jobcreation',
      'executionmanagement.jobmanagement',
      'information.discovery',
      'information.discovery.job',
      'information.discovery.resource',
      'information.logging',
      'information.model',
      'information.monitoring',
      'information.provenance',
      'information.publication',
      'information.lookup.job',
      'information.query',
      'information.query.xpath1',
      'security.accounting',
      'security.attributeauthority',
      'security.authentication',
      'security.authorization',
      'security.credentialstorage',
      'security.delegation',
      'security.identitymapping'
      ]   
   if value in types:
      return True
   else:
      return False

def is_AppEnvState_t(value):
   states = [
      'installable',
      'installationfailed',
      'installedbroken',
      'installednotverified',
      'installedverified',
      'installingautomatically',
      'installingmanually',
      'notinstallable',
      'pendingremoval',
      'removing'
      ]
   if value in states:
      return True
   else:
      return False

def is_SchedulingPolicy_t(value):
   policies = [
      'fairshare',
      'fifo',
      'random'
      ]
   if value in policies:
      return True
   else:
      return False

def is_ComputingActivityType_t(value):
   types = [
      'collectionelement',
      'parallelelement',
      'single',
      'workflownode'
      ]
   if value in types:
      return True
   else:
      return False

def is_ComputingActivityState_t(value):
    # open season!
    return True

def is_AccessMode_t(value):
    # not described in the spec 
    return True

def is_ApplicationHandle_t(value):
   types = [
      'executable',
      'module',
      'Path',
      'softenv'
      ]
   if value in types:
      return True
   else:
      return False

def is_CPUMultiplicity_t(value):
   types = [
      'multicpu-multicore',
      'multicpu-singlecore',
      'singlecpu-multicore',
      'singlecpu-singlecore'
      ]
   if value in types:
      return True
   else:
      return False

def is_DataStoreType_t(value):
   types = [
      'disk',
      'optical',
      'tape'
      ]
   if value in types:
      return True
   else:
      return False

def is_License_t(value):
   types = [
      'commercial',
      'opensource',
      'unknown'
      ]
   if value in types:
      return True
   else:
      return False

def is_NetworkInfo_t(value):
   types = [
      '100megabitethernet',
      'gigabitethernet',
      'infiniband',
      'myrinet'
      ]
   if value in types:
      return True
   else:
      # let it pass
      return True

def is_OSFamily_t(value):
   types = [
      'linux',
      'macosx',
      'solaris',
      'windows'
      ]
   if value in types:
      return True
   else:
      return False

def is_OSName_t(value):
   types = [
      'aix',
      'centos',
      'debian',
      'fedoracore',
      'gentoo',
      'leopard',
      'linux-rocks',
      'mandrake',
      'redhatenterpriseas',
      'scientificlinux',
      'scientificlinuxcern',
      'suse',
      'ubuntu',
      'windowsvista',
      'windowsxp'
      ]
   if value in types:
      return True
   else:
      # let it pass
      return True


def is_ParallelSupport_t(value):
   types = [
      'mpi',
      'none',
      'openmp'
      ]
   if value in types:
      return True
   else:
      return False

def is_Platform_t(value):
   types = [
      'amd64',
      'i386',
      'i686',
      'itanium',
      'powerpc',
      'sparc',
      'x86_64'
      ]
   if value in types:
      return True
   else:
      return False

def is_ReservationPolicy_t(value):
   types = [
      'mandatory',
      'none',
      'optional'
      ]
   if value in types:
      return True
   else:
      return False

def is_RetentionPolicy_t(value):
   types = [
      'custodial',
      'output',
      'replica'
      ]
   if value in types:
      return True
   else:
      return False

def is_AccessLatency_t(value):
   types = [
      'online',
      'nearline',
      'offline'
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

def is_EndpointHealthState_t(value):
   types = ['critical', 'ok', 'other', 'unknown', 'warning']
   if value in types:
      return True
   else:
      return False

def is_EndpointTechnology_t(value):
   types = [ 'corba', 'jndi', 'webservice' ]
   if value in types:
      return True
   else:
      return False

def is_ServingState_t(value):
   types = [ 'closed', 'draining', 'production', 'queueing' ]
   if value in types:
      return True
   else:
      return False

def is_Staging_t(value):
   types = [ 'none', 'stagingin', 'staginginout', 'stagingout']
   if value in types:
      return True
   else:
      return False

def is_Benchmark_t(value):
   types = [ 'bogomips', 'cfp2006', 'cint2006', 'linpack', 'specfp2000', 'specint2000', 'hep-spec06' ]
   if value in types:
      return True
   else:
      return False

def is_Benchmarkabbr_t(value):
   types = [ 'SI00', 'HS06', 'SI2K' ]
   if value in types:
      return True
   else:
      return False


def is_JobDescription_t(value):
   types = [ 'condor', 'egee:jdl', 'globus:rsl', 'nordugrid:xrsl', 'ogf:jsdl:1.0', 'glite:jdl']
   if value in types:
      return True
   else:
      return False


def is_EntityOtherInfo_t(value):
   types = [
      'InfoProviderHost',
      'InfoProviderName',
      'InfoProviderVersion',
      'ProfileName',
      'ProfileVersion',
      'BLOG',
      'CONFIG',
      'EGI_NGI',
      'GRID',
      'ICON',
      'OLDNAME',
      'WLCG_NAME',
      'WLCG_NAMEICON',
      'WLCG_PARENT',
      'WLCG_TIER' 
      'MiddlewareName',
      'MiddlewareVersion',
      'HostDN',
      'Share',
      'CPUScalingReferenceSI00',
      'CreamCEId',
      'CREAMCEId',
      'MiddlewareName=EMI',
      'This CREAM-CE is using Argus'
      ] 
   if value.rsplit('=')[0] in types:
      return True
   else:
      return False

def is_Middleware_t(value):
   types = [
      'EMI',
      'UMD'
      ]
   if value in types:
      return True
   else:
      return False
  
def is_Tier_t(value):
   types = [
      '0',
      '1',
      '2',
      '3'
      ]
   if value in types:
      return True
   else:
      return False

def is_WLCGname_t(value):
   types = [
      'AGLT2',
      'Australia-ATLAS',
      'BEgrid-ULB-VUB',
      'BEIJING-LCG2',
      'BelGrid-UCL',
      'BNL-ATLAS',
      'BU_ATLAS_Tier2',
      'BUDAPEST',
      'CA-ALBERTA-WESTGRID-T2',
      'CA-MCGILL-CLUMEQ-T2',
      'CA-SCINET-T2',
      'CA-VICTORIA-WESTGRID-T2',
      'CERN-PROD',
      'CIEMAT-LCG2',
      'CIT_CMS_T2',
      'CSCS-LCG2',
      'CYFRONET-LCG2',
      'DESY-HH',
      'DESY-HH',
      'DESY-ZN',
      'DESY-ZN',
      'DESY-ZN',
      'EFDA-JET',
      'ELTE',
      'FI_HIP_T2',
      'FMPhI-UNIBA',
      'FZK-LCG2',
      'GLOW',
      'GoeGrid',
      'GR-07-UOI-HEPLAB',
      'GridUNESP_CENTRAL',
      'GRIF',
      'GSI-LCG2',
      'HEPHY-UIBK',
      'Hephy-Vienna',
      'HU_ATLAS_Tier2',
      'ICM',
      'IEPSAS-Kosice',
      'ifae',
      'IFCA-LCG2',
      'IFIC-LCG2',
      'IL-TAU-HEP',
      'IN2P3-CC',
      'IN2P3-CC-T2',
      'IN2P3-CPPM',
      'IN2P3-IRES',
      'IN2P3-LAPP',
      'IN2P3-LPC',
      'IN2P3-LPSC',
      'IN2P3-SUBATECH',
      'IN-DAE-VECC-02',
      'INDIACMS-TIFR',
      'INFN-BARI',
      'INFN-CATANIA',
      'INFN-CNAF-LHCB',
      'INFN-FRASCATI',
      'INFN-LNL-2',
      'INFN-MILANO-ATLASC',
      'INFN-NAPOLI-ATLAS',
      'INFN-PISA',
      'INFN-ROMA1',
      'INFN-ROMA1-CMS',
      'INFN-T1',
      'INFN-TORINO',
      'ITEP',
      'JINR-LCG2',
      'Kharkov-KIPT-LCG2',
      'KR-KISTI-GCRT-01',
      'KR-KISTI-GSDC-01',
      'LCG_KNU',
      'LC-glcc',
      'LIP-Coimbra',
      'LIP-Lisbon',
      'LRZ-LMU',
      'MIT_CMS',
      'MPPMU',
      'MWT2',
      'MWT2_UC',
      'NCG-INGRID-PT',
      'NCP-LCG2',
      'NDGF-T1',
      'Nebraska',
      'NERSC-PDSF',
      'NIHAM',
      'NIKHEF-ELPROD',
      'NO-NORGRID-T2',
      'OU_OCHEP_SWT2',
      'pic',
      'praguelcg2',
      'PSNC',
      'Purdue-Carter',
      'Purdue-Hansen',
      'Purdue-RCAC',
      'Purdue-Rossmann',
      'Purdue-Steele',
      'RAL-LCG2',
      'RO-02-NIPNE',
      'RO-07-NIPNE',
      'RO-11-NIPNE',
      'RO-13-ISS',
      'RO-14-ITIM',
      'RO-16-UAIC',
      'RRC-KI',
      'ru-Moscow-FIAN-LCG2',
      'ru-Moscow-SINP-LCG2',
      'ru-PNPI',
      'RU-Protvino-IHEP',
      'RU-SPbSU',
      'Ru-Troitsk-INR-LCG2',
      'RWTH-Aachen',
      'SARA-MATRIX',
      'SE-SNIC-T2',
      'SFU-LCG2',
      'SiGNET',
      'SPRACE',
      'SWT2_CPB',
      'T2_Estonia',
      'Taiwan-LCG2',
      'TECHNION-HEP',
      'TOKYO-LCG2',
      'TR-03-METU',
      'TR-10-ULAKBIM',
      'TRIUMF-LCG2',
      'TW-FTT',
      'A-BITP',
      'UA-KNU',
      'UAM-LCG2',
      'UB-LCG2',
      'UCSDT2',
      'UFlorida-HPC',
      'UFlorida-PG',
      'UFlorida-SSERCA',
      'UKI-LT2-Brunel',
      'UKI-LT2-IC-HEP',
      'UKI-LT2-QMUL',
      'UKI-LT2-RHUL',
      'UKI-LT2-UCL-HEP',
      'UKI-NORTHGRID-LANCS-HEP',
      'UKI-NORTHGRID-LIV-HEP',
      'UKI-NORTHGRID-MAN-HEP',
      'UKI-NORTHGRID-SHEF-HEP',
      'UKI-SCOTGRID-DURHAM',
      'UKI-SCOTGRID-ECDF',
      'UKI-SCOTGRID-GLASGOW',
      'UKI-SOUTHGRID-BHAM-HEP',
      'UKI-SOUTHGRID-BRIS-HEP',
      'UKI-SOUTHGRID-CAM-HEP',
      'UKI-SOUTHGRID-OX-HEP',
      'UKI-SOUTHGRID-RALPP',
      'UKI-SOUTHGRID-SUSX',
      'UNIBE-LHEP',
      'UNI-FREIBURG',
      'USC-LCG2',
      'USCMS-FNAL-WC1',
      'UTA_SWT2',
      'WEIZMANN-LCG2',
      'WT2',
      'wuppertalprod'
      ]
   if value in types:
      return True
   else:
      return False

def is_Grid_t(value):
   types = [
      'EGI',
      'EELA',
      'WLCG',
      'NDGF',
      'GRIDPP',
      'UKNGS', 
      'LondonGrid',
      'NORTGHRID',
      'SOUTHGRID',
      'SCOTGRID',
      'SEE-GRID',
      'OSG'
      ]
   if value in types:
      return True
   else:
      return False

def is_Config_t(value):
   types = [
      'yaim',
      'puppet',
      'quattor'
      ]
   if value in types:
      return True
   else:
      return False

def is_EGIngi_t(value):
    types = [
       'AsiaPacific',
       'CERN',
       'EGI.eu',
       'NGI_AEGIS',
       'NGI_AL',
       'NGI_ARMGRID',
       'NGI_BA',
       'NGI_BG',
       'NGI_BY',
       'NGI_CH',
       'NGI_CYGRID',
       'NGI_CZ',
       'NGI_DE',
       'NGI_FI',
       'NGI_FRANCE',
       'NGI_GE',
       'NGI_GRNET',
       'NGI_HR',
       'NGI_HU',
       'NGI_IBERGRID',
       'NGI_IE',
       'NGI_IL',
       'NGI_IT',
       'NGI_MARGI',
       'NGI_MD',
       'NGI_ME',
       'NGI_NDGF',
       'NGI_NL',
       'NGI_PL',
       'NGI_RO',
       'NGI_SI',
       'NGI_SK',
       'NGI_TR',
       'NGI_UA',
       'NGI_UK',
       'NGI_ZA',
       'ROC_Canada',
       'ROC_IGALC',
       'ROC_LA',
       'Russia'
       ]
    if value in types:
       return True
    else:
       return False
  

def is_VO_t(value): 
    types = [
    'aegis',
    'alice',
    'ams',
    'ams02.cern.ch',
    'apesci',
    'argo',
    'armgrid.grid.am',
    'astro.vo.eu-egee.org',
    'astron',
    'astrop',
    'atlas',
    'atlas.ac.il',
    'auger',
    'auvergrid',
    'babar',
    'balticgrid',
    'bbmri.nl',
    'belle',
    'belle2.org',
    'bg-edu.grid.acad.bg',
    'bing.vo.ibergrid.eu',
    'bio',
    'biomed',
    'calice',
    'camont',
    'cdf',
    'cesga',
    'chem.vo.ibergrid.eu',
    'climate-g.vo.eu-egee.org',
    'cms',
    'comet.j-parc.jp',
    'cometa',
    'compchem',
    'comput-er.it',
    'cosmo',
    'cppm',
    'cyclops',
    'd4science.research-infrastructures.eu',
    'dca.euro-vo.org',
    'dech',
    'demo.vo.edges-grid.eu',
    'desktopgrid.vo.edges-grid.eu',
    'desy',
    'dream.hipcat.net',
    'dteam',
    'dzero',
    'earth.vo.ibergrid.eu',
    'edteam',
    'eearth',
    'eela',
    'egeode',
    'eirevo.ie',
    'embrace',
    'enea',
    'eng.vo.ibergrid.eu',
    'enmr.eu',
    'env.see-grid-sci.eu',
    'envirogrids.vo.eu-egee.org',
    'eo-grid.ikd.kiev.ua',
    'epic.vo.gridpp.ac.uk',
    'esr',
    'euasia.euasiagrid.org',
    'euchina',
    'euindia',
    'eumed',
    'fedcloud.egi.eu',
    'fkppl.kisti.re.kr',
    'fusion',
    'gaussian',
    'geant4',
    'geclipse',
    'geclipsetutor',
    'gene',
    'gerda.mpg.de',
    'ghep',
    'gilda',
    'glast.org',
    'gr-sim.grid.auth.gr',
    'grid.uniovi.es',
    'gridcc',
    'gridit',
    'gridmosi.ici.ro',
    'gridpp',
    'hermes',
    'hgdemo',
    'hone',
    'hpc.vo.ibergrid.eu',
    'hungrid',
    'iber.vo.ibergrid.eu',
    'icarus-exp.org',
    'icecube',
    'ict.vo.ibergrid.eu',
    'ific',
    'igi.italiangrid.it',
    'ilc',
    'ildg',
    'imath.cesga.es',
    'inaf',
    'infngrid',
    'ipv6.hepix.org',
    'israelvo.isragrid.org.il',
    'lattice.itep.ru',
    'lhcb',
    'libi',
    'life.vo.ibergrid.eu',
    'lights.infn.it',
    'lofar',
    'lsgrid',
    'magic',
    'meteo.see-grid-sci.eu',
    'mice',
    'minos.vo.gridpp.ac.uk',
    'moldyngrid',
    'mpi-kickstart.egi.eu',
    'na4.vo.eu-egee.org',
    'na62.vo.gridpp.ac.uk',
    'ncf',
    'neiss.org.uk',
    'net.egi.eu',
    'neurogrid.incf.org',
    'ngs.ac.uk',
    'nordugrid.org',
    'oper.vo.eu-eela.eu',
    'ops',
    'ops.ndgf.org',
    'ops.vo.egee-see.org',
    'ops.vo.ibergrid.eu',
    'oxgrid.ox.ac.uk',
    'pacs.infn.it',
    'pamela',
    'pfound.vo.ibergrid.eu',
    'pheno',
    'photon',
    'phys.vo.ibergrid.eu',
    'planck',
    'proactive',
    'prod.vo.eu-eela.eu',
    'pvier',
    'rdteam',
    'rfusion',
    'rgstest',
    'see',
    'seegrid',
    'seismo.see-grid-sci.eu',
    'sgdemo',
    'shiwa-workflow.eu',
    'snoplus.snolab.ca',
    'social.vo.ibergrid.eu',
    'solovo',
    'superbvo.org',
    'supernemo.vo.eu-egee.org',
    'swetest',
    't2k.org',
    'theophys',
    'tps.infn.it',
    'trgrida',
    'trgridb',
    'trgridd',
    'trgride',
    'tut.vo.ibergrid.eu',
    'twgrid',
    'ukmhd.ac.uk',
    'ukqcd',
    'uniandes.edu.co',
    'uscms',
    'verce.eu',
    'virgo',
    'vlemed',
    'vo.agata.org',
    'vo.aginfra.eu',
    'vo.aleph.cern.ch',
    'vo.apc.univ-paris7.fr',
    'vo.astro.pic.es',
    'vo.cmip5.e-inis.ie',
    'vo.complex-systems.eu',
    'vo.cs.br',
    'vo.cta.in2p3.fr',
    'vo.dch-rp.eu',
    'vo.delphi.cern.ch',
    'vo.dorii.eu',
    'vo.e-ca.es',
    'vo.eu-decide.eu',
    'vo.formation.idgrilles.fr',
    'vo.france-asia.org',
    'vo.france-grilles.fr',
    'vo.gear.cern.ch',
    'vo.general.csic.es',
    'vo.grand-est.fr',
    'vo.grid.auth.gr',
    'vo.gridcl.fr',
    'vo.grif.fr',
    'vo.helio-vo.eu',
    'vo.hess-experiment.eu',
    'vo.ifisc.csic.es',
    'vo.indicate-project.eu',
    'vo.ingv.it',
    'vo.ipnl.in2p3.fr',
    'vo.ipno.in2p3.fr',
    'vo.irfu.cea.fr',
    'vo.iscpif.fr',
    'vo.lal.in2p3.fr',
    'vo.landslides.mossaic.org',
    'vo.lapp.in2p3.fr',
    'vo.llr.in2p3.fr',
    'vo.londongrid.ac.uk',
    'vo.lpnhe.in2p3.fr',
    'vo.lpsc.in2p3.fr',
    'vo.lpta.in2p3.fr',
    'vo.mcia.fr',
    'vo.metacentrum.cz',
    'vo.msfg.fr',
    'vo.mure.in2p3.fr',
    'vo.neugrid.eu',
    'vo.northgrid.ac.uk',
    'vo.ops.csic.es',
    'vo.panda.gsi.de',
    'vo.paus.pic.es',
    'vo.pic.es',
    'vo.plgrid.pl',
    'vo.renabi.fr',
    'vo.rhone-alpes.idgrilles.fr',
    'vo.sbg.in2p3.fr',
    'vo.scotgrid.ac.uk',
    'vo.sim-e-child.org',
    'vo.sixt.cern.ch',
    'vo.sn2ns.in2p3.fr',
    'vo.southgrid.ac.uk',
    'vo.stratuslab.eu',
    'vo.turbo.pic.es',
    'vo.u-psud.fr',
    'vo.ucad.sn',
    'vo.up.pt',
    'voce',
    'webcom',
    'xenon.biggrid.nl',
    'xfel.eu',
    'zeus'
    ]
    if value in types:
       return True
    else:
       return False

