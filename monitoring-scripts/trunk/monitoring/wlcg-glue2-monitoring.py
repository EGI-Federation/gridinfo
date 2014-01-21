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

path_to_command = "/afs/cern.ch/user/m/malandes/public/glue-validator/usr/bin"

# Obsolete entries file output definition
file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/obsolete_entries/obsolete_entries.txt"
ggus_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/obsolete_entries/ggus_obsolete_entries.txt"
output = os.open (file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
ggus_output = os.open (ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

for site_name in sorted(sites.wlcg_site_bdiis.keys()):

    dt=datetime.datetime.now()
    today=datetime.date.today()
    file_url = "http://malandes.web.cern.ch/malandes/ssb/wlcg/glue2/%s.html#%s" % (site_name,today)
    file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/glue2/%s.html" % (site_name)

    result, color, full_text = glue2_monitor.glue2_validator_monitor (site_name, sites.wlcg_site_bdiis[site_name], \
                                                                      file_name, file_url, today) 

    print ("%s %s %s %s %s" % (dt,site_name,result,color,file_url))

    # Obsolete entries
    obsolete_entries.obsolete_entries (site_name, sites.wlcg_site_bdiis[site_name], output, ggus_output, full_text) 

# Obsolete entries file output closing
os.close(output)
os.close(ggus_output)

