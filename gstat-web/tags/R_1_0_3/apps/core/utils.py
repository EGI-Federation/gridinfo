import re
import socket
import time
import sys
import logging

from django.db import models
from django.conf import settings
from topology.models import Entity
from topology.models import Entityrelationship
from glue.models import *

# Set logging
log = logging.getLogger(sys.argv[0])
hdlr = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('[%(levelname)s]: %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(2)

# ---------------------------------------
# -- Glue data model related functions --
# ---------------------------------------

def get_glue_entities(model_name, uniqueids_list=[]):
    try:
        model = models.get_model('glue', model_name)
        if not uniqueids_list:
            objects = model.objects.all()
        else:
            objects = model.objects.filter(uniqueid__in=uniqueids_list)
        return objects
    except:
        # need to re-factor
        return None

def get_unique_gluesite(site_name):
    """ get glue site entities from glue database """
    site = gluesite.objects.filter(uniqueid=site_name)
    if site:
        return site[0]
    else:
        return None

def get_gluesubclusters(service_list):
    """ get glue subcluster entities from glue database """
    # get cluster uniqueid 
    uniqueids = []
    for service in service_list:
        if service.type == 'CE': uniqueids.append(service.uniqueid)

    sub_clusters = gluesubcluster.objects.filter(gluecluster_fk__in = uniqueids)
    return sub_clusters


def get_glueses(service_list):
    """ get glue se entities from glue database """
    #get se uniqueid
    uniqueids = []
    for service in service_list:
        if service.type == 'SE': uniqueids.append(service.uniqueid)

    se_list = gluese.objects.filter(uniqueid__in = uniqueids)
    return se_list

def get_gluevoviews(service_list, vo_name=None):
    """ get glue voview entities from glue database """
    # get cluster uniqueid 
    uniqueids = []
    for service in service_list:
        if service.type == 'CE': uniqueids.append(service.uniqueid)

    ces = gluece.objects.filter(gluecluster_fk__in = uniqueids)
    uniqueids = [ce.uniqueid for ce in ces]
    voviews = gluevoview.objects.filter(gluece_fk__in = uniqueids)
    if vo_name:
        voview_list = []
        vo_to_voview_mapping = get_vo_to_voview_mapping(voviews)
        for voview in voviews:
            try:
                voname = vo_to_voview_mapping[voview.glueceuniqueid][voview.localid]
            except KeyError, e:
                continue
            if voname == vo_name:
                voview_list.append(voview)
        voviews = voview_list

    return voviews

def get_gluesas(service_list, vo_name=None):
    """ get glue voview entities from glue database """
    #get se uniqueid
    uniqueids = []
    for service in service_list:
        if service.type == 'SE': uniqueids.append(service.uniqueid)

    sas = gluesa.objects.filter(gluese_fk__in = uniqueids)
    if vo_name:
        sa_list = []
        vo_to_sa_mapping = get_vo_to_sa_mapping(sas)
        for sa in sas:
            try:
                voname = vo_to_sa_mapping[sa.gluese_fk][sa.localid]
            except KeyError, e:
                    continue
            if voname == vo_name:
                sa_list.append(sa)
        sas = sa_list
        
    return sas

def get_vo_to_voview_mapping(voview_list=None):
    # Create VO to VOView Mapping
    vo_to_voview_mapping = {}
    if voview_list:
        gluece_uniqueids = [voview.gluece_fk for voview in voview_list]
        objects = gluemultivalued.objects.filter(attribute='GlueCEAccessControlBaseRule', uniqueid__in=gluece_uniqueids)
    else:
        objects = gluemultivalued.objects.filter(attribute='GlueCEAccessControlBaseRule')
    for object in objects:
        if ( object.localid == "" ):
            continue
        if ( object.value[:3] == "VO:" ):
            vo = object.value[3:]
        elif ( object.value[:5] == "VOMS:" ):
            vo = object.value[5:]
            vo = vo.split('/')[1]
        else:
            continue
        if vo.strip() == '': continue
            
        if ( not vo_to_voview_mapping.has_key(object.uniqueid) ):
            vo_to_voview_mapping[object.uniqueid] = {}
        # vo_to_voview_mapping[gluece_uniqueid][gluevoview_localid] = vo_name
        vo_to_voview_mapping[object.uniqueid][object.localid] = vo
    
    return vo_to_voview_mapping

def get_vo_to_sa_mapping(sa_list=None):
    # Create VO to SA Mapping
    vo_to_sa_mapping = {}
    
    if sa_list:
        gluese_uniqueids = [sa.gluese_fk for sa in sa_list]
        objects = gluemultivalued.objects.filter(attribute='GlueSAAccessControlBaseRule', uniqueid__in=gluese_uniqueids)
    else:
        objects = gluemultivalued.objects.filter(attribute='GlueSAAccessControlBaseRule') 
    
    for object in objects:
        # extract the vo name
        if ( object.value[:3] == "VO:" ):
            if len(object.value.split('/')) > 1:
                continue
            vo = object.value[3:]
        elif ( object.value[:5] == "VOMS:" ):
            vo = object.value[5:]
            vo = vo.split('/')[1]
        else:
            if len(object.value.split('/')) > 1:
                continue
            vo = object.value
        
        if vo.strip() == '': continue
        
        if ( not vo_to_sa_mapping.has_key(object.uniqueid) ):
            vo_to_sa_mapping[object.uniqueid] = {}
        # vo_to_sa_mapping[gluese_uniqueid][gluesa_localid] = vo_name
        vo_to_sa_mapping[object.uniqueid][object.localid] = vo

    return vo_to_sa_mapping

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

def get_sites(type, value="ALL", groups=None):
    """ get site entities from topology database """
    predicate = {'GRID'     : 'SiteGrid', 
                 'EGEE_ROC' : 'SiteEgeeRoc', 
                 'WLCG_TIER': 'SiteWlcgTier',
                 'Country'  : 'SiteCountry',
                 'VO'       : 'ServiceVO'}
    
    site_list = [] 
    if not groups:
        if ( value == "ALL"):
            groups = Entity.objects.filter(type=type)
        else:
            groups = Entity.objects.filter(type=type, uniqueid=value)
        
    for group in groups:
        relationships = Entityrelationship.objects.select_related('subject').filter(predicate=predicate[type], object=group)
        if type == "VO":
            relationships = Entityrelationship.objects.select_related('subject').filter(predicate='SiteService', object__in=[rlp.subject for rlp in relationships])
        site_list += [rlp.subject for rlp in relationships]
    
    site_list = {}.fromkeys(site_list).keys() 

    return site_list


def get_countries(site_list):
    """ get country entities from topology database """
    relationships = Entityrelationship.objects.select_related('object').filter(predicate='SiteCountry', subject__in=site_list)
    countries = []
    for relation in relationships:
        try:
            countries.index(relation.object.uniqueid)
        except:    
            countries.append(relation.object.uniqueid)
    return countries

def get_services(site_list, service_type=None):
    """ get service entities from topology database """
    if service_type:
        relationships = Entityrelationship.objects.select_related('object').filter(predicate = 'SiteService', subject__in = site_list, object__type=service_type)
    else:
        relationships = Entityrelationship.objects.select_related('object').filter(predicate = 'SiteService', subject__in = site_list)
    services = []
    for relation in relationships:
        services.append(relation.object)
    return services

def get_vo_services(vo_name, service_type):
    
    # vo_to_site_mapping[vo][service] = [site]
    site_service_rlp = Entityrelationship.objects.select_related('subject', 'object').filter(predicate = 'SiteService', object__type=service_type)
    service_vo_rlp = Entityrelationship.objects.select_related('subject', 'object').filter(predicate = 'ServiceVO', subject__type=service_type, object__uniqueid=vo_name)

    service_to_site_mapping = {}
    # {"service entity": "site entity"}
    for site_service in site_service_rlp:
        site = site_service.subject
        service = site_service.object
        if service not in service_to_site_mapping:
            service_to_site_mapping[service] = site

    site_service = {}
    # {"site entity": ["service_entity_list"]}
    for service_vo in service_vo_rlp:
        service = service_vo.subject
            
        try:
            site = service_to_site_mapping[service]
        except KeyError, e:
            continue
            
        if site not in site_service:
            site_service[site] = []
        site_service[site].append(service)


    """
    service_to_site_mapping = {}
    # {"service_type": {"service_uniqueid": "site_name"}}
    for site_service in site_service_rlp:
        site_name = site_service.subject.uniqueid
        service_uniqueid = site_service.object.uniqueid
        service_type = site_service.object.type
        if service_type not in service_to_site_mapping:
            service_to_site_mapping[service_type] = {}
        service_to_site_mapping[service_type][service_uniqueid] = site_name
    
    vo_site_service = {}
    # {"vo_name": {"site_name": {"service_type": ["service_uniqueid_list"]}}}
    for service_vo in service_vo_rlp:
        service_uniqueid = service_vo.subject.uniqueid
        service_type = service_vo.subject.type
        vo = service_vo.object.uniqueid
        if ( not vo_site_service.has_key(vo) ):
            vo_site_service[vo] = {}
        try:
            site_name = service_to_site_mapping[service_type][service_uniqueid]
        except KeyError, e:
            continue
            
        if site_name not in vo_site_service[vo]:
            vo_site_service[vo][site_name] = {}
        if service_type not in vo_site_service[vo][site_name]:
            vo_site_service[vo][site_name][service_type] = []
        vo_site_service[vo][site_name][service_type].append(service_uniqueid)
    """   
            
    
    return site_service
    
"""
def get_services_from_vo(vo_list, service_type=None):
    if service_type:
        relationships = Entityrelationship.objects.select_related('subject').filter(predicate = 'ServiceVO', object__in = vo_list, subject__type=service_type)
    else:
        relationships = Entityrelationship.objects.select_related('subject').filter(predicate = 'ServiceVO', object__in = vo_list)
    services = []
    for relation in relationships:
        services.append(relation.subject)
    return services
"""

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

def get_installed_capacity_cpu(sub_cluster_list):
    """ calculate cpu numbers in glue subcluster entities """
    attributes = ["physicalcpus", "logicalcpus"]
    stats = [0, 0]
    for sub_cluster in sub_cluster_list:
        for attr in attributes:
            value = sub_cluster.__getattribute__(attr)
            stats[attributes.index(attr)] += convert_to_integer(value)
    return  stats   

def get_installed_capacity_si2000(sub_cluster_list):
    """ calculate total installed computing capacity in glue subcluster entities """
    attributes = ["benchmarksi00", "logicalcpus"]
    si2000 = 0
    for sub_cluster in sub_cluster_list:
        product = convert_to_integer(sub_cluster.benchmarksi00) * convert_to_integer(sub_cluster.logicalcpus)
        si2000 += product
    return  si2000   

def get_installed_capacity_storage(se_list):
    """ calculate storage space in glue se entities """
    attributes = ["totalonlinesize", "usedonlinesize", "totalnearlinesize", "usednearlinesize"]
    stats = [0, 0, 0, 0]
    for se in se_list:
        for attr in attributes:
            value = se.__getattribute__(attr)
            stats[attributes.index(attr)] += convert_to_integer(value)
    return  stats        

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

def get_voview_job_stats(voview_list):
    """ calculate job numbers in glue voview entities """
    attributes = ["totaljobs", "runningjobs", "waitingjobs"]
    stats = [0, 0, 0]
    for voview in voview_list:
        for attr in attributes:
            value = voview.__getattribute__(attr)
            if (attr == "waitingjobs" and value == "444444"): value="0"
            stats[attributes.index(attr)] += convert_to_integer(value)
    return  stats    

def get_sa_storage_stats(sa_list):
    """ calculate storage space in glue sa entities """
    attributes = ["totalonlinesize", "usedonlinesize", "totalnearlinesize", "usednearlinesize"]
    stats = [0, 0, 0, 0]
    for sa in sa_list:
        for attr in attributes:
            value = sa.__getattribute__(attr)
            if (value != "999999"): 
                stats[attributes.index(attr)] += convert_to_integer(value)
    return  stats

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
    def __getDefinitions(content, token):
        """ Parse the status.dat file and extract matching object definitions """
        pattern = re.compile(token +' \{([\S\s]*?)\}',re.DOTALL)
        finds = pattern.findall(content)
        return finds
    
    def __getDirective(item, directive):
        """ parse an object definition, return the directives """
        #pat = re.compile(' '+directive+'[\s= ]*([\S, ]*)\n')
        pattern = re.compile(' '+directive+'[=]*([\S, ]*)\n')
        m = pattern.search(item)
        if m:
            return m.group(1).strip()    
        
    # store nagios status data in a dictionary object. 
    status_dict = {}
        
    # config local access control permission to enable the file to be readbale by this script
    # Please note that it's HARD CODE for now!!!
    status_file="/var/nagios/status.dat"
    if settings.NAGIOS_STATUS_FILE:
        status_file = settings.NAGIOS_STATUS_FILE
    try:
        file = open(status_file)
    except(IOError):
        log.error( "apps/core/utils.py: Nagios realtime status file doesn't exist: %s" % status_file )
        return status_dict
    content = file.read().replace("\t"," ")
    file.close
    
    # fixme - the following token change dependiong on the version of Nagios 
    hosttoken='hoststatus'
    servicetoken='servicestatus'
    
    # parse the nagios realtime status data and generate a dictionary
    hostdefs = __getDefinitions(content, hosttoken)
    for hostdef in hostdefs:
        host_name          = __getDirective(hostdef, "host_name")
        current_state      = __getDirective(hostdef, "current_state")
        plugin_output      = __getDirective(hostdef, "plugin_output")
        last_check         = __getDirective(hostdef, "last_check")
        has_been_checked   = __getDirective(hostdef, "has_been_checked")
        if host_name not in status_dict:
            status_dict[host_name] = {}
        status_dict[host_name]['current_state']    = convert_to_integer(current_state)
        status_dict[host_name]['plugin_output']    = plugin_output
        status_dict[host_name]['last_check']       = last_check
        status_dict[host_name]['has_been_checked'] = convert_to_integer(has_been_checked)

    servicedefs = __getDefinitions(content, servicetoken)
    for servicedef in servicedefs:
        host_name           = __getDirective(servicedef, "host_name")
        service_description = __getDirective(servicedef, "service_description")
        current_state       = __getDirective(servicedef, "current_state")
        plugin_output       = __getDirective(servicedef, "plugin_output")
        long_plugin_output  = __getDirective(servicedef, "long_plugin_output")
        last_check          = __getDirective(servicedef, "last_check")
        has_been_checked    = __getDirective(servicedef, "has_been_checked")
        if host_name in status_dict:
            if service_description not in status_dict[host_name]:
                status_dict[host_name][service_description] = {}
            status_dict[host_name][service_description]['current_state']      = convert_to_integer(current_state)
            status_dict[host_name][service_description]['plugin_output']      = plugin_output
            status_dict[host_name][service_description]['long_plugin_output'] = long_plugin_output
            status_dict[host_name][service_description]['last_check']         = last_check
            status_dict[host_name][service_description]['has_been_checked']   = convert_to_integer(has_been_checked)

    return status_dict

def get_overall_check_status(status_dict):
    overall_status = -1
    has_been_checked = 1
    for key in status_dict.keys(): 
        if key.startswith("check"):
            status = status_dict[key]['current_state']
            checked = status_dict[key]['has_been_checked']
            if status > overall_status:
                overall_status = status
            if checked == 0:
                has_been_checked = 0
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

def get_check_list(nagios_status, hostname):
    check_list = []
    if ( nagios_status.has_key(hostname) ) :
        for key in nagios_status[hostname].keys(): 
            if re.compile('^check-.+').match(key):
                check_list.append(key)
    check_list.sort()
    
    return check_list
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
    hosts.sort()
    
    return hosts

def get_hosts_from_aliases(hostnames):
    hosts = []
    for hostname in hostnames:
        hosts_from_alias = get_hosts_from_alias(hostname)
        if ( len(hosts_from_alias) > 1 ):
            #This is an alias point to more than one real hostname
            hosts += hosts_from_alias
        elif ( len(hosts_from_alias) == 1 ):
            if not ( hostname == hosts_from_alias[0]):
                #This is an alias for a single instance
                hosts += hosts_from_alias
            else:
                #The actual id given was a real host.
                hosts.append(hostname)
    hosts.sort()
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

def get_status_for_sites(site_list):
    nagios_status = get_nagios_status_dict()
    #relationships = Entityrelationship.objects.select_related('subject', 'object').filter(predicate = 'SiteService',  subject__in = site_list, object__type='bdii_top') | Entityrelationship.objects.select_related('subject', 'object').filter(predicate = 'SiteService',  subject__in = site_list, object__type='bdii_site')
    relationships = Entityrelationship.objects.select_related('subject', 'object').filter(predicate = 'SiteService',  subject__in = site_list, object__type__in=['bdii_top', 'bdii_site']) 
    site_bdii = {}
    for relation in relationships:
        site_id = relation.subject.uniqueid
        if not site_bdii.has_key(site_id):
            site_bdii[site_id] = []
        site_bdii[site_id].append(relation.object.hostname)
    data = {}
    for site in site_list:
        site_id = site.uniqueid
        site_status = 'N/A'
        if site_bdii.has_key(site_id):
            hostnames = site_bdii[site_id]
            overall_status = -1
            checked = 1
            #The performance of this command needs to be improved. 
            for hostname in hostnames:
                hosts_from_alias = get_hosts_from_alias(hostname)
                for host in hosts_from_alias:
                    if host in nagios_status.keys():
                        (status, has_been_checked) = get_overall_check_status(nagios_status[host])
                        if status > overall_status:
                            overall_status = status
                        if has_been_checked == 0:
                            checked = 0
            site_status = get_nagios_status_str(overall_status, checked)
        data[site_id] = site_status

    return data

def get_installed_capacities(site_list, vo_name=None):
# data structure
# 0 physical_cpu
# 1 logical_cpu 
# 2 total_online
# 3 used_online
# 4 total_nearline
# 5 used_nearline
# 6 total_jobs
# 7 running_jobs
# 8 waiting_jobs    

    # Create data structure
    site_data = {}
    for site in site_list:
        site_id = site.uniqueid
        site_data[site_id] = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

    # Get the list of clusters
    relationships = Entityrelationship.objects.select_related('object','subject').filter(predicate = 'SiteService', subject__in = site_list, object__type='CE')
    cluster_site_mapping = {}
    for relation in relationships:
        cluster_site_mapping[relation.object.uniqueid]=relation.subject.uniqueid
    #Get a list of subclusters
    sub_clusters_list = gluesubcluster.objects.filter(gluecluster_fk__in = cluster_site_mapping.keys())

    # Get CE installed capacities
    for sub_cluster in sub_clusters_list:
        try:
            site_id = cluster_site_mapping[sub_cluster.gluecluster_fk]
            site_data[site_id][0] += convert_to_integer(sub_cluster.physicalcpus)
            site_data[site_id][1] += convert_to_integer(sub_cluster.logicalcpus)
            site_data[site_id][2] += convert_to_integer(sub_cluster.logicalcpus) * convert_to_integer(sub_cluster.benchmarksi00)
        except KeyError, e:
            continue

    #Get ce/cluster mapping
    ces = gluece.objects.filter(gluecluster_fk__in = cluster_site_mapping.keys())
    ce_cluster_mapping = {}
    for ce in ces:
        ce_cluster_mapping[ce.uniqueid]=ce.gluecluster_fk

    #Get VO Views
    if (not vo_name == None):
        objects = gluemultivalued.objects.filter(value__startswith='VO:%s' % vo_name, attribute='GlueCEAccessControlBaseRule',uniqueid__in=ce_cluster_mapping.keys()).exclude(localid__exact="") | gluemultivalued.objects.filter(value__startswith='VOMS:/%s' % vo_name, attribute='GlueCEAccessControlBaseRule',uniqueid__in=ce_cluster_mapping.keys()).exclude(localid__exact="")
        ce_vo_view = {}
        for object in objects:
            if not ce_vo_view.has_key(object.uniqueid):
                ce_vo_view[object.uniqueid] = {}
            ce_vo_view[object.uniqueid][object.localid] = None
    vo_view_list = gluevoview.objects.filter(gluece_fk__in = ce_cluster_mapping.keys())

    # Create a mapping between Sites and CEs
    for vo_view in vo_view_list:
        if (not vo_name == None ):
            if (not ce_vo_view.has_key(vo_view.glueceuniqueid)):
                continue
            if (not ce_vo_view[vo_view.glueceuniqueid].has_key(vo_view.localid)):
                continue
        try:
            site_id = cluster_site_mapping[ce_cluster_mapping[vo_view.glueceuniqueid]]
            site_data[site_id][7] += convert_to_integer(vo_view.totaljobs)
            site_data[site_id][8] += convert_to_integer(vo_view.waitingjobs)
            site_data[site_id][9] += convert_to_integer(vo_view.runningjobs)
        except KeyError:
            continue

   # Get the list of ses                                                  
    relationships = Entityrelationship.objects.select_related('object','subject').filter(predicate = 'SiteService', subject__in = site_list, object__type='SE')
    se_site_mapping = {}
    for relation in relationships:
        se_site_mapping[relation.object.uniqueid]=relation.subject.uniqueid

    #Get a list of ses                                                  
    se_list = gluese.objects.filter(uniqueid__in = se_site_mapping.keys())

    if ( vo_name == None ): 
        # Get SE Installed Capacities
        for se in se_list:
            try:
                site_id = se_site_mapping[se.uniqueid]
                site_data[site_id][3] += convert_to_integer(se.totalonlinesize)
                site_data[site_id][4] += convert_to_integer(se.usedonlinesize)
                site_data[site_id][5] += convert_to_integer(se.totalnearlinesize)
                site_data[site_id][6] += convert_to_integer(se.usednearlinesize)
            except KeyError, e:
                continue
    else:
        objects = gluemultivalued.objects.filter(value__startswith='VO:%s' % vo_name, attribute='GlueSAAccessControlBaseRule',uniqueid__in=se_list).exclude(localid__exact="") | gluemultivalued.objects.filter(value__startswith='VOMS:/%s' % vo_name, attribute='GlueSAAccessControlBaseRule',uniqueid__in=se_list).exclude(localid__exact="")
        se_sa = {}
        for object in objects:
            if not se_sa.has_key(object.uniqueid):
                se_sa[object.uniqueid] = {}
            se_sa[object.uniqueid][object.localid] = None

        sa_list = gluesa.objects.filter(gluese_fk__in = se_list)

        for sa in sa_list:
            if ( not se_sa.has_key(sa.gluese_fk)):
                continue
            if (not se_sa[sa.gluese_fk].has_key(sa.localid)):
                continue
            try:
                site_id = se_site_mapping[sa.gluese_fk]
                site_data[site_id][3] += convert_to_integer(sa.totalonlinesize)
                site_data[site_id][4] += convert_to_integer(sa.usedonlinesize)
                site_data[site_id][5] += convert_to_integer(sa.totalnearlinesize)
                site_data[site_id][6] += convert_to_integer(sa.usednearlinesize)
            except KeyError, e:
                pass

    return site_data

