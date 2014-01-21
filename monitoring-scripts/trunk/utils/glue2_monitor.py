#!/usr/bin/python
#
# Library to monitor glue-validator results in the dashboard
#
###############################################################

import subprocess
import sys
from cStringIO import StringIO
import fileinput

def glue2_validator_monitor (site_name, site_bdii, file_name, file_url, date):

    path_to_command = "/afs/cern.ch/user/m/malandes/public/glue-validator/usr/bin"
    lines = iter(open(file_name,"r"))

    command_glue="%s/glue-validator -H %s -p 2170 -b GLUE2DomainID=%s,o=glue -v 2 -t 600 -k" % \
                 (path_to_command, site_bdii, site_name)

    p = subprocess.Popen(command_glue, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results = p.communicate()
    html_results = results[0].replace("\n","<br>\n")
    detail_result_string="<body>\n<a name=\"%s\">%s:<br>\n%s</a><br>\n" % (date,date,html_results)

    # Code to avoid duplicating the same log information
    first_line,_ = results[0].split("\n",1)
    for line in lines:
        if (line.find("Same as previous day") == -1 and line.find("html") == -1):
            line=lines.next()
            if (line.replace("<br>","").rstrip() == first_line.rstrip() ):
                detail_result_string="<body>\n<a name=\"%s\">%s: Same as previous day</a><br>\n" % (date,date)
            break

    for line in fileinput.input(file_name, inplace=True):
        sys.stdout.write(line.replace('<body>\n', detail_result_string))

    full_text = results[0]
    index1=full_text.find("Error:") 
    index2=full_text.find("UNKNOWN:") 
    if (index1 > -1) or (index2 > -1): 
        color = "grey"
        result = "Unreachable"
    else:
        first,_=full_text.split("\n",1) 
        end=first.split("|")
        error,warning,info=end[1].split(";")
        error_num = int(error.split("=")[1])
        warning_num = int(warning.split("=")[1])
        info_num = int(info.split("=")[1])
        if (error_num != 0):
           color = "red"
           result = "ERROR"
        elif (warning_num != 0):
            color  = "orange"
            result = "WARNING"
        elif (info_num != 0):
            color = "yellow"
            result = "INFO" 
        else:
            color = "green"
            result = "OK"

    return result,color,full_text

