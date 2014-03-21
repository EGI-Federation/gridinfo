#!/usr/bin/python
#
# Script to automatically track GGUS tickets opened by the 
# GLUE 2 validator Nagios probe
#
##############################################################

import os, sys
import datetime
import ggus_monitor
import sites

nagios_ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/nagios/nagios_ggus.txt"
nagios_ggus_output = os.open (nagios_ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

#######################################
# Interacting with GGUS
#######################################

dt=datetime.datetime.now()
extra_condition = False
detail_ggus = ""


for site_name in sorted(sites.wlcg_site_bdiis.keys()):
    print "%s" % (site_name)

    ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor(site_name, "nagios_ggus", \
                                                                       detail_ggus, extra_condition, "prod") 
    os.write(nagios_ggus_output,"%s %s %s %s %s\n" % (dt,site_name,ggus_result,ggus_color,ggus_file_url))
