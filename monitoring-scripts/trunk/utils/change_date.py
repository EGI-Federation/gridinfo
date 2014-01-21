#!/usr/bin/python
#
# Script to change the date of detailed output files
#
###############################################################

import sys
import sites
import fileinput

old = "<a name=\"2014-01-17\">2014-01-17:<br>"
new = "<a name=\"2014-01-16\">2014-01-16:<br>"

for site_name in sorted(sites.wlcg_site_bdiis.keys()):
    file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/obsolete_entries/%s-obs.html" % (site_name)
    for line in fileinput.input(file_name, inplace=True):
        sys.stdout.write(line.replace(old,new))

    file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/%s.html" % (site_name)
    for line in fileinput.input(file_name, inplace=True):
        sys.stdout.write(line.replace(old,new))

