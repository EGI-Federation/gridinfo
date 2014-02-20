#!/usr/bin/python
#
# Script to monitor GLUE 1 and GLUE 2 deployment
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import fileinput

def glue_size (glue_version):

    if ( glue_version == "1" ):
        binding = "grid"
    elif ( glue_version == "2" ):
        binding = "glue"
    temp_file = "/afs/cern.ch/user/m/malandes/workspace/ssb/general/glue%s" % (glue_version)
    output = os.open (temp_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
    command1 = "ldapsearch -LLL -x -h lcg-bdii:2170 -b o=%s" % (binding)
    command2 = "ls -l --block-size=MB %s | cut -d \" \" -f5" % (temp_file)
    p = subprocess.Popen(command1 ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results = p.communicate()
    if (results[0].find("ldap_bind: Can't contact LDAP server") > -1):
       color = "grey"
       result = "Unreachable"
    else:
       color = "green"
       os.write(output,results[0])
       os.close(output)
       p = subprocess.Popen(command2 ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       results = p.communicate()
       result = results[0].strip()
    os.remove(temp_file)
    return color,result
 
path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/general"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/general" 
dt=datetime.datetime.now()
today=datetime.date.today()

command_glue1_dns              = "ldapsearch -LLL -x -h lcg-bdii:2170 -b mds-vo-name=local,o=grid dn | grep dn: | wc -l"
command_glue2_dns              = "ldapsearch -LLL -x -h lcg-bdii:2170 -b GLUE2GroupID=grid,o=glue dn | grep dn: | wc -l"
command_glue1_sites            = "ldapsearch -LLL -x -h lcg-bdii:2170 -b mds-vo-name=local,o=grid '(objectClass=GlueSite)' \
                                  GlueSiteUniqueID | grep GlueSiteUniqueID: | wc -l"
command_glue2_sites            = "ldapsearch -LLL -x -h lcg-bdii:2170 -b GLUE2GroupID=grid,o=glue \
                                  '(objectClass=GLUE2Domain)' GLUE2DomainID | grep GLUE2DomainID: | wc -l"
command_non_obsolete_glue2_appenv ="ldapsearch -LLL -x -h lcg-bdii -p 2170 -b GLUE2GroupID=grid,o=glue \
                                    '(&(objectClass=GLUE2ApplicationEnvironment)(GLUE2EntityCreationTime=%s*))' \
                                    dn | grep dn: | wc -l" % (today)
command_glue2_services         = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b GLUE2GroupID=grid,o=glue \
                                  '(objectClass=GLUE2Service)' GLUE2ServiceID | grep GLUE2ServiceID: | sort | uniq | wc -l"
command_glue1_endpoints        = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b mds-vo-name=local,o=grid \
                                  '(objectClass=GlueService)' GlueServiceUniqueID | grep GlueServiceUniqueID: \
                                  | sort | uniq | wc -l"
command_glue2_endpoints        = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b GLUE2GroupID=grid,o=glue \
                                  '(objectClass=GLUE2Endpoint)' \
                                  GLUE2EndpointID | grep GLUE2EndpointID: | sort | uniq | wc -l"
command_glue2_service_types    = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b GLUE2GroupID=grid,o=glue \
                                  '(objectClass=GLUE2Service)' GLUE2ServiceType | grep GLUE2ServiceType: \
                                  | sort | uniq | wc -l" 
command_glue1_endpoint_types   = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b mds-vo-name=local,o=grid \
                                  '(objectClass=GlueService)' GlueServiceType | grep GlueServiceType: | sort | uniq | wc -l"
command_glue2_endpoint_types   = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b GLUE2GroupID=grid,o=glue \
                                  '(objectClass=GLUE2Endpoint)' GLUE2EndpointInterfaceName \
                                  | grep GLUE2EndpointInterfaceName: | sort | uniq | wc -l"

test_dict = {
'glue1_dns'                 :  command_glue1_dns,
'glue2_dns'                 :  command_glue2_dns,
'glue1_sites'               :  command_glue1_sites,
'glue2_sites'               :  command_glue2_sites,
'non_obsolete_glue2_appenv' :  command_non_obsolete_glue2_appenv,
'glue2_services'            :  command_glue2_services, 
'glue1_endpoints'           :  command_glue1_endpoints,
'glue2_endpoints'           :  command_glue2_endpoints,
'glue2_service_types'       :  command_glue2_service_types,
'glue1_endpoint_types'      :  command_glue1_endpoint_types,
'glue2_endpoint_types'      :  command_glue2_endpoint_types,
'glue1_data_size'           :  "1",
'glue2_data_size'           :  "2"         
}

for test in test_dict.keys():

    output_file_name = "%s/%s.txt" % (path_to_output,test) 
    detail_file_name = "%s/%s.html" % (path_to_output,test) 
    detail_url = "%s/%s.html#%s" % (path_to_url,test,today)
    output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

    if ( test == "glue1_data_size" ) or (test == "glue2_data_size" ):
        color, result=glue_size(test_dict[test])
    else:
        p = subprocess.Popen(test_dict[test] ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        if (results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1 ):
            color = "grey"
            result = "Unreachable" 
        else:
            color = "green"
            result = results[0].strip()

    detail_result_string="<a name=\"%s\">%s: %s</a><br>\n</body></html>" % (today,today,result)
    for line in fileinput.input(detail_file_name, inplace=True): 
        sys.stdout.write(line.replace('</body></html>', detail_result_string))
    result_string = "%s lcg-bdii %s %s %s" % (dt,result,color,detail_url)
    os.write(output_fd,result_string)
    os.close(output_fd)

