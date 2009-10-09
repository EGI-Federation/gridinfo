from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils import html
from glue.models import glueservice
from summary.utils import *
import gsutils
import socket
import re
from django.core.serializers import serialize
   
def overview(request, site_name):     
    # add exception here in case of empty queryset
    gluesite = getGlueSite(site_name)
    if not gluesite:
        pass
        #raise Http404
        
                
    gluesite.usersupportcontact = str(gluesite.usersupportcontact).split(":")[-1]
    site_entity = getEntityByUniqueidType(site_name, 'Site')
    topbdii_list  = getNodesInSite(site_entity, 'bdii_top')
    sitebdii_list = getNodesInSite(site_entity, 'bdii_site')
    ce_list       = getNodesInSite(site_entity, 'CE')
    se_list       = getNodesInSite(site_entity, 'SE')
    service_list  = getServicesInSite(site_entity)
    count_dict             = {}
    count_dict['topbdii']  = len(topbdii_list)
    count_dict['sitebdii'] = len(sitebdii_list)
    count_dict['ce']       = len(ce_list)
    count_dict['se']       = len(se_list)
    count_dict['service']  = len(service_list)
    nagios_status = getNagiosStatusDict()
    overall_status_dict             = {}
    hostnames = [topbdii.hostname for topbdii in topbdii_list]
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-bdii.+')
    overall_status_dict['topbdii']  = Cell_Status(getNagiosStatusStr(status, has_been_checked))
    hostnames = [sitebdii.hostname for sitebdii in sitebdii_list]
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-bdii.+')
    overall_status_dict['sitebdii'] = Cell_Status(getNagiosStatusStr(status, has_been_checked))
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-ce$')
    overall_status_dict['ce']       = Cell_Status(getNagiosStatusStr(status, has_been_checked))
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-se$')
    overall_status_dict['se']       = Cell_Status(getNagiosStatusStr(status, has_been_checked))
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-service$')
    overall_status_dict['service']  = Cell_Status(getNagiosStatusStr(status, has_been_checked))
    (status, has_been_checked)      = getNodesOverallStatus(nagios_status, hostnames, '^check-site$')
    overall_status_dict['site']     = Cell_Status(getNagiosStatusStr(status, has_been_checked))

    # To compose the content of table 
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = generateTableContentForSiteList(site_entity)


    return render_to_response('overview.html', {'site': gluesite,
                                                'topbdii_list': topbdii_list,
                                                'sitebdii_list': sitebdii_list,
                                                'ce_list': ce_list,
                                                'se_list': se_list,
                                                'service_list': service_list,
                                                'count_dict': count_dict,
                                                'overall_status_dict': overall_status_dict,
                                                'thead': thead,
                                                'tbody': tbody})
    
def topbdii(request, site_name):
    status_thead = ['Top BDII', 'Check', 'Current State', 'Status Information', 'More Information']
    status_list = getStatusList(site_name, '^check-bdii.+', 'bdii_top')
    
#    status_list = []
#    glue_list = []
#    site_entity = getEntityByUniqueidType(site_name, 'Site')
#    if not site_entity:
#        pass
#        #raise Http404               
#    node_list = getNodesInSite(site_entity, 'bdii_top')
#    status_list = getStatusList([node.hostname for node in node_list], '^check-bdii.+')
#
#    for unique_id in [node.uniqueid for node in node_list]:
#        glue_dict = {}
#        glue_dict['class'] = 'GlueService'
#        glue_dict['uniqueid'] = unique_id
#        glue_dict['attributes'] = []
#        glue_service_values = glueservice.objects.filter(endpoint = unique_id, type = 'bdii_top').values()
#        for value_dict in glue_service_values:
#            for key in value_dict.keys():
#                glue_dict['attributes'].append({'attribute': key, 'value': value_dict[key]})                
#        if glue_dict:
#            glue_list.append(glue_dict)

    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_thead': status_thead,
                                              'status_list' : status_list})

#def topbdii_xml(request, site_name):
#    site_entity = getEntityByUniqueidType(site_name, 'Site')
#    node_list = getNodesInSite(site_entity, 'bdii_top')
#    glue = glueservice.objects.filter(endpoint__in=[node.uniqueid for node in node_list], type = 'bdii_top')
#    xml = serialize('xml', glue)
#    #f = open('/home/bubu/workspace/GStat2.0-gstat/apps/gridsite/xml-tree-data.xml','r')
#    #xml=f.read()
#    return HttpResponse(xml,mimetype='application/xml') 

#def topbdii_json(request, site_name):
#    site_entity = getEntityByUniqueidType(site_name, 'Site')
#    node_list = getNodesInSite(site_entity, 'bdii_top')
#    glue = glueservice.objects.filter(endpoint__in=[node.uniqueid for node in node_list], type = 'bdii_top')
#    json = serialize('json', glue)
#    return HttpResponse(json,mimetype='text/javascript;')

def sitebdii(request, site_name):
    status_thead = ['Site BDII', 'Check', 'Current State', 'Status Information', 'More Information']
    status_list = getStatusList(site_name, '^check-bdii.+', 'bdii_site')            
    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_thead': status_thead,
                                              'status_list' : status_list})
    
def ce(request, site_name):
    status_thead = ['Site BDII', 'Check', 'Current State', 'Status Information', 'More Information']
    status_list = getStatusList(site_name, '^check-ce$', 'bdii_site')
            
    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_thead': status_thead,
                                              'status_list' : status_list})    
    
def se(request, site_name):
    status_thead = ['Site BDII', 'Check', 'Current State', 'Status Information', 'More Information']
    status_list = getStatusList(site_name, '^check-se$', 'bdii_site')
            
    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_thead': status_thead,
                                              'status_list' : status_list})       
    
def service(request, site_name):
    status_thead = ['Site BDII', 'Check', 'Current State', 'Status Information', 'More Information']
    status_list = getStatusList(site_name, '^check-service$', 'bdii_site')
            
    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_thead': status_thead,
                                              'status_list' : status_list})    
    
def site(request, site_name):
    status_thead = ['Site BDII', 'Check', 'Current State', 'Status Information', 'More Information']
    status_list = getStatusList(site_name, '^check-site$', 'bdii_site')
            
    return render_to_response('status.html', {'site_name'   : site_name,
                                              'status_thead': status_thead,
                                              'status_list' : status_list}) 
    
"""
def getStatusList(hostname_list, check_name_phrase):
    nagios_status = getNagiosStatusDict()
    status_list = []
    for hostname in hostname_list:
        for check in nagios_status[hostname].keys():
            status_dict = {}
            if re.compile(check_name_phrase).match(check):
                status_dict['hostname'] = hostname
                status_dict['check'] = check
                status_dict['current_state']      = NAGIOS_STATUS_MAPPING[nagios_status[hostname][check]['current_state']]
                status_dict['plugin_output']      = nagios_status[hostname][check]['plugin_output']
                status_dict['long_plugin_output'] = nagios_status[hostname][check]['long_plugin_output'].split('\n')
                status_dict['last_check']         = nagios_status[hostname][check]['last_check']
            if status_dict:
                status_list.append(status_dict)
    return status_list    
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





""" THE FOLLOWING CODES ARE DUPLICATED FROM SUMMARY VIEW  """
def generateTableContentForSiteList(site):
    tbody = []
    # To count the CPU and Jobs numbers for all CEs at all sites in certain Grid
    # To count the storage space on all SEs at all sites in certain Grid
    (logicalcpus, physicalcpus)           = countCPUsInSite(site)
    (totalsize, usedsize)                 = countStoragesInSite(site)
    (runningjobs, waitingjobs, totaljobs) = countJobsInSite(site)

    # need to add a KeyError exception here
    # "Grid Name", "Sites", "Logical/Physical CPUs", "Total/Used/Free Storage Space", "Running/Waiting/Total Jobs"
    site_name     = Cell_Link(site.uniqueid, "/gstat/site/%s" % site.uniqueid)
    logical_cpus  = Cell_Link(logicalcpus, "")
    physical_cpus = Cell_Link(physicalcpus, "")
    storage_space = Cell_PercentBar(totalsize, 
                                    usedsize, 
                                    total_desc="Total Space (GB)", 
                                    used_desc="Used Space (GB)", 
                                    free_desc="Free Space (GB)")
    jobs          = Cell_PercentBar(totaljobs, 
                                    waitingjobs, 
                                    total_desc="Total Jobs", 
                                    used_desc="Waiting Jobs", 
                                    free_desc="Running Jobs")

    row = [site_name, logical_cpus, physical_cpus, storage_space, jobs]
    tbody.append(row)
        
    return tbody

class Cell_Status:
    def __init__(self, status):
        self.type = "Status"
        self.status = status

class Cell_Link:
    def __init__(self, anchor_desc, url_addr):
        self.type = "Link"
        self.anchor_desc = anchor_desc
        self.url_addr = url_addr

class Cell_PercentBar:
    def __init__(self, total, used, total_desc="Total", used_desc="Used", free_desc="Free"):
        self.type = "PercentBar"
        self.total = total
        self.used = used
        self.free = total - used
        if total != 0:
            self.percentage = used * 100 / total
        else:
            self.percentage = 0
        self.total_desc = total_desc
        self.used_desc = used_desc
        self.free_desc = free_desc