from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils import html
from glue.models import glueservice
from core.utils import *
import gsutils
import socket
import re
import time
   
def overview(request, site_name):     

    # Get the site information from glue database
    entity = getGlueEntity('gluesite', uniqueids_list=[site_name])
    if not entity:
        #raise Http404
        gluesite = "N/A"
    else:
        gluesite = entity[0]
        gluesite.sysadmincontact = str(gluesite.sysadmincontact).split(":")[-1]      
        gluesite.usersupportcontact = str(gluesite.usersupportcontact).split(":")[-1]
        gluesite.securitycontact = str(gluesite.securitycontact).split(":")[-1]

    # Get all the service and entity at site from topology database
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    service_list = get_services([site_entity])
    topbdii_list  = []
    sitebdii_list = []
    ce_list       = []
    se_list       = []
    for service in service_list:
        if service.type == 'bdii_top':  topbdii_list.append(service)
        if service.type == 'bdii_site': sitebdii_list.append(service)
        if service.type == 'CE':        ce_list.append(service)
        if service.type == 'SE':        se_list.append(service)
    last_update = time.mktime(time.strptime(str(site_entity.updated_at), "%Y-%m-%d %H:%M:%S"))
    minutes_ago = int((time.mktime(time.localtime()) - time.mktime(time.strptime(str(site_entity.updated_at), "%Y-%m-%d %H:%M:%S")))/60)
    
    # Count the numbers of entities
    count_dict             = {}
    count_dict['topbdii']  = len(topbdii_list)
    count_dict['sitebdii'] = len(sitebdii_list)
    count_dict['ce']       = len(ce_list)
    count_dict['se']       = len(se_list)
    count_dict['service']  = len(service_list)
    
    # Get the overall monitoring and validation results
    nagios_status = getNagiosStatusDict()
    overall_status_dict             = {}
    hostnames = [topbdii.hostname for topbdii in topbdii_list]
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-bdii.+')
    overall_status_dict['topbdii']  = getNagiosStatusStr(status, has_been_checked)
    hostnames = [sitebdii.hostname for sitebdii in sitebdii_list]
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-bdii.+')
    overall_status_dict['sitebdii'] = getNagiosStatusStr(status, has_been_checked)
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-ce$')
    overall_status_dict['ce']       = getNagiosStatusStr(status, has_been_checked)
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-se$')
    overall_status_dict['se']       = getNagiosStatusStr(status, has_been_checked)
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-service$')
    overall_status_dict['service']  = getNagiosStatusStr(status, has_been_checked)
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-site$')
    overall_status_dict['site']     = getNagiosStatusStr(status, has_been_checked)


    # Count the CPU and Jobs numbers in all CEs and the storage space in all SEs at site
    installed_capacity = {}
    sub_cluster_list = get_subclusters(service_list)
    physical_cpu, logical_cpu = get_installed_capacity_cpu(sub_cluster_list)
    installed_capacity['physicalcpus']      = physical_cpu
    installed_capacity['logicalcpus']       = logical_cpu
    
    se_list = get_ses(service_list)
    total_online, used_online, total_nearline, used_nearline = get_installed_capacity_storage(se_list)
    installed_capacity['totalonlinesize']   = total_online
    installed_capacity['usedonlinesize']    = used_online
    installed_capacity['totalnearlinesize'] = total_nearline
    installed_capacity['usednearlinesize']  = used_nearline
    
    vo_jobs = []
    vo_view_list = get_vo_view(service_list)
    for vo_view in vo_view_list:
        job_dict = {}
        total_jobs, running_jobs, waiting_jobs = get_job_stats([vo_view])   
        job_dict['voname']      = vo_view.localid
        job_dict['totaljobs']   = total_jobs
        job_dict['runningjobs'] = running_jobs
        job_dict['waitingjobs'] = waiting_jobs
        vo_jobs.append(job_dict)
    
    return render_to_response('overview.html', {'sitename'           : site_name,
                                                'gluesite'           : gluesite,
                                                'count_dict'         : count_dict,
                                                'overall_status_dict': overall_status_dict,
                                                'installed_capacity' : installed_capacity,
                                                'vo_jobs'            : vo_jobs,
                                                'last_update'        : last_update,
                                                'minutes_ago'        : minutes_ago})
    
def status(request, site_name, type):
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    if not site_entity:
        #raise Http404 
        pass

    service_list = get_services([site_entity])
    nodetype = 'bdii_site'
    if type == 'topbdii': nodetype = 'bdii_top'
    bdii_list  = []
    for service in service_list:
        if service.type == nodetype:  bdii_list.append(service)
    hostnames  = [bdii.hostname for bdii in bdii_list]
    hostname_list = []
    for hostname in hostnames:
        hosts_from_alias = get_hosts_from_alias(hostname)
        if ( len(hosts_from_alias) > 1 ):
            #This is and alias point to more than on reall hostname
            hostname_list += hosts_from_alias
        elif not ( hostname == hosts_from_alias[0]):
            #This is an alias for a single instance
            hostname_list += hosts_from_alias
        else:
            #The actual id given was a real host.
            hostname_list.append(hostname)
            
    nagios_status = getNagiosStatusDict()         
    status_list = []
    for hostname in hostname_list:
        if type == 'topbdii':
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-freshness', hostname) )
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-sites', hostname) )
        elif type == 'sitebdii':
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-freshness', hostname) )
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-services', hostname) )
        elif type == 'ce':
            status_list.append( getNagiosStatus(nagios_status, 'check-ce', hostname) )
        elif type == 'se':
            status_list.append( getNagiosStatus(nagios_status, 'check-se', hostname) )
        elif type == 'service':
            status_list.append( getNagiosStatus(nagios_status, 'check-service', hostname) )
        elif type == 'site':
            status_list.append( getNagiosStatus(nagios_status, 'check-site', hostname) )
    
    if type in ['topbdii', 'sitebdii']:
        check_type = 'monitoring'
    else:
        check_type = 'validation'

    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_list' : status_list,
                                              'check_type'  : check_type})


"""
def getStatusList(site_name, search_phrase, node_type):
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    if not site_entity:
        raise Http404 

    hostname_list  = [node.hostname for node in getNodesInSite(site_entity, node_type)]
    nagios_status = getNagiosStatusDict()
    status_list = []
    
    for hostname in hostname_list:
        try:
            for check in nagios_status[hostname].keys():
                status_dict = {}
                if re.compile(search_phrase).match(check):
                    status_dict['hostname']           = hostname
                    status_dict['check']              = check
                    current_state                     = nagios_status[hostname][check]['current_state']
                    has_been_checked                  = nagios_status[hostname][check]['has_been_checked']
                    status_dict['current_state']      = getNagiosStatusStr(current_state, has_been_checked)
                    status_dict['plugin_output']      = nagios_status[hostname][check]['plugin_output']
                    status_dict['long_plugin_output'] = nagios_status[hostname][check]['long_plugin_output']
                    status_dict['last_check']         = nagios_status[hostname][check]['last_check']
                if status_dict:
                    status_list.append(status_dict)
        except (KeyError):
            pass
    return status_list    
"""

# ------------------------------------
# -- RRD graphs HTML pages function --
# ------------------------------------
def site_graphs(request, site_name, attribute):
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    service_list = get_services([site_entity])
    sub_cluster_list = get_subclusters(service_list)
    se_list = get_ses(service_list)
    
    if attribute == 'cpu':
        objects = sub_cluster_list
    elif attribute in ['online','nearline']:
        objects = se_list
    
    return render_to_response('site_graphs.html', {'site_name': site_name,
                                                   'objects'  : objects,
                                                   'attribute': attribute}) 

def vo_graphs(request, site_name, attribute, vo_name):
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    service_list = get_services([site_entity])
    ce_list = []
    for service in service_list:
        if service.type == 'CE': ce_list.append(service)
    objects = ce_list
        

    return render_to_response('vo_graphs.html', {'site_name': site_name,
                                                 'objects'  : objects,
                                                 'attribute': attribute,
                                                 'vo_name'  : vo_name}) 
