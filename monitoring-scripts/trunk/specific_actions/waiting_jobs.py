#!/usr/bin/python
#
# Script to automatically track in GGUS those sites 
# that publish 4444444 WaitingJobs
#
##############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import fileinput
import ggus_monitor

def waiting_jobs (site_name, site_bdii, txt_fd, ggus_txt_fd, validator_output):

    # Getting detailed information for obsolete entries

    today=datetime.date.today()
    dt=datetime.datetime.now()
    file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/waiting_jobs/%s-wait.html" % (site_name)
    file_url = "http://malandes.web.cern.ch/malandes/ssb/wlcg/waiting_jobs/%s-wait.html#%s" % (site_name,today)
    html_results = ""
   
    index1=validator_output.find("Error:")
    index2=validator_output.find("UNKNOWN:")
    if (index1 > -1) or (index2 > -1):
        color = "grey"
        result = "Unreachable"
    else:
        index = validator_output.find("E022")
        if index > -1:
            color = "red"
            index_start = validator_output.find(":",index)
            index_end = validator_output.find("\n",index)
            result = validator_output[index_start+2:index_end]
            command_objects="ldapsearch -LLL -x -h %s -p 2170 -b GLUE2DomainID=%s,o=glue \
                             '(&(objectClass=GLUE2ComputingShare)(GLUE2ComputingShareWaitingJobs=444444))' dn \
                             | perl -p00e 's/\r?\n //g' | sed '/^$/d' | awk -F\"=\" '{print $(NF-4)}' | cut -d\"_\" -f1" % \
                             (site_bdii, site_name)
            p = subprocess.Popen(command_objects, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            results = p.communicate()
            full_text = results[0]
            index1=full_text.find("Error:")
            index2=full_text.find("UNKNOWN:")
            if (index1 > -1) or (index2 > -1):
                html_results = "Unable to contact site BDII\n<br>"
            else:
                if ( full_text == "" ):
                    full_text = "None\n"
                html_results = "Affected CEs: %s" % (full_text.replace("\n","<br>\n"))
            detail_result_string="<body>\n<a name=\"%s\">%s:<br>\n%s</a><br>\n" % (today,today,html_results)
            for line in fileinput.input(file_name, inplace=True):
                sys.stdout.write(line.replace('<body>\n', detail_result_string))
        else:
            color = "green"
            result = "0"

    os.write(txt_fd,"%s %s %s %s %s\n" % (dt,site_name,result,color,file_url))

    #######################################
    # Interacting with GGUS
    #######################################

    extra_condition = False
    detail_ggus = ""
    if ( color == "red" and full_text != "None\n" ):
        extra_condition = True
        detail_ggus = html_results.replace("<br>","")
            
    ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor(site_name, "waiting_jobs", \
                                             detail_ggus, extra_condition, "test") 

    os.write(ggus_txt_fd,"%s %s %s %s %s\n" % (dt,site_name,ggus_result,ggus_color,ggus_file_url))

