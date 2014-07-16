#!/usr/bin/python
#
# Script to monitor GLUE 1 and GLUE 2 deployment per site
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import fileinput
import sites

path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/general/glue-per-site"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/general/glue-per-site" 
dt=datetime.datetime.now()
today=datetime.date.today()

test_list = ['glue1_dns','glue2_dns','non_obsolete_glue2_appenv','glue2_services','glue1_endpoints','glue2_endpoints',\
             'glue2_service_types','glue1_endpoint_types','glue2_endpoint_types']

for test in test_list:
    output_file_name = "%s/%s.txt" % (path_to_output,test)
    output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
    for site_name in sorted(sites.wlcg_site_bdiis.keys()):

        command_glue1_dns              = "ldapsearch -LLL -x -h %s:2170 -b mds-vo-name=%s,o=grid dn | grep dn: | wc -l" \
                                          % (sites.wlcg_site_bdiis[site_name],site_name)
        command_glue2_dns              = "ldapsearch -LLL -x -h %s:2170 -b GLUE2DomainID=%s,o=glue dn | grep dn: | wc -l" \
                                          % (sites.wlcg_site_bdiis[site_name],site_name) 
        command_non_obsolete_glue2_appenv ="ldapsearch -LLL -x -h %s:2170 -b GLUE2DomainID=%s,o=glue \
                                            '(&(objectClass=GLUE2ApplicationEnvironment)(GLUE2EntityCreationTime=%s*))' \
                                            dn | grep dn: | wc -l" % (sites.wlcg_site_bdiis[site_name],site_name,today)
        command_glue2_services         = "ldapsearch -LLL -x -h %s:2170 -b GLUE2DomainID=%s,o=glue \
                                          '(objectClass=GLUE2Service)' GLUE2ServiceID | grep GLUE2ServiceID: \
                                          | sort | uniq | wc -l" % (sites.wlcg_site_bdiis[site_name],site_name)
        command_glue1_endpoints        = "ldapsearch -LLL -x -h %s:2170 -b mds-vo-name=%s,o=grid \
                                          '(objectClass=GlueService)' GlueServiceUniqueID | grep GlueServiceUniqueID: \
                                          | sort | uniq | wc -l" % (sites.wlcg_site_bdiis[site_name],site_name)
        command_glue2_endpoints        = "ldapsearch -LLL -x -h %s:2170 -b GLUE2DomainID=%s,o=glue \
                                          '(objectClass=GLUE2Endpoint)' \
                                          GLUE2EndpointID | grep GLUE2EndpointID: | sort | uniq | wc -l" \
                                          % (sites.wlcg_site_bdiis[site_name],site_name)
        command_glue2_service_types    = "ldapsearch -LLL -x -h %s:2170 -b GLUE2DomainID=%s,o=glue \
                                          '(objectClass=GLUE2Service)' GLUE2ServiceType | grep GLUE2ServiceType: \
                                          | sort | uniq | wc -l" % (sites.wlcg_site_bdiis[site_name],site_name)
        command_glue1_endpoint_types   = "ldapsearch -LLL -x -h %s:2170 -b mds-vo-name=%s,o=grid \
                                          '(objectClass=GlueService)' GlueServiceType | grep GlueServiceType: \
                                          | sort | uniq | wc -l" % (sites.wlcg_site_bdiis[site_name],site_name)
        command_glue2_endpoint_types   = "ldapsearch -LLL -x -h %s:2170 -b GLUE2DomainID=%s,o=glue \
                                          '(objectClass=GLUE2Endpoint)' GLUE2EndpointInterfaceName \
                                          | grep GLUE2EndpointInterfaceName: | sort | uniq | wc -l" \
                                          % (sites.wlcg_site_bdiis[site_name],site_name)

        test_dict = {
        'glue1_dns'                 :  command_glue1_dns,
        'glue2_dns'                 :  command_glue2_dns,
        'non_obsolete_glue2_appenv' :  command_non_obsolete_glue2_appenv,
        'glue2_services'            :  command_glue2_services, 
        'glue1_endpoints'           :  command_glue1_endpoints,
        'glue2_endpoints'           :  command_glue2_endpoints,
        'glue2_service_types'       :  command_glue2_service_types,
        'glue1_endpoint_types'      :  command_glue1_endpoint_types,
        'glue2_endpoint_types'      :  command_glue2_endpoint_types,
        }


        detail_file_name = "%s/%s/%s.html" % (path_to_output,test,site_name) 
        detail_url = "%s/%s/%s.html#%s" % (path_to_url,test,site_name,today)
   
        p = subprocess.Popen(test_dict[test] ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        if (results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1 or \
            results[0].find("ldap_bind") > -1 or results[0].find("No such object") > -1 or \
            results[0].find("Can't contact") > -1):
            color = "grey"
            result = "Unreachable" 
        else:
            color = "green"
            result = results[0].strip()
    
        detail_result_string="<a name=\"%s\">%s: %s</a><br>\n</body></html>" % (today,today,result)
        for line in fileinput.input(detail_file_name, inplace=True): 
            sys.stdout.write(line.replace('</body></html>', detail_result_string))
        result_string = "%s %s %s %s %s\n" % (dt,site_name,result,color,detail_url)
        os.write(output_fd,result_string)

    os.close(output_fd)

