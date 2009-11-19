
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from core.utils import *

def main(request, type='GRID', value='ALL', output=None):

    overview = {}

    site_list = get_sites(type, value)
    overview["Sites"] = len(site_list) 

    country_list = get_countries(site_list)
    overview["Countries"] = len(country_list)

    service_list = get_services(site_list)
    overview["Services"] = len(service_list)

    vo_list = get_vos(service_list)
    overview["VOs"]= len(vo_list)

    sub_cluster_list = get_gluesubclusters(service_list)

    physical_cpu, logical_cpu = get_installed_capacity_cpu(sub_cluster_list)
    overview["Physical CPU"] = physical_cpu
    overview["Logical CPU"] = logical_cpu

    os = get_installed_capacity_per_os(sub_cluster_list)
    
    se_list = get_glueses(service_list)

    total_online, used_online, total_nearline, used_nearline = get_installed_capacity_storage(se_list)
    overview["Total Online"] = total_online 
    overview["Used Online"] = used_online
    overview["Total Nearline"] = total_nearline
    overview["Used Nearline"] = used_nearline

    vo_view_list = get_gluevoview(service_list)
    total_jobs, running_jobs, waiting_jobs = get_job_stats(vo_view_list)
    overview["Total Jobs"] = total_jobs
    overview["Running Jobs"] = running_jobs
    overview["Waiting Jobs"] = waiting_jobs

    data = []
    for  data_type in overview:
            data.append([data_type, overview[data_type] ])

    versions = get_service_versions(service_list)

    breadcrumbs_list = [{'name':'Stats', 'url':'/gstat/stats/'}]
     
    return render_to_response('stats.html', {'stats_active': 1,
                                             'breadcrumbs_list': breadcrumbs_list,
                                             'filters_enabled': True,
                                             'type' :  type,
                                             'value' :  value,
                                             'data': data,
                                             'versions': versions,
                                             'os': os})


