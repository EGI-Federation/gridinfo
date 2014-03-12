#!/usr/bin/python
#
# Script to monitor endpoints published in the BDII for ATLAS sites
#
# Note: In GLUE 2 xroot or http endpoints do not seem to publish the
# associated access policy, so endpoints published by the site are all
# considered 
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import sites

path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/atlas/endpoints"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/atlas/endpoints"

test_list = ['xroot_glue1','xroot_glue2','http_glue1','http_glue2']


for test in test_list:

    output_file_name = "%s/%s/%s.txt" % (path_to_output,test,test)
    output = os.open (output_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

    for site_name in sorted(sites.atlas_site_bdiis.keys()):
        detail_file_name = "%s/%s/%s" % (path_to_output,test,site_name)
        detail_output = os.open (detail_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
        detail_file_url = "%s/%s/%s" % (path_to_url,test,site_name)
        dt=datetime.datetime.now()

        command_xroot_glue1 = "for i in `ldapsearch -x -LLL -h %s -b  mds-vo-name=%s,o=grid '(&(objectClass=GlueSA)\
                               (GlueSAAccessControlBaseRule=*atlas*))' GlueChunkKey | grep GlueChunkKey: | \
                                cut -d\"=\" -f2 | sort | uniq`; do ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid \
                                '(&(objectClass=GlueSEAccessProtocol)(|(GlueSEAccessProtocolType=root)\
                               (GlueSEAccessProtocolType=xroot)(GlueSEAccessProtocolType=xrootd)))' \
                                GlueSEAccessProtocolEndpoint | grep GlueSEAccessProtocolEndpoint: | \
                                cut -d\":\" -f2-; done" % \
                               (sites.atlas_site_bdiis[site_name], site_name, sites.atlas_site_bdiis[site_name], site_name)

        command_xroot_glue2 = "ldapsearch -x -LLL -h %s -b GLUE2DomainID=%s,o=glue \
                              '(&(objectClass=GLUE2Endpoint)(GLUE2EndpointInterfaceName=xroot))' GLUE2EndpointURL | \
                               grep GLUE2EndpointURL: | cut -d\":\" -f2-" % \
                               (sites.atlas_site_bdiis[site_name], site_name)

        command_http_glue1 = "for i in `ldapsearch -x -LLL -h %s -b  mds-vo-name=%s,o=grid '(&(objectClass=GlueSA)\
                               (GlueSAAccessControlBaseRule=*atlas*))' GlueChunkKey | grep GlueChunkKey: | \
                                cut -d\"=\" -f2 | sort | uniq`; do ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid \
                                '(&(objectClass=GlueSEAccessProtocol)(|(GlueSEAccessProtocolType=http)\
                               (GlueSEAccessProtocolType=https)))' GlueSEAccessProtocolEndpoint | \
                                grep GlueSEAccessProtocolEndpoint: | cut -d\":\" -f2-; done" % \
                               (sites.atlas_site_bdiis[site_name], site_name, sites.atlas_site_bdiis[site_name], site_name)

        command_http_glue2 = "ldapsearch -x -LLL -h %s -b GLUE2DomainID=%s,o=glue \
                              '(&(objectClass=GLUE2Endpoint)(|(GLUE2EndpointInterfaceName=http)\
                               (GLUE2EndpointInterfaceName=https)))' GLUE2EndpointURL | \
                               grep GLUE2EndpointURL: | cut -d\":\" -f2-" % \
                               (sites.atlas_site_bdiis[site_name], site_name)

        test_dict = {
        'xroot_glue1' : command_xroot_glue1,
        'xroot_glue2' : command_xroot_glue2,
        'http_glue1'  : command_http_glue1,
        'http_glue2'  : command_http_glue1
        }

        p = subprocess.Popen(test_dict[test], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        full_text = p.communicate()[0]
        os.write(detail_output,full_text)
        os.close(detail_output)
        if (full_text == ""):
            color = "red"
            result = "None" 
        else:
            index1=full_text.find("Error:") 
            index2=full_text.find("UNKNOWN:") 
            index3=full_text.find("No such object")
            index4=full_text.find("Can't contact")
            if (index1 > -1) or (index2 > -1) or (index3 > -1) or (index4 > -1): 
                color = "grey"
                result = "Unreachable"
            else:
                color = "green"
                result = "OK"

        result_string = "%s %s %s %s %s\n" % (dt,site_name,result,color,detail_file_url)
        os.write(output,result_string)

    os.close(output)


