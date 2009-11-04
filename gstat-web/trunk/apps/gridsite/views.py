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
from django.core.serializers import serialize
   
def overview(request, site_name):     
    # add exception here in case of empty queryset
    # Get the site information
    entity = getGlueEntity('gluesite', uniqueids_list=[site_name])
    if not entity:
        #raise Http404
        gluesite = "N/A"
    else:
        gluesite = entity[0]
        gluesite.sysadmincontact = str(gluesite.sysadmincontact).split(":")[-1]      
        gluesite.usersupportcontact = str(gluesite.usersupportcontact).split(":")[-1]
        gluesite.securitycontact = str(gluesite.securitycontact).split(":")[-1]
        
    
    
    
    # Get all the service and entity at site
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    topbdii_list  = getNodesInSite(site_entity, 'bdii_top')
    sitebdii_list = getNodesInSite(site_entity, 'bdii_site')
    ce_list       = getNodesInSite(site_entity, 'CE')
    se_list       = getNodesInSite(site_entity, 'SE')
    service_list  = getServicesInSite(site_entity)
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
    (logicalcpus, physicalcpus)             = countCPUsInSite(site_entity)
    installed_capacity['physicalcpus']      = physicalcpus
    installed_capacity['logicalcpus']       = logicalcpus
    (totalonlinesize, usedonlinesize, totalnearlinesize, usednearlinesize) = countStoragesInSite(site_entity)
    installed_capacity['totalonlinesize']   = totalonlinesize
    installed_capacity['usedonlinesize']    = usedonlinesize
    installed_capacity['totalnearlinesize'] = totalnearlinesize
    installed_capacity['usednearlinesize']  = usednearlinesize
    #(totaljobs, runningjobs, waitingjobs) = countJobsInSite(site_entity)
    #installed_capacity['runningjobs']     = runningjobs
    #installed_capacity['waitingjobs']     = waitingjobs
    #installed_capacity['totaljobs']       = totaljobs
    
    #vo_list = getVOsInSite(site_entity)
    vo_list = countJobsInVO_Site(site_entity)
    
    return render_to_response('overview.html', {'sitename'           : site_name,
                                                'gluesite'           : gluesite,
                                                'count_dict'         : count_dict,
                                                'overall_status_dict': overall_status_dict,
                                                'installed_capacity' : installed_capacity,
                                                'vo_list'            : vo_list,
                                                'last_update'        : last_update,
                                                'minutes_ago'        : minutes_ago})
    
def status(request, site_name, type):
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    if not site_entity:
        #raise Http404 
        pass
    
    nodetype = 'bdii_site'
    if type == 'topbdii': nodetype = 'bdii_top'

    hostnames  = [node.hostname for node in getNodesInSite(site_entity, nodetype)]
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
    if attribute == 'cpu':
        ce_list  = getNodesInSite(site_entity, 'CE')
        objects = getSubClusterByCluster(cluster_uniqueids_list=[ce.uniqueid for ce in ce_list])
    elif attribute in ['online','nearline']:
        se_list = getNodesInSite(site_entity, 'SE')
        objects = getGlueEntity(model_name='gluese', uniqueids_list=[se.uniqueid for se in se_list])
        

    return render_to_response('site_graphs.html', {'site_name': site_name,
                                              'objects'  : objects,
                                              'attribute': attribute}) 

def vo_graphs(request, site_name, attribute, vo_name):
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    objects = getNodesInSite(site_entity, 'CE')
        

    return render_to_response('vo_graphs.html', {'site_name': site_name,
                                                 'objects'  : objects,
                                                 'attribute': attribute,
                                                 'vo_name'  : vo_name}) 
