#!/usr/bin/python
#
# Script to monitor GLUE 2 validation in LHCb sites
#
###############################################################

import datetime
from cStringIO import StringIO
import sites
import glue2_monitor
import obsolete_entries

path_to_command = "/afs/cern.ch/user/m/malandes/public/glue-validator/usr/bin"

for site_name in sorted(sites.lhcb_site_bdiis.keys()):

    dt=datetime.datetime.now()
    today=datetime.date.today()
    file_url = "http://malandes.web.cern.ch/malandes/ssb/lhcb/glue2/%s.html#%s" % (sites.lhcb_names_dict[site_name],today)
    file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/lhcb/glue2/%s.html" % (sites.lhcb_names_dict[site_name])

    result, color, full_text = glue2_monitor.glue2_validator_monitor (site_name, sites.lhcb_site_bdiis[site_name], \
                                                                      file_name, file_url) 

    print ("%s %s %s %s %s" % (dt,sites.lhcb_names_dict[site_name],result,color,file_url))

