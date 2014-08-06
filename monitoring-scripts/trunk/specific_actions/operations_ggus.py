#!/usr/bin/python
#
# Script to automatically track GGUS tickets opened by the 
# Operations team
#
##############################################################

import os, sys
import datetime
import ggus_monitor
import sites


#########################
# CVMFS deployment
#########################

ops_cvmfs_ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/ops/ops_cvmfs_ggus.txt"
ops_cvmfs_ggus_output = os.open (ops_cvmfs_ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

dt=datetime.datetime.now()
extra_condition = False
detail_ggus = ""


for site_name in sorted(sites.wlcg_site_bdiis.keys()):
    #print "%s" % (site_name)

    ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor(site_name, "ops_cvmfs_ggus", \
                                                                       detail_ggus, extra_condition, "prod") 
    os.write(ops_cvmfs_ggus_output,"%s %s %s %s %s\n" % (dt,site_name,ggus_result,ggus_color,ggus_file_url))

#########################
# New VOMS server
#########################

ops_voms_ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/ops/ops_voms_ggus.txt"
ops_voms_ggus_output = os.open (ops_voms_ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

dt=datetime.datetime.now()
extra_condition = False
detail_ggus = ""


for site_name in sorted(sites.wlcg_site_bdiis.keys()):
    #print "%s" % (site_name)

    ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor(site_name, "ops_voms_ggus", \
                                                                       detail_ggus, extra_condition, "test")
    os.write(ops_voms_ggus_output,"%s %s %s %s %s\n" % (dt,site_name,ggus_result,ggus_color,ggus_file_url))


#########################
# Test
#########################

#ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor("WT2", "ops_cvmfs_ggus", "", False, "prod")
 
