
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from core.utils import *
from topology.models import Entityrelationship
from topology.models import Entity
from glue.models import glueservice

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

    vo_view_list = get_gluevoviews(service_list)
    total_jobs, running_jobs, waiting_jobs = get_voview_job_stats(vo_view_list)
    overview["Total Jobs"] = total_jobs
    overview["Running Jobs"] = running_jobs
    overview["Waiting Jobs"] = waiting_jobs

    data = []
    for  data_type in overview:
            data.append([data_type, overview[data_type] ])

    versions = get_service_versions(service_list)

    # Get SE Instances
    se_instances = {}
    se_instances_sites = {}
    for se in  se_list:
        if (se.implementationname.upper() ):
            name=se.implementationname.upper()
        else:
            name="Unknown"
        if (not se_instances.has_key(name)):
            se_instances[name] = 0
        se_instances[name] += 1

        if (se.gluesite_fk):
            site = se.gluesite_fk
        else:
            site = "Unknown"
        if (not se_instances_sites.has_key(name)):
            se_instances_sites[name] = {}
        if (not se_instances_sites[name].has_key(site)):
            se_instances_sites[name][site] = None


    
    se_types = []
    for name in se_instances.keys():
        row = [ name, se_instances[name], len(se_instances_sites[name]) ]
        se_types.append(row)

    fts_instances = glueservice.objects.filter(type='org.glite.FileTransfer')
    fts_versions = {}
    for instance in fts_instances:
        fts_versions[instance.uniqueid] = instance.version
    relationship = Entityrelationship.objects.select_related('subject','object').filter(object__type='org.glite.FileTransfer')
    fts_site_instances = []
    for relation in relationship:
        site_name=relation.subject.uniqueid
        service_unique_id = relation.object.uniqueid
        fts_site_instances.append([site_name, fts_versions[service_unique_id] ])
    

    breadcrumbs_list = [{'name':'Stats', 'url':'/gstat/stats/'}]
     
    return render_to_response('stats.html', {'stats_active': 1,
                                             'breadcrumbs_list': breadcrumbs_list,
                                             'filters_enabled': True,
                                             'type' :  type,
                                             'value' :  value,
                                             'data': data,
                                             'versions': versions,
                                             'se_types': se_types,
                                             'fts_site_instances': fts_site_instances,
                                             'os': os})


