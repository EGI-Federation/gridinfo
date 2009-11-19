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

def main(request, type='GRID', value='ALL', output=None):
    predicate = {'GRID'     : 'SiteGrid', 
                 'EGEE_ROC' : 'SiteEgeeRoc', 
                 'WLCG_TIER': 'SiteWlcgTier',
                 'Country'  : 'SiteCountry'}

    data = []
    
    if (value == "ALL"):
        # group list, ex: list of grid, list of roc, list of country
        groups = get_groups(type=type)
        for group in groups:
            site_list = get_sites(type=type, value=group.uniqueid)
            sites_data_rows  = get_data_for_sites(site_list)
            group_summary = [str(group.uniqueid), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for row in sites_data_rows:
                group_summary[1] += 1
                for i in range(9):
                    group_summary[i + 2] += row[i + 2]
            data.append(group_summary)       
    else:
        # site list
        site_list = get_sites(type, value)
        data = get_data_for_sites(site_list, get_status=True)

    if (output == 'json'):
        content = '{"aaData": %s}' % (json.dumps(data))
        return HttpResponse(content, mimetype='application/json')  
    else:
        breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'}]

        return render_to_response('single_table.html', {'summary_active'  : 1,
                                                        'breadcrumbs_list': breadcrumbs_list,
                                                        'type'            : type,
                                                        'value'           : value,
                                                        'filters_enabled' : True})
def get_data_for_sites(site_list, get_status=False):
    data = []
    nagios_status = {}
    for site in site_list:
        # Get installed capacities for site 
        site_name = str(site.uniqueid)
        
        service_list = get_services([site])
        sub_cluster_list = get_gluesubclusters(service_list)
        physical_cpu, logical_cpu = get_installed_capacity_cpu(sub_cluster_list)
        
        se_list = get_glueses(service_list)
        total_online, used_online, total_nearline, used_nearline = get_installed_capacity_storage(se_list)

        vo_view_list = get_gluevoview(service_list)
        total_jobs, running_jobs, waiting_jobs = get_job_stats(vo_view_list)        
        
        site_number_or_status = 0
        if get_status:
            if not nagios_status: nagios_status = get_nagios_status_dict()
            topbdii_list  = []
            sitebdii_list = []
            for service in service_list:
                if service.type == 'bdii_top':  topbdii_list.append(service)
                if service.type == 'bdii_site': sitebdii_list.append(service)       
            hostnames = [bdii.hostname for bdii in topbdii_list+sitebdii_list]
            (status, has_been_checked) = get_hosts_overall_nagios_status(nagios_status, hostnames, '^check-.+')
            site_number_or_status = get_nagios_status_str(status, has_been_checked)
            
        row = [ site_name,
                site_number_or_status,
                physical_cpu,
                logical_cpu,  
                total_online, 
                used_online, 
                total_nearline,
                used_nearline,
                total_jobs,
                running_jobs, 
                waiting_jobs]
        data.append(row)

    return data

