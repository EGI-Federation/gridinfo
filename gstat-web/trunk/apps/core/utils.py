import re

from django.db import models
from topology.models import Entity
from topology.models import Entityrelationship
from glue.models import gluesite
from glue.models import gluesubcluster
from glue.models import gluese
from glue.models import gluece
from glue.models import glueservice

CPU_COUNTS_SUBCLUSTER = None
JOB_COUNTS_CE         = None
SPACE_COUNTS_SE       = None

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
        pass

def getSubClusterByCluster(cluster_uniqueids_list=[]):
    try:
        objects = gluesubcluster.objects.filter(gluecluster_fk__in=cluster_uniqueids_list)
        return objects
    except:
        # need to re-factor
        pass  

def getCPUNumbersFromGlueSubCluster():
    # To get a list of gluesubcluster and then count the cpu numbers
    cpu_counts_subcluster = {}
    qs_subcluster = gluesubcluster.objects.filter()
    for subcluster in qs_subcluster:
        if subcluster.uniqueid not in cpu_counts_subcluster:
            cpu_counts_subcluster[subcluster.uniqueid] = {
                'logicalcpus' : int(subcluster.logicalcpus),
                'physicalcpus': int(subcluster.physicalcpus)}
        else:
            cpu_counts_subcluster[subcluster.uniqueid]['logicalcpus']  += int(subcluster.logicalcpus)
            cpu_counts_subcluster[subcluster.uniqueid]['physicalcpus'] += int(subcluster.physicalcpus)
    
    return cpu_counts_subcluster

def getStorageSpacesFromGlueSE():
    # To get a list of gluese and then count the storage spaces
    space_counts_se = {}
    qs_se = gluese.objects.filter()
    for se in qs_se:
        try:
            int(se.totalonlinesize)
            int(se.totalnearlinesize)
            int(se.usedonlinesize)
            int(se.usednearlinesize)
        except (ValueError), error:
            pass
            #print "The value is 'unset' or empty character."
        else:
            if se.uniqueid not in space_counts_se:
                space_counts_se[se.uniqueid] = {
                    'totalonlinesize'   : int(se.totalonlinesize),
                    'usedonlinesize'    : int(se.usedonlinesize),
                    'totalnearlinesize' : int(se.totalnearlinesize),
                    'usednearlinesize'  : int(se.usednearlinesize)}
            else:
                space_counts_se[se.uniqueid]['totalonlinesize']   += int(se.totalonlinesize)
                space_counts_se[se.uniqueid]['usedonlinesize']    += int(se.usedonlinesize)
                space_counts_se[se.uniqueid]['totalnearlinesize'] += int(se.totalnearlinesize)
                space_counts_se[se.uniqueid]['usednearlinesize']  += int(se.usednearlinesize)

    return space_counts_se

def getJobNumbersFromGlueCE():
    # To get a list of gluece and then count the number of jobs
    job_counts_ce = {}
    qs_ce = gluece.objects.filter()
    for ce in qs_ce:
        if ce.hostingcluster not in job_counts_ce:
            if int(ce.waitingjobs) != 444444:
                waiting_jobs = int(ce.waitingjobs)     
            else:
                waiting_jobs = 0
            job_counts_ce[ce.hostingcluster] = {
                'runningjobs' : int(ce.runningjobs),
                'waitingjobs' : waiting_jobs,
                'totaljobs'   : int(ce.totaljobs)}
        else:
            if int(ce.waitingjobs) != 444444:
                waiting_jobs = int(ce.waitingjobs)     
            else:
                waiting_jobs = 0
            job_counts_ce[ce.hostingcluster]['runningjobs'] += int(ce.runningjobs)
            job_counts_ce[ce.hostingcluster]['waitingjobs'] += waiting_jobs
            job_counts_ce[ce.hostingcluster]['totaljobs']   += int(ce.totaljobs)
            
    return job_counts_ce

#def getGlueServiceByUniqueidType(unique_id, type_name):
#    qs_service = glueservice.objects.filter(uniqueid = unique_id, type = type_name)
#    # CAUTION!, alert exception or warning if there is more than one record
#    return qs_service[0]


# -------------------------------------------
# -- Topology data model related functions --
# -------------------------------------------

def getEntitiesByType(type_name):
    qs_entities = Entity.objects.filter(type=type_name)
    
    return qs_entities

def getEntityByUniqueidType(unique_id, type_name):
    qs_entity = Entity.objects.filter(uniqueid = unique_id, type = type_name)
    # CAUTION!, alert exception or warning if there is more than one record
    return qs_entity[0]

def getSitesInGroup(predicate_name, entity):
    # Get the list of Sites in the specified group, ex.: grid, egee roc, country, etc.
    site_list = [er.subject for er in Entityrelationship.objects.filter(predicate = predicate_name, 
                                                                        object = entity)]
        
    return site_list

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

def getQueuesInSite(site_entity):
    # Get a list of dictionaries they are queues at specified site
    # Queue: {'ce': CE entity, 'vo': VO entity}
    ce_list = getNodesInSite(site_entity, 'CE')
    queue_list = [{'ce':er.subject, 'vo':er.object} for er in Entityrelationship.objects.filter(
                                                    predicate   = 'ServiceVO',
                                                    subject__in = ce_list)]
    return queue_list

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
    runningjobs = 0
    waitingjobs = 0
    totaljobs   = 0

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
            runningjobs += JOB_COUNTS_CE[ce.uniqueid]['runningjobs']
            waitingjobs += JOB_COUNTS_CE[ce.uniqueid]['waitingjobs']
            totaljobs   += JOB_COUNTS_CE[ce.uniqueid]['totaljobs']   
            
    return (runningjobs, waitingjobs, totaljobs) 

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
        status_dict[host_name]['current_state']    = int(current_state)
        status_dict[host_name]['plugin_output']    = plugin_output
        status_dict[host_name]['last_check']       = last_check
        status_dict[host_name]['has_been_checked'] = int(has_been_checked)

        for servicedef in services:
            if (__GetDirective(servicedef, "host_name") == host_name):
                service_description = __GetDirective(servicedef, "service_description")
                current_state       = __GetDirective(servicedef, "current_state")
                plugin_output       = __GetDirective(servicedef, "plugin_output")
                long_plugin_output  = __GetDirective(servicedef, "long_plugin_output")
                last_check          = __GetDirective(servicedef, "last_check")
                has_been_checked    = __GetDirective(servicedef, "has_been_checked")
                
                status_dict[host_name][service_description]                       = {}
                status_dict[host_name][service_description]['current_state']      = int(current_state)
                status_dict[host_name][service_description]['plugin_output']      = plugin_output
                status_dict[host_name][service_description]['long_plugin_output'] = long_plugin_output
                status_dict[host_name][service_description]['last_check']         = last_check
                status_dict[host_name][service_description]['has_been_checked']   = int(has_been_checked)
    
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

