#!/usr/bin/python
#
# Script to monitor GLUE 2 validation in WLCG
#
###############################################################

import os
import datetime
from cStringIO import StringIO
import sites
import glue2_monitor
import obsolete_entries
import waiting_jobs

path_to_command = "/afs/cern.ch/user/m/malandes/public/glue-validator/usr/bin"

# Obsolete entries file output definition
#obs_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/obsolete_entries/obsolete_entries.txt"
#obs_ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/obsolete_entries/ggus_obsolete_entries.txt"
#obs_output = os.open (obs_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
#obs_ggus_output = os.open (obs_ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

# Waiting jobs file output definition
wait_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/waiting_jobs/waiting_jobs.txt"
wait_ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/waiting_jobs/ggus_waiting_jobs.txt"
wait_output = os.open (wait_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
wait_ggus_output = os.open (wait_ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)


for site_name in sorted(sites.wlcg_site_bdiis.keys()):

    dt=datetime.datetime.now()
    today=datetime.date.today()
    file_url = "http://malandes.web.cern.ch/malandes/ssb/wlcg/glue2/%s.html#%s" % (site_name,today)
    file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/glue2/%s.html" % (site_name)

    result, color, full_text = glue2_monitor.glue2_validator_monitor (site_name, sites.wlcg_site_bdiis[site_name], \
                                                                      file_name, file_url, today) 

    print ("%s %s %s %s %s" % (dt,site_name,result,color,file_url))

    # Obsolete entries
    #obsolete_entries.obsolete_entries (site_name, sites.wlcg_site_bdiis[site_name], obs_output, obs_ggus_output, full_text) 

    # Waiting jobs
    waiting_jobs.waiting_jobs (site_name, sites.wlcg_site_bdiis[site_name], wait_output, wait_ggus_output, full_text)

# Obsolete entries file output closing
#os.close(obs_output)
#os.close(obs_ggus_output)

# Waiting jobs file output closing
os.close(wait_output)
os.close(wait_ggus_output)


