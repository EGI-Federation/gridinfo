#
# Library to declare templates for automatic GGUS generation
# 

templates = {
'obsolete_entries' : {
'description' : 'GLUE 2 obsolete entries',
'long_description' : 'Dear sys admin,\n\n It seems you are running a buggy version of the \
                resource BDII and/or the site BDII (please, check them all!) that produces \
                obsolete GLUE 2 entries.\n\n Could you please consider upgrading to the latest BDII? Obsolete \
                entries raise an Error in glue-validator and we are trying to clean this up before we could \
                actually release glue-validator as a Nagios probe.\n\n \
                Latest versions of the bdii package are available in EMI, UMD and EPEL repositories for SL5 and SL6.\n\n \
                Thanks a lot,\nMaria\n\n',
'mail' : 'maria.alandes.pradillo@cern.ch',
'loginname' : '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=malandes/CN=644124/CN=Maria Alandes Pradillo',
'name' : 'Maria Alandes',
'priority' : 'less urgent',
'last_modifier' : 'Maria Alandes',
'last_login' : 'Maria Alandes',
'carbon_copy' : None
},
'maxCPUTime' : {
'description' : 'Publishing default value for Max CPU Time',
'long_description' : 'Dear site admin,\n\n Your site is publishing 999999999 for the Max CPU Time. \
                      LHCb uses this parameter to calculate the queue length. Would it be possible to provide a \
                      defined limit for Max CPU Time?\n\nDetails:',
'mail' : 'lhcb-grid-bdii-srm-comparison@cern.ch',
'loginname' : 'DN = /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=roiser/CN=576600/CN=Stefan Roiser',
'name' : 'Stefan Roiser',
'priority' : 'less urgent',
'last_modifier' : 'Stefan Roiser',
'last_login' : 'Stefan Roiser',
'carbon_copy' : 'maria.alandes.pradillo@cern.ch'
},
'lhcb-storage' : {
'description' : 'BDII and SRM publish inconsistent storage capacity numbers',
'long_description' : 'Dear site admin,\n\n Your site is publishing inconsistent storage capacity numbers in BDII compared \
                      to what SRM reports. Could you please check?\n\nDetails:',
'mail' : 'lhcb-grid-bdii-srm-comparison@cern.ch',
'loginname' : 'DN = /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=roiser/CN=576600/CN=Stefan Roiser',
'name' : 'Stefan Roiser',
'priority' : 'less urgent',
'last_modifier' : 'Stefan Roiser',
'last_login' : 'Stefan Roiser',
'carbon_copy' : 'maria.alandes.pradillo@cern.ch'
}
}
