#!/usr/bin/python
#
# Script to monitor maxCPUTime GLUE 2 attribute for LHCb sites
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import sites
import ggus_monitor

path_to_command = "/afs/cern.ch/user/m/malandes/public/glue-validator/usr/bin/"
path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/lhcb/maxCPUTime/"
path_to_temp = "/afs/cern.ch/user/m/malandes/temp/ssb/lhcb/"
ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/lhcb/maxCPUTime/ggus_maxCPUTime.txt"
ggus_output = os.open (ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

for site_name in sorted(sites.lhcb_site_bdiis.keys()):
    file_name = "%s%s" % (path_to_output,site_name)
    ldif_file = "%sldif" % (path_to_temp)
    share_file = "%sshare" % (path_to_temp)
    output = os.open (file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
    share = os.open (share_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
    ldif = os.open (ldif_file, os.O_CREAT | os.O_TRUNC, 0600)
    os.close(ldif)
    file_url = "http://malandes.web.cern.ch/malandes/ssb/lhcb/maxCPUTime/%s" % (site_name)
    dt=datetime.datetime.now()

    command_mappol = "ldapsearch -LLL -x -h %s -p 2170 -b GLUE2DomainID=%s,o=glue \
                     '(&(objectClass=GLUE2MappingPolicy)(GLUE2PolicyRule=*lhcb*))' GLUE2MappingPolicyShareForeignKey \
                     | perl -p00e 's/\r?\n //g' | grep GLUE2MappingPolicyShareForeignKey: | cut -d\":\" -f2-" % \
                     (sites.lhcb_site_bdiis[site_name], site_name)
    p = subprocess.Popen(command_mappol, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results = p.communicate()
    os.write(share,results[0])
    os.close(share)
    if (results[0] == ""):
        color = "pink"
        result = "Missing_LHCb_queues" 
    else:
        share = open (share_file, 'r')
        for line in share:
            command_maxcpu = "ldapsearch -LLL -x -h %s -p 2170 -b GLUE2DomainID=%s,o=glue \
                             '(&(objectClass=GLUE2ComputingShare)(GLUE2ShareID=%s))'" % \
                             (sites.lhcb_site_bdiis[site_name], site_name, line.strip())  
    
            p = subprocess.Popen(command_maxcpu, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            results = p.communicate()
            ldif = open(ldif_file, 'a')
            ldif.write(results[0])
        share.close()
        ldif.close()
        command_glue="%sglue-validator -f %s -s lhcb -v 3" % \
                     (path_to_command , ldif_file)
        p = subprocess.Popen(command_glue, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        os.write(output,results[0])
        os.close(output)
        full_text = results[0]

        index1=full_text.find("Error:") 
        index2=full_text.find("UNKNOWN:") 
        if (index1 > -1) or (index2 > -1): 
            color = "grey"
            result = "Unreachable"
        else:
            info_code=full_text.find("I029")
            if (info_code > -1):
               color = "red"
               result = "ERROR"
            else:
               color = "green"
               result = "OK"

    print ("%s %s %s %s %s" % (dt,sites.lhcb_names_dict[site_name],result,color,file_url))


    #######################################
    # Interacting with GGUS
    #######################################

    extra_condition = False
    detail_ggus = ""
    if ( color == "red" ):
        extra_condition = True

    ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor(site_name, "maxCPUTime", \
                                             full_text, extra_condition)

    os.write(ggus_output,"%s %s %s %s %s\n" % (dt,sites.lhcb_names_dict[site_name],ggus_result,ggus_color,ggus_file_url))


os.remove(ldif_file)
os.remove(share_file)


