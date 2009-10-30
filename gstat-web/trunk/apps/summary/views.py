from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
import gsutils
import socket
from django.utils import simplejson as json
from topology.models import Entity
from topology.models import Entityrelationship
from core.utils import *

def main(request, type=None, value=None, output=None):
    predicate = {'GRID'     : 'SiteGrid', 
                 'EGEE_ROC' : 'SiteEgeeRoc', 
                 'WLCG_TIER': 'SiteWlcgTier',
                 'Country'   : 'SiteCountry'}

    data = []
    if (type == None):
        type = 'GRID'
    
    if (value == "ALL" or value == None):
        # group list, ex: list of grid, list of roc, list of country
        groups = getEntitiesByType(type)
        for group in groups:
            site_list = getSitesInGroup(predicate[type], group)
            sites_data_rows  = get_data_for_sites(site_list)
            group_summary = [str(group.uniqueid), 0, 0, 0, 0, 0, 0, 0, 0]
            for row in sites_data_rows:
                group_summary[1] += 1
                for i in range(7):
                    group_summary[i + 2] += row[i + 2]
            data.append(group_summary)       
    else:
        # site list
        group = getEntityByUniqueidType(value, type)
        site_list = getSitesInGroup(predicate[type], group)
        data = get_data_for_sites(site_list, get_status=True)

    if (output == 'json'):
        content = '{"aaData": %s}' % (json.dumps(data))
        return HttpResponse(content, mimetype='application/json')  
    else:
        breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'}]

        return render_to_response('single_table.html', {'summary_active'  : 1,
                                                        'breadcrumbs_list': breadcrumbs_list,
                                                        'filters_enabled' : True})
def get_data_for_sites(site_list, get_status=False):
    data = []
    nagios_status = {}
    for site in site_list:
        # Get installed capacities for site 
        site_name = str(site.uniqueid)
        (logical_cpus, physical_cpus) = countCPUsInSite(site)
        (totalonlinesize, usedonlinesize, totalnearlinesize, usednearlinesize) = countStoragesInSite(site)
        total_size = totalonlinesize + totalnearlinesize
        used_size  = usedonlinesize + usednearlinesize
        (total_jobs, running_jobs, waiting_jobs) = countJobsInSite(site)
        site_number_or_status = 0
        if get_status:
            if not nagios_status: nagios_status = getNagiosStatusDict()
            topbdii_list  = getNodesInSite(site, 'bdii_top')
            sitebdii_list = getNodesInSite(site, 'bdii_site')
            hostnames = [bdii.hostname for bdii in topbdii_list+sitebdii_list]
            (status, has_been_checked) = getNodesOverallStatus(nagios_status, hostnames, '^check-.+')
            site_number_or_status = getNagiosStatusStr(status, has_been_checked)

        
        row = [ site_name,
                site_number_or_status,
                physical_cpus,
                logical_cpus,  
                total_size, 
                used_size, 
                total_jobs,
                running_jobs, 
                waiting_jobs]
        data.append(row)

    return data

