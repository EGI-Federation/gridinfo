import re
import socket

from django.db import models
from topology.models import Entity
from topology.models import Entityrelationship
from glue.models import *

"""
CPU_COUNTS_SUBCLUSTER = None
JOB_COUNTS_CE         = None
SPACE_COUNTS_SE       = None
"""

# ---------------------------------------
# -- Glue data model related functions --
# ---------------------------------------
    
def getGlueEntity(model_name, uniqueids_list=[], all=False):
    try:
        model = models.get_model('glue', model_name)
        if all:
            objects = model.objects.all()
        else:
            objects = model.objects.filter(uniqueid__in=uniqueids_list)
        return objects
    except:
        # need to re-factor
        return None



def get_subclusters(service_list):
    """ get glue subcluster entities from glue database """
    uniqueids = [service.uniqueid for service in service_list]
    clusters = Entity.objects.filter(type = 'CE', uniqueid__in = uniqueids)
    uniqueids = [cluster.uniqueid for cluster in clusters]
    sub_clusters = gluesubcluster.objects.filter(gluecluster_fk__in = uniqueids)
    return sub_clusters


def get_ses(service_list):
    """ get glue se entities from glue database """
    uniqueids = [service.uniqueid for service in service_list]
    ses = Entity.objects.filter(type = 'SE', uniqueid__in = uniqueids)
    uniqueids = [se.uniqueid for se in ses]
    se_list = gluese.objects.filter(uniqueid__in = uniqueids)
    return se_list

def get_vo_view(service_list):
    """ get glue voview entities from glue database """
    uniqueids = [service.uniqueid for service in service_list]
    clusters = Entity.objects.filter(type = 'CE', uniqueid__in = uniqueids)
    uniqueids = [cluster.uniqueid for cluster in clusters]
    CEs = gluece.objects.filter(gluecluster_fk__in = uniqueids)
    uniqueids = [ce.uniqueid for ce in CEs]
    VO_views = gluevoview.objects.filter(gluece_fk__in = uniqueids)

    return VO_views

"""
def getSubClusterByCluster(cluster_uniqueids_list=[]):
    try:
        objects = gluesubcluster.objects.filter(gluecluster_fk__in=cluster_uniqueids_list)
        return objects
    except:
        # need to re-factor
        return None


def getCPUNumbersFromGlueSubCluster():
    # To get a list of gluesubcluster and then count the cpu numbers
    cpu_counts_subcluster = {}
    qs_subcluster = gluesubcluster.objects.filter()
    for subcluster in qs_subcluster:
        if subcluster.uniqueid not in cpu_counts_subcluster:
            cpu_counts_subcluster[subcluster.uniqueid] = {
                'logicalcpus' : convertToInteger(subcluster.logicalcpus),
                'physicalcpus': convertToInteger(subcluster.physicalcpus)}
        else:
            cpu_counts_subcluster[subcluster.uniqueid]['logicalcpus']  += convertToInteger(subcluster.logicalcpus)
            cpu_counts_subcluster[subcluster.uniqueid]['physicalcpus'] += convertToInteger(subcluster.physicalcpus)
    
    return cpu_counts_subcluster

def getStorageSpacesFromGlueSE():
    # To get a list of gluese and then count the storage spaces
    space_counts_se = {}
    qs_se = gluese.objects.filter()
    for se in qs_se:
        if se.uniqueid not in space_counts_se:
            space_counts_se[se.uniqueid] = {
                'totalonlinesize'   : convertToInteger(se.totalonlinesize),
                'usedonlinesize'    : convertToInteger(se.usedonlinesize),
                'totalnearlinesize' : convertToInteger(se.totalnearlinesize),
                'usednearlinesize'  : convertToInteger(se.usednearlinesize)}
        else:
            space_counts_se[se.uniqueid]['totalonlinesize']   += convertToInteger(se.totalonlinesize)
            space_counts_se[se.uniqueid]['usedonlinesize']    += convertToInteger(se.usedonlinesize)
            space_counts_se[se.uniqueid]['totalnearlinesize'] += convertToInteger(se.totalnearlinesize)
            space_counts_se[se.uniqueid]['usednearlinesize']  += convertToInteger(se.usednearlinesize)

    return space_counts_se

def getJobNumbersFromGlueCE():
    # To get a list of gluece and then count the number of jobs
    job_counts_ce = {}
    qs_ce = gluece.objects.filter()
    for ce in qs_ce:
        if ce.hostingcluster not in job_counts_ce:
            if convertToInteger(ce.waitingjobs) != 444444:
                waiting_jobs = convertToInteger(ce.waitingjobs)     
            else:
                waiting_jobs = 0
            job_counts_ce[ce.hostingcluster] = {
                'runningjobs' : convertToInteger(ce.runningjobs),
                'waitingjobs' : waiting_jobs,
                'totaljobs'   : convertToInteger(ce.totaljobs)}
        else:
            if convertToInteger(ce.waitingjobs) != 444444:
                waiting_jobs = convertToInteger(ce.waitingjobs)     
            else:
                waiting_jobs = 0
            job_counts_ce[ce.hostingcluster]['runningjobs'] += convertToInteger(ce.runningjobs)
            job_counts_ce[ce.hostingcluster]['waitingjobs'] += waiting_jobs
            job_counts_ce[ce.hostingcluster]['totaljobs']   += convertToInteger(ce.totaljobs)
            
    return job_counts_ce
"""

def convertToInteger(number):
    try:
        return int(number)
    except (ValueError), error:
        return 0

#def getGlueServiceByUniqueidType(unique_id, type_name):
#    qs_service = glueservice.objects.filter(uniqueid = unique_id, type = type_name)
#    # CAUTION!, alert exception or warning if there is more than one record
#    return qs_service[0]


# -------------------------------------------
# -- Topology data model related functions --
# -------------------------------------------

""" reserved """
def getEntitiesByType(type_name):
    qs_entities = Entity.objects.filter(type=type_name)
    
    return qs_entities

""" reserved """
def getEntityByUniqueidType(unique_id, type_name):
    qs_entity = Entity.objects.filter(uniqueid = unique_id, type = type_name)
    # CAUTION!, alert exception or warning if there is more than one record
    if qs_entity:
        return qs_entity[0]
    else:
        return None

""" reserved """
def getSitesInGroup(predicate_name, entity):
    # Get the list of Sites in the specified group, ex.: grid, egee roc, country, etc.
    site_list = [er.subject for er in Entityrelationship.objects.filter(predicate = predicate_name, 
                                                                        object = entity)]
        
    return site_list


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


def getQueuesInSite(site_entity):
    # Get a list of dictionaries they are queues at specified site
    # Queue: {'ce': CE entity, 'vo': VO entity}
    service_list = get_services([site_entity])
    ce_list = []
    for service in service_list:
        if service.type == 'CE': ce_list.append(service)
    
    queue_list = [{'ce':er.subject, 'vo':er.object} for er in Entityrelationship.objects.filter(
                                                    predicate   = 'ServiceVO',
                                                    subject__in = ce_list)]
    return queue_list

"""
def getNodesInSite(site_entity, node_type):
    # Get the list of nodes at specified site
    node_list = [er.object for er in Entityrelationship.objects.filter(predicate    = 'SiteService',
                                                                       subject      = site_entity,
                                                                       object__type = node_type)]
    return node_list

def getServicesInSite(site_entity):
    # Get the list of all services at specified site
    service_list = [er.object for er in Entityrelationship.objects.filter(predicate = 'SiteService',
                                                                          subject   = site_entity)]
    return service_list

def getVOsInCE(ce_entity):
    unsorted_vo_list = [er.object for er in Entityrelationship.objects.filter(predicate = 'ServiceVO',
                                                                              subject   = ce_entity)]
    # sorting list of object
    sorted_vo_list = sortObjectsByAttr(unsorted_vo_list, 'uniqueid')
    
    return sorted_vo_list


def getVOsInSite(site_entity):
    # Get a list of supported VOs at specified site
    queue_list = getQueuesInSite(site_entity)
    vo_list = [queue['vo'] for queue in queue_list]
    # remove duplicates
    distinct_vo_list = {}.fromkeys(vo_list).keys()
    # sorting list of object
    distinct_sorted_vo_list = sortObjectsByAttr(distinct_vo_list, 'uniqueid')
    
    return distinct_sorted_vo_list


def sortObjectsByAttr(object_list, attribute):
    unsorted_list = object_list
    sorted_list = [(obj.__getattribute__(attribute), obj) for obj in unsorted_list]
    sorted_list.sort()
    result_list = [obj for (attribute, obj) in sorted_list]
    
    return result_list
"""


# ---------------------------------------------------------
# -- Installed Capacity and Statistics related functions --
# ---------------------------------------------------------

def get_installed_capacity_cpu(sub_clusters_list):
    """ calculate cpu numbers in glue subcluster entities """
    physical_cpus = 0
    logical_cpus = 0
    for sub_cluster in sub_clusters_list:
        logical_cpus += convertToInteger(sub_cluster.logicalcpus)
        physical_cpus += convertToInteger(sub_cluster.physicalcpus)

    return [physical_cpus, logical_cpus]


def get_installed_capacity_storage(se_list):
    """ calculate storage space in glue se entities """
    total_online = 0
    used_online = 0
    total_nearline = 0
    used_nearline = 0 

    for se in se_list:
        total_online += convertToInteger(se.totalonlinesize)
        used_online += convertToInteger(se.usedonlinesize)
        total_nearline += convertToInteger(se.totalnearlinesize) 
        used_nearline += convertToInteger(se.usednearlinesize) 

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

        os[os_name][os_release][0] += convertToInteger(sub_cluster.physicalcpus)    
        os[os_name][os_release][1] += convertToInteger(sub_cluster.logicalcpus)

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
        total_jobs += convertToInteger(voview.totaljobs)
        running_jobs += convertToInteger(voview.runningjobs)
        if ( not convertToInteger(voview.waitingjobs) == 444444):
            waiting_jobs += convertToInteger(voview.waitingjobs)
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

"""
def countCPUsInSite(site_entity):
    logicalcpus  = 0
    physicalcpus = 0

    # To get numbers of logic and physical cpus from gluesubcluster
    # Just once to count the cpu numbers in subcluster entities
    global CPU_COUNTS_SUBCLUSTER
    if not CPU_COUNTS_SUBCLUSTER:
        CPU_COUNTS_SUBCLUSTER = getCPUNumbersFromGlueSubCluster()
    
    # Get the list of CE entities at specified site
    ce_list = getNodesInSite(site_entity, 'CE')

    for ce in ce_list:
        # To count the CPU numbers
        if ce.uniqueid in CPU_COUNTS_SUBCLUSTER:
            logicalcpus  += CPU_COUNTS_SUBCLUSTER[ce.uniqueid]['logicalcpus']
            physicalcpus += CPU_COUNTS_SUBCLUSTER[ce.uniqueid]['physicalcpus']
            
    return (logicalcpus, physicalcpus)
    
def countJobsInSite(site_entity):
    totaljobs   = 0
    runningjobs = 0
    waitingjobs = 0

    # To get numbers of runningjobs, waitingjobs, and totaljobs from gluece
    # Just once to count the job numbers in subcluster entities
    global JOB_COUNTS_CE
    if not JOB_COUNTS_CE:
        JOB_COUNTS_CE = getJobNumbersFromGlueCE()
    
    # Get the list of CE entities at specified site
    ce_list = getNodesInSite(site_entity, 'CE')

    for ce in ce_list:
        # To count job numbers
        if ce.uniqueid in JOB_COUNTS_CE:
            totaljobs   += JOB_COUNTS_CE[ce.uniqueid]['totaljobs']   
            runningjobs += JOB_COUNTS_CE[ce.uniqueid]['runningjobs']
            waitingjobs += JOB_COUNTS_CE[ce.uniqueid]['waitingjobs']
            
    return (totaljobs, runningjobs, waitingjobs) 

def countStoragesInSite(site_entity):
    totalonlinesize = 0
    usedonlinesize  = 0
    totalnearlinesize = 0
    usednearlinesize  = 0
    
    # To get storage spaces from gluese
    # Just once to count the storage spaces in se entities
    global SPACE_COUNTS_SE
    if not SPACE_COUNTS_SE:
        SPACE_COUNTS_SE = getStorageSpacesFromGlueSE()

    # Get the list of SE entities at specified site
    se_list = getNodesInSite(site_entity, 'SE')
            
    # To count the storage space
    for se in se_list:
        if se.uniqueid in SPACE_COUNTS_SE:
            totalonlinesize   += SPACE_COUNTS_SE[se.uniqueid]['totalonlinesize']
            usedonlinesize    += SPACE_COUNTS_SE[se.uniqueid]['usedonlinesize']
            totalnearlinesize += SPACE_COUNTS_SE[se.uniqueid]['totalnearlinesize']
            usednearlinesize  += SPACE_COUNTS_SE[se.uniqueid]['usednearlinesize']
            
    return (totalonlinesize, usedonlinesize, totalnearlinesize, usednearlinesize)

def countJobsInVO_Site(site_entity):
    vo_jobs = []

    queue_list = getQueuesInSite(site_entity)
    gluece = models.get_model('glue', 'gluece')
    glueces = gluece.objects.filter(gluecluster_fk__in=[queue["ce"].uniqueid for queue in queue_list])
    vo_list = getVOsInSite(site_entity)
    for vo in vo_list:
        totaljobs   = 0
        runningjobs = 0
        waitingjobs = 0
        job_dict = {}
        gluevoview = models.get_model('glue', 'gluevoview')
        voviews= gluevoview.objects.filter(localid=vo.uniqueid, gluece_fk__in=[gluece.uniqueid for gluece in glueces])
        for voview in voviews:
            totaljobs   += convertToInteger(voview.totaljobs)
            runningjobs += convertToInteger(voview.runningjobs)
            waitingjobs += convertToInteger(voview.waitingjobs)
        job_dict['voname'] = vo.uniqueid
        job_dict['totaljobs'] = totaljobs
        job_dict['runningjobs'] = runningjobs
        job_dict['waitingjobs'] = waitingjobs
        
        vo_jobs.append(job_dict)
    return vo_jobs
"""
# ------------------------------
# -- Nagios related functions --
# ------------------------------

def getNagiosStatusDict():
    """ This takes the nagios realtime status data and outputs as a dictionary object. """
    def __GetDefinitions(filename, obj):
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
    
    def __GetDirective(item, directive):
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
    hosts = __GetDefinitions(status_file, hosttoken)
    services = __GetDefinitions(status_file, servicetoken)
    for hostdef in hosts:
        host_name          = __GetDirective(hostdef, "host_name")
        current_state      = __GetDirective(hostdef, "current_state")
        plugin_output      = __GetDirective(hostdef, "plugin_output")
        last_check         = __GetDirective(hostdef, "last_check")
        has_been_checked   = __GetDirective(hostdef, "has_been_checked")
        
        status_dict[host_name]                     = {}
        status_dict[host_name]['current_state']    = convertToInteger(current_state)
        status_dict[host_name]['plugin_output']    = plugin_output
        status_dict[host_name]['last_check']       = last_check
        status_dict[host_name]['has_been_checked'] = convertToInteger(has_been_checked)

        for servicedef in services:
            if (__GetDirective(servicedef, "host_name") == host_name):
                service_description = __GetDirective(servicedef, "service_description")
                current_state       = __GetDirective(servicedef, "current_state")
                plugin_output       = __GetDirective(servicedef, "plugin_output")
                long_plugin_output  = __GetDirective(servicedef, "long_plugin_output")
                last_check          = __GetDirective(servicedef, "last_check")
                has_been_checked    = __GetDirective(servicedef, "has_been_checked")
                
                status_dict[host_name][service_description]                       = {}
                status_dict[host_name][service_description]['current_state']      = convertToInteger(current_state)
                status_dict[host_name][service_description]['plugin_output']      = plugin_output
                status_dict[host_name][service_description]['long_plugin_output'] = long_plugin_output
                status_dict[host_name][service_description]['last_check']         = last_check
                status_dict[host_name][service_description]['has_been_checked']   = convertToInteger(has_been_checked)
    
    return status_dict


def getNodesOverallStatus(status_dict, hostname_list, check_name_phrase):
    overall_status = -1
    has_been_checked = 1
    for hostname in hostname_list:
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

def getNagiosStatusStr(current_state, has_been_checked):
    if (current_state == 0):
        if (has_been_checked == 0):
            return 'PENDING'
        else:
            return 'OK'
    elif (current_state == 1):
        return 'WARNING'
    elif (current_state == 2):
        return 'CRITICAL'
    elif (current_state == 3):
        return 'UNKNOWN'
    else:
        #return "Unknown Status %s" % (current_state)
        return 'N/A'

def getNagiosStatus(nagios_status, check, hostname):

    status_dict = {'hostname': hostname,
                   'current_state': 'N/A'
                   }
    if ( nagios_status.has_key(hostname) ) :
        if ( nagios_status[hostname].has_key(check) ) :
            status_dict['check']              = check
            current_state                     = nagios_status[hostname][check]['current_state']
            has_been_checked                  = nagios_status[hostname][check]['has_been_checked']
            status_dict['current_state']      = getNagiosStatusStr(current_state, has_been_checked)
            status_dict['plugin_output']      = nagios_status[hostname][check]['plugin_output']
            status_dict['long_plugin_output'] = nagios_status[hostname][check]['long_plugin_output']
            status_dict['last_check']         = nagios_status[hostname][check]['last_check']

    return status_dict


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
