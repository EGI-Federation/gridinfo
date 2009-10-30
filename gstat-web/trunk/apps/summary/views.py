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
    predicate = {'Grid': 'SiteGrid', 
               'EGEE_ROC': 'SiteEgeeRoc', 
               'WLCG_TIER': 'SiteWlcgTier',
               'County': 'SiteCountry'
               }

    data = []
    if ( type == None ):
        type = 'Grid'
    
    if ( value == "ALL" ):
        entities = Entity.objects.filter(type=type)
        for entity in entities:
            site_list = getSitesInGroup(predicate[type], entity)
            group  = get_data_for_sites(site_list)
            summary = [str(entity.uniqueid), 0, 0, 0, 0, 0, 0, 0]
            for row in group:
                for i in range(7):
                    summary[i + 1] += row[i + 1]
            data.append(summary)       
    else:
        entity = Entity.objects.get(uniqueid__iexact=value, type=type)
        site_list = getSitesInGroup(predicate[type], entity)
        data = get_data_for_sites(site_list)

    if (output == 'json'):
        content = '{ "aaData": %s }' % (json.dumps(data))
        return HttpResponse(content, mimetype='application/json')  
    else:
        breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'}]
        thead = ["Name", "Logical CPUs", "Physical CPUs", "Total Space", "Used Space", "Running Jobs", "Waiting Jobs", "Total Jobs"]

        return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                        'filters_enabled': True,
                                                        'thead': thead})
def get_data_for_sites(site_list):
    data = [ ]
    for site in site_list:
        # Get installed capacities for site 
        (logical_cpus, physical_cpus)           = countCPUsInSite(site)
        (totalonlinesize, usedonlinesize, totalnearlinesize, usednearlinesize) = countStoragesInSite(site)
        (running_jobs, waiting_jobs, total_jobs) = countJobsInSite(site)
        site_name = str(site.uniqueid)
        total_size = totalonlinesize + totalnearlinesize
        used_size  = usedonlinesize + usednearlinesize
        
        row = [ site_name, 
                logical_cpus, 
                physical_cpus, 
                total_size, 
                used_size, 
                running_jobs, 
                waiting_jobs, 
                total_jobs ]
        data.append(row)

    return data

