#!/usr/bin/python
#
# Script to monitor BDII deployment
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import fileinput

path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/bdii"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/bdii" 
dt=datetime.datetime.now()
today=datetime.date.today()

total = {
'bdii_site' : 0,
'bdii_top' : 0
}

for version in ["5.2.10", "5.2.12", "5.2.13", "5.2.17", "5.2.20", "5.2.21", "5.2.22"]:
    output_file_name = "%s/%s.txt" % (path_to_output,version) 
    output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT, 0600)
    for bdii in ["bdii_site", "bdii_top"]:
        detail_file_name = "%s/%s-%s.html" % (path_to_output,bdii,version) 
        detail_url = "%s/%s-%s.html#%s" % (path_to_url,bdii,version,today)

        command = "ldapsearch -LLL -x -h lcg-bdii -p 2170 -b GLUE2GroupID=grid,o=glue \
                   '(&(objectClass=GLUE2Endpoint)(GLUE2EndpointInterfaceName=%s)\
                    (GLUE2EndpointImplementationVersion=%s))' GLUE2EndpointImplementationVersion \
                   | grep GLUE2EndpointImplementationVersion | wc -l" % (bdii,version)

        p = subprocess.Popen(command ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        if (results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1 ):
            color = "grey"
            result = "Unreachable" 
        else:
            color = "green"
            result = results[0].strip()
            total[bdii] = total[bdii] + int (result)

        detail_result_string="<a name=\"%s\">%s: %s</a><br>\n</body></html>" % (today,today,result)
        for line in fileinput.input(detail_file_name, inplace=True): 
            sys.stdout.write(line.replace('</body></html>', detail_result_string))
        result_string = "%s %s %s %s %s\n" % (dt,bdii,result,color,detail_url)
        os.write(output_fd,result_string)
    os.close(output_fd)

output_file_name = "%s/bdii.txt" % (path_to_output)
output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT, 0600)
for bdii in ["bdii_site", "bdii_top"]:
    detail_file_name = "%s/%s.html" % (path_to_output,bdii)
    detail_url = "%s/%s.html#%s" % (path_to_url,bdii,today)
    if ( total[bdii] == 0 ):
        color = "grey"
        result = "Unreachable"
    else: 
        color = "green"
        result = total[bdii]
    detail_result_string="<a name=\"%s\">%s: %s</a><br>\n</body></html>" % (today,today,result)
    for line in fileinput.input(detail_file_name, inplace=True):
        sys.stdout.write(line.replace('</body></html>', detail_result_string))
    result_string = "%s %s %s %s %s\n" % (dt,bdii,result,color,detail_url)
    os.write(output_fd,result_string)
os.close(output_fd)
