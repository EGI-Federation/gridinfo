import re
import socket

from django.db import models
from topology.models import Entity
from topology.models import Entityrelationship
from glue.models import *

# ---------------------------------------
# -- Glue data model related functions --
# ---------------------------------------

def get_unique_gluesite(site_name):
    """ get glue site entities from glue database """
    site = gluesite.objects.filter(uniqueid=site_name)
    if site:
        return site[0]
    else:
        return None

def get_gluesubclusters(service_list):
    """ get glue subcluster entities from glue database """
    uniqueids = [service.uniqueid for service in service_list]
    clusters = Entity.objects.filter(type = 'CE', uniqueid__in = uniqueids)
    uniqueids = [cluster.uniqueid for cluster in clusters]
    sub_clusters = gluesubcluster.objects.filter(gluecluster_fk__in = uniqueids)
    return sub_clusters


def get_glueses(service_list):
    """ get glue se entities from glue database """
    uniqueids = [service.uniqueid for service in service_list]
    ses = Entity.objects.filter(type = 'SE', uniqueid__in = uniqueids)
    uniqueids = [se.uniqueid for se in ses]
    se_list = gluese.objects.filter(uniqueid__in = uniqueids)
    return se_list

def get_gluevoview(service_list):
    """ get glue voview entities from glue database """
    uniqueids = [service.uniqueid for service in service_list]
    clusters = Entity.objects.filter(type = 'CE', uniqueid__in = uniqueids)
    uniqueids = [cluster.uniqueid for cluster in clusters]
    CEs = gluece.objects.filter(gluecluster_fk__in = uniqueids)
    uniqueids = [ce.uniqueid for ce in CEs]
    VO_views = gluevoview.objects.filter(gluece_fk__in = uniqueids)

    return VO_views

# -------------------------------------------
# -- Topology data model related functions --
# -------------------------------------------

def get_unique_entity(unique_id, type_name):
    """ get unique entity from topology database """
    qs_entity = Entity.objects.filter(uniqueid=unique_id, type=type_name)
    # CAUTION!, alert exception or warning if there is more than one record
    if qs_entity:
        return qs_entity[0]
    else:
        return None

def get_groups(type):
    """ get entities by type from topology database """
    groups = Entity.objects.filter(type=type)
    
    return groups

def get_sites(type, value="ALL"):
    """ get site entities from topology database """
    predicate = {'GRID'     : 'SiteGrid', 
                 'EGEE_ROC' : 'SiteEgeeRoc', 
                 'WLCG_TIER': 'SiteWlcgTier',
                 'Country'  : 'SiteCountry'}
    
    site_list = [] 
    if ( value == "ALL"):
        groups = Entity.objects.filter(type=type)
    else:
        groups = Entity.objects.filter(uniqueid = value, type = type)
    for group in groups:
        relationships = Entityrelationship.objects.select_related('subject').filter(predicate = predicate[type], object = group)
        for relationship in relationships:
            site_list.append(relationship.subject)
    
    return site_list


def get_countries(site_list):
    """ get country entities from topology database """
    relationships = Entityrelationship.objects.select_related('object').filter(predicate = 'SiteCountry', subject__in = site_list)
    countries = []
    for relation in relationships:
        try:
            countries.index(relation.object.uniqueid)
        except:    
            countries.append(relation.object.uniqueid)
    return countries

def get_services(site_list):
    """ get service entities from topology database """
    relationships = Entityrelationship.objects.select_related('object').filter(predicate = 'SiteService', subject__in = site_list)
    services = []
    for relation in relationships:
        services.append(relation.object)
    return services

def get_vos(service_list):
    """ get vo entities from topology database """
    relationships = Entityrelationship.objects.select_related('object').filter(predicate = 'ServiceVO', subject__in = service_list)
    vos = []
    for relation in relationships:
        try:
            vos.index(relation.object)
        except:    
            vos.append(relation.object)
    return vos


# ---------------------------------------------------------
# -- Installed Capacity and Statistics related functions --
# ---------------------------------------------------------

def get_installed_capacity_cpu(sub_clusters_list):
    """ calculate cpu numbers in glue subcluster entities """
    physical_cpus = 0
    logical_cpus = 0
    for sub_cluster in sub_clusters_list:
        logical_cpus += convert_to_integer(sub_cluster.logicalcpus)
        physical_cpus += convert_to_integer(sub_cluster.physicalcpus)

    return [physical_cpus, logical_cpus]

def get_installed_capacity_storage(se_list):
    """ calculate storage space in glue se entities """
    total_online = 0
    used_online = 0
    total_nearline = 0
    used_nearline = 0 

    for se in se_list:
        total_online += convert_to_integer(se.totalonlinesize)
        used_online += convert_to_integer(se.usedonlinesize)
        total_nearline += convert_to_integer(se.totalnearlinesize) 
        used_nearline += convert_to_integer(se.usednearlinesize) 

    return [ total_online, used_online, total_nearline, used_nearline ]

def get_installed_capacity_per_os(sub_clusters_list):
    """ calculate cpu numbers in glue subcluster entities by os version """
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

        os[os_name][os_release][0] += convert_to_integer(sub_cluster.physicalcpus)    
        os[os_name][os_release][1] += convert_to_integer(sub_cluster.logicalcpus)

    data = []
    keys = os.keys()
    keys.sort()
    for  name in keys:
        for release in os[name]:
            data.append([name, release, os[name][release][0], os[name][release][1]])

    return data

def get_job_stats(vo_view_list):
    """ calculate job numbers in glue voview entities """
    total_jobs = 0
    running_jobs = 0
    waiting_jobs = 0
    for voview in vo_view_list:
        total_jobs += convert_to_integer(voview.totaljobs)
        running_jobs += convert_to_integer(voview.runningjobs)
        if ( not convert_to_integer(voview.waitingjobs) == 444444):
            waiting_jobs += convert_to_integer(voview.waitingjobs)
    return  [ total_jobs, running_jobs, waiting_jobs ]

def get_service_versions(service_list):
    """ get service version information from glue service entities """
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

# ------------------------------
# -- Nagios related functions --
# ------------------------------

def get_nagios_status_dict():
    """ This takes the nagios realtime status data and outputs as a dictionary object. """
    def __getDefinitions(filename, obj):
        """ Parse the status.dat file and extract matching object definitions """
        try:
            file = open(filename)
        except(IOError):
            print "Nagios realtime status file doesn't exist: %s" % filename
            sys.exit()
            
        content = file.read().replace("\t"," ")
        file.close
        pat = re.compile(obj +' \{([\S\s]*?)\}',re.DOTALL)
        finds = pat.findall(content)
        return finds
    
    def __getDirective(item, directive):
        """ parse an object definition, return the directives """
        #pat = re.compile(' '+directive+'[\s= ]*([\S, ]*)\n')
        pat = re.compile(' '+directive+'[=]*([\S, ]*)\n')
        m = pat.search(item)
        if m:
            return m.group(1).strip()    
    # config local access control permission to enable the file to be readbale by this script
    # Please note that it's HARD CODE for now!!!
    status_file="/var/nagios/status.dat"

    # store nagios status data in a dictionary object. 
    status_dict = {}

    # fixme - the following token change dependiong on the version of Nagios 
    hosttoken='hoststatus'
    servicetoken='servicestatus'
    programtoken='programstatus'
    
    # parse the nagios realtime status data and generate a dictionary
    
    # each host
    hosts = __getDefinitions(status_file, hosttoken)
    services = __getDefinitions(status_file, servicetoken)
    for hostdef in hosts:
        host_name          = __getDirective(hostdef, "host_name")
        current_state      = __getDirective(hostdef, "current_state")
        plugin_output      = __getDirective(hostdef, "plugin_output")
        last_check         = __getDirective(hostdef, "last_check")
        has_been_checked   = __getDirective(hostdef, "has_been_checked")
        
        status_dict[host_name]                     = {}
        status_dict[host_name]['current_state']    = convert_to_integer(current_state)
        status_dict[host_name]['plugin_output']    = plugin_output
        status_dict[host_name]['last_check']       = last_check
        status_dict[host_name]['has_been_checked'] = convert_to_integer(has_been_checked)

        for servicedef in services:
            if (__getDirective(servicedef, "host_name") == host_name):
                service_description = __getDirective(servicedef, "service_description")
                current_state       = __getDirective(servicedef, "current_state")
                plugin_output       = __getDirective(servicedef, "plugin_output")
                long_plugin_output  = __getDirective(servicedef, "long_plugin_output")
                last_check          = __getDirective(servicedef, "last_check")
                has_been_checked    = __getDirective(servicedef, "has_been_checked")
                
                status_dict[host_name][service_description]                       = {}
                status_dict[host_name][service_description]['current_state']      = convert_to_integer(current_state)
                status_dict[host_name][service_description]['plugin_output']      = plugin_output
                status_dict[host_name][service_description]['long_plugin_output'] = long_plugin_output
                status_dict[host_name][service_description]['last_check']         = last_check
                status_dict[host_name][service_description]['has_been_checked']   = convert_to_integer(has_been_checked)
    
    return status_dict


def get_hosts_overall_nagios_status(status_dict, hostname_list, check_name_phrase):
    overall_status = -1
    has_been_checked = 1
    real_hostname_list = []
    for hostname in hostname_list:
        alias = get_hostname(hostname)
        real_hostname_list += get_hosts_from_alias(alias)
    for hostname in real_hostname_list:
        try:
            for key in status_dict[hostname].keys(): 
                if re.compile(check_name_phrase).match(key):
                    if status_dict[hostname][key]['current_state'] > overall_status:
                        overall_status = status_dict[hostname][key]['current_state']
                    if status_dict[hostname][key]['has_been_checked'] == 0:
                        has_been_checked = 0
        except (KeyError):
            # No matching records found
            pass
    
    return (overall_status, has_been_checked)

def get_nagios_status_str(current_state, has_been_checked):
    if (current_state == 0):
        if (has_been_checked == 0): return 'PENDING'
        else:                       return 'OK'
    elif (current_state == 1):      return 'WARNING'
    elif (current_state == 2):      return 'CRITICAL'
    elif (current_state == 3):      return 'UNKNOWN'
    else:                           return 'N/A'

def get_nagios_status(nagios_status, check, hostname):

    status_dict = {'hostname': hostname,
                   'current_state': 'N/A'}
    if ( nagios_status.has_key(hostname) ) :
        if ( nagios_status[hostname].has_key(check) ) :
            status_dict['check']              = check
            current_state                     = nagios_status[hostname][check]['current_state']
            has_been_checked                  = nagios_status[hostname][check]['has_been_checked']
            status_dict['current_state']      = get_nagios_status_str(current_state, has_been_checked)
            status_dict['plugin_output']      = nagios_status[hostname][check]['plugin_output']
            status_dict['long_plugin_output'] = nagios_status[hostname][check]['long_plugin_output']
            status_dict['last_check']         = nagios_status[hostname][check]['last_check']

    return status_dict

# -----------------------------
# -- Miscellaneous functions --
# -----------------------------

def get_hostname(uniqueid):
    hostname=uniqueid
    index=hostname.rfind(':')
    if (index > -1 ):
        hostname = hostname[:index]
    index=hostname.find(':')
    if (index > -1 ):
        hostname = hostname[index+3:]


    return hostname

def get_hosts_from_alias(hostname):
    hosts = []
    try:
        ips = socket.gethostbyname_ex(hostname)[2]
        for ip in ips:
            instance = socket.gethostbyaddr(ip)[0]
            hosts.append(instance)
    except Exception, e:
        pass
    return hosts

def convert_to_integer(number):
    try:
        return int(number)
    except (ValueError), error:
        return 0

def sort_objects_by_attr(object_list, attribute):
    unsorted_list = object_list
    sorted_list = [(obj.__getattribute__(attribute), obj) for obj in unsorted_list]
    sorted_list.sort()
    result_list = [obj for (attribute, obj) in sorted_list]
    
    return result_list