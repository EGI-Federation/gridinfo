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
'waiting_jobs' : {
'description' : 'Waiting Jobs 444444 published',
'long_description' : 'Dear sys admin,\n\n Your site is publishing 444444 Waiting Jobs. Please, refer to \
                https://wiki.egi.eu/wiki/Tools/Manuals/TS59 , to get more details on how to fix this problem.\n\n \
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
'long_description' : 'Dear site admin,\n\n Your site is publishing 999999999 for the GLUE2ComputingShareMaxCPUTime, \
                      which is the maximum obtainable CPU time limit that MAY be granted to the job upon user request \
                      per slot (do not confuse with GLUE2ComputingShareMaxTotalCPUTime, which is the maximum obtainable \
                      CPU time limit that MAY be granted to the job upon user request across all assigned slots; this \
                      attribute is a limit on the sum of the CPU time used in all the slots occupied by a multi-slot job). \
                      LHCb uses GLUE2ComputingShareMaxCPUTime to calculate the queue length. \
                      Would it be possible to provide a defined limit for GLUE2ComputingShareMaxCPUTime?\n\nDetails:',
'mail' : 'wlcg-lhcb-bdii-srm-comparison@cern.ch',
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
'mail' : 'wlcg-lhcb-bdii-srm-comparison@cern.ch',
'loginname' : 'DN = /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=roiser/CN=576600/CN=Stefan Roiser',
'name' : 'Stefan Roiser',
'priority' : 'less urgent',
'last_modifier' : 'Stefan Roiser',
'last_login' : 'Stefan Roiser',
'carbon_copy' : 'maria.alandes.pradillo@cern.ch'
},
'nagios_ggus' : {
'description' : 'NAGIOS  *org.bdii.GLUE2-Validate* failed on%%',
'long_description' : None,
'mail' : None,
'loginname' : None,
'name' : None,
'priority' : None,
'last_modifier' : None,
'last_login' : None,
'carbon_copy' : None
}
}
