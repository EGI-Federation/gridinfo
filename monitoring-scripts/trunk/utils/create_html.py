#!/usr/bin/python
#
# Script to create for the first time, the html files that are  
# used for detailed output.
#
###############################################################

import os
import sites

for site_name in sorted(sites.lhcb_site_bdiis.keys()):

    output_file_name = "/afs/cern.ch/user/m/malandes/www/web/ssb/lhcb/glue2/%s.html" % (sites.lhcb_names_dict[site_name])
    output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
    html_code = "<html><head><title>GLUE 2 validation results for %s</title></head><body>\n</body></html>" % \
                 (sites.lhcb_names_dict[site_name])
    os.write(output_fd,html_code)
    os.close(output_fd)


