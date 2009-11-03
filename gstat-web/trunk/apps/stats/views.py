
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from topology.models import Entity
from topology.models import Entityrelationship
from glue.models import *
from core.utils import *

def main(request, type='GRID', value=None, output=None):

    overview = {}

    site_list = get_sites(type, value)
    overview["Sites"] = len(site_list) 

    country_list = get_countries(site_list)
    overview["Countries"] = len(country_list)

    service_list = get_services(site_list)
    overview["Services"] = len(service_list)

    vo_list = get_VOs(service_list)
    overview["VOs"]= len(vo_list)

    sub_cluster_list = get_subclusters(service_list)

    physical_cpu, logical_cpu = get_installed_capacity_cpu(sub_cluster_list)
    overview["Physical CPU"] = physical_cpu
    overview["Logical CPU"] = logical_cpu

    os = get_installed_capacity_per_os(sub_cluster_list)
    
    se_list = get_SEs(service_list)

    total_online, used_online, total_nearline, used_nearline = get_installed_capacity_storage(se_list)
    overview["Total Online"] = total_online 
    overview["Used Online"] = used_online
    overview["Total Nearline"] = total_nearline
    overview["Used Nearline"] = used_nearline

    vo_view_list = get_vo_view(service_list)
    total_jobs, running_jobs, waiting_jobs = get_job_stats(vo_view_list)
    overview["Total Jobs"] = total_jobs
    overview["Running Jobs"] = running_jobs
    overview["Waiting Jobs"] = waiting_jobs

    data = []
    for  type in overview:
            data.append([type, overview[type] ])

    versions = get_service_versions(service_list)

    breadcrumbs_list = [{'name':'Stats', 'url':'/gstat/stats/'}]
     
    return render_to_response('stats.html', {'stats_active': 1,
                                             'breadcrumbs_list': breadcrumbs_list,
                                             'filters_enabled': True,
                                             'data': data,
                                             'versions': versions,
                                             'os': os})

def get_sites(type=None, value=None):
    predicate = {'GRID': 'SiteGrid', 
               'EGEE_ROC': 'SiteEgeeRoc', 
               'WLCG_TIER': 'SiteWlcgTier',
               'Country': 'SiteCountry'}
    
    if ( value == "ALL"):
        #entities = Entity.objects.filter(type=type)
        entities = getEntitiesByType(type)
        site_list = [] 
        for entity in entities:
            site_list.extend(getSitesInGroup(predicate[type], entity))
    else:
        #entity = Entity.objects.filter(uniqueid=value, type=type)
        entity = getEntityByUniqueidType(value, type)
        site_list = getSitesInGroup(predicate[type], entity)
    return site_list


def get_countries(site_list):
    relationships = Entityrelationship.objects.filter(predicate = 'SiteCountry', subject__in = site_list)
    countries = []
    for relation in relationships:
        try:
            countries.index(relation.object.uniqueid)
        except:    
            countries.append(relation.object.uniqueid)
    return countries

def get_services(site_list):
    relationships = Entityrelationship.objects.filter(predicate = 'SiteService', subject__in = site_list)
    services = []
    for relation in relationships:
        services.append(relation.object)
    return services

def get_VOs(service_list):
    relationships = Entityrelationship.objects.filter(predicate = 'ServiceVO', subject__in = service_list)
    vos = []
    for relation in relationships:
        try:
            vos.index(relation.object.uniqueid)
        except:    
            vos.append(relation.object.uniqueid)
    return vos

def get_subclusters(service_list):
    uniqueids = [service.uniqueid for service in service_list]
    clusters = Entity.objects.filter(type = 'CE', uniqueid__in = uniqueids)
    uniqueids = [cluster.uniqueid for cluster in clusters]
    sub_clusters = gluesubcluster.objects.filter(gluecluster_fk__in = uniqueids)
    return sub_clusters

def get_SEs(service_list):
    uniqueids = [service.uniqueid for service in service_list]
    SEs = Entity.objects.filter(type = 'SE', uniqueid__in = uniqueids)
    uniqueids = [se.uniqueid for se in SEs]
    se_list = gluese.objects.filter(uniqueid__in = uniqueids)
    return se_list

def get_installed_capacity_cpu(sub_clusters_list):
    physical_cpus = 0
    logical_cpus = 0
    for sub_cluster in sub_clusters_list:
        logical_cpus += int(sub_cluster.logicalcpus)
        physical_cpus += int(sub_cluster.physicalcpus)

    return [physical_cpus, logical_cpus]


def get_installed_capacity_storage(se_list):
    total_online = 0
    used_online = 0
    total_nearline = 0
    used_nearline = 0 

    for se in se_list:
        try:
            total_online += int(se.totalonlinesize)
            used_online += int(se.usedonlinesize)
            total_nearline += int(se.totalnearlinesize) 
            used_nearline += int(se.usednearlinesize) 
        except ValueError:
            pass
    return [ total_online, used_online, total_nearline, used_nearline ]

def get_installed_capacity_per_os(sub_clusters_list):
    os = {}
    for sub_cluster in sub_clusters_list:
        os_name = sub_cluster.operatingsystemname
        index = sub_cluster.operatingsystemrelease.find(".")
        if (index > -1) :
            os_release = sub_cluster.operatingsystemrelease[:index]
        else:
            os_release = "?"

        if ( not os.has_key(os_name)):
            os[os_name] = {}
        if ( not os[os_name].has_key(os_release)):
            os[os_name][os_release] = [0, 0]

        os[os_name][os_release][0] += int(sub_cluster.physicalcpus)    
        os[os_name][os_release][1] += int(sub_cluster.logicalcpus)

    data = []
    keys = os.keys()
    keys.sort()
    for  name in keys:
        for release in os[name]:
            data.append([name, release, os[name][release][0], os[name][release][1]])

    return data


def get_vo_view(service_list):
    uniqueids = [service.uniqueid for service in service_list]
    clusters = Entity.objects.filter(type = 'CE', uniqueid__in = uniqueids)
    uniqueids = [cluster.uniqueid for cluster in clusters]
    CEs = gluece.objects.filter(gluecluster_fk__in = uniqueids)
    uniqueids = [ce.uniqueid for ce in CEs]
    VO_views = gluevoview.objects.filter(gluece_fk__in = uniqueids)

    return VO_views

def get_job_stats(vo_view_list):
    total_jobs = 0
    running_jobs = 0
    waiting_jobs = 0
    for voview in vo_view_list:
        total_jobs += int(voview.totaljobs)
        running_jobs += int(voview.runningjobs)
        if ( not int(voview.waitingjobs) == 444444):
            waiting_jobs += int(voview.waitingjobs)
    return  [ total_jobs, running_jobs, waiting_jobs ]

def get_service_versions(service_list):
    uniqueids = [service.uniqueid for service in service_list]
    glue_service_list = glueservice.objects.filter(uniqueid__in = uniqueids)

    services = {}
    for service in glue_service_list:
        type = service.type.lower()
        version = service.version
        if ( not services.has_key(type)):
            services[type] = {}
        if ( not services[type].has_key(version)):
            services[type][version] = 0

        services[type][version] += 1    

    data = []
    keys = services.keys()
    keys.sort()
    for  type in keys:
        for version in services[type]:
            data.append([type, version, services[type][version] ])

    return data
