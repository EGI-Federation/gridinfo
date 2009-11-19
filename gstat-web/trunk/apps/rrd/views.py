from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from core.utils import *
import os, time


# -----------------------------------
# -- RRD graphs rendering function --
# -----------------------------------
def graph_render(graph_cmd):
    debug = False
    if graph_cmd == 'N/A' or debug:
        response = HttpResponse(mimetype="text/html")
        response.write(graph_cmd)
    else:
        image = os.popen(graph_cmd, 'rb').read()
        response = HttpResponse(mimetype="image/png")
        response.write(image)
        response['Content-Length'] = len(image)

    return response

# -------------------------------------------
# -- rrd graph command composing functions --
# -------------------------------------------
def rrdgraph_cmd_options(start_time, title, label, small=False):
    graph_cmd = ''
    if small: width=200
    else:     width=450
    
    graph_cmd = \
        '/usr/bin/rrdtool graph "-"' +\
        ' --imgformat=PNG' +\
        ' --start=%s' %(start_time) +\
        ' --end=-300' +\
        ' --title="%s"' %(title) +\
        ' --rigid' +\
        ' --base=1000' +\
        ' --height=100' +\
        ' --width=%s' %(width) +\
        ' --alt-autoscale-max' +\
        ' --lower-limit=0' +\
        ' --vertical-label="%s"' %(label) +\
        ' --slope-mode'
    if small:
        graph_cmd += \
        ' --font TITLE:8:Arial' +\
        ' --font AXIS:7:Arial' +\
        ' --font LEGEND:7:Arial' +\
        ' --font UNIT:8:Arial'
    else:
        graph_cmd += \
        ' --units-exponent=0' +\
        ' --font TITLE:9:Arial' +\
        ' --font AXIS:8:Arial' +\
        ' --font LEGEND:9:Arial' +\
        ' --font UNIT:9:Arial'
              
    return graph_cmd     

def rrdgraph_cmd_gprint(variable_name, small=False):
    if small:
        graph_cmd = \
        ' GPRINT:'+variable_name+':LAST:"NOW\:%2.1lf%s"' +\
        ' GPRINT:'+variable_name+':MAX:"MAX\:%2.1lf%s"' +\
        ' GPRINT:'+variable_name+':AVERAGE:"AVG\:%2.1lf%s\\n"'
       
    else:
        graph_cmd = \
        ' GPRINT:'+variable_name+':LAST:"NOW\:%8.2lf%s\\t"' +\
        ' GPRINT:'+variable_name+':MAX:"MAX\:%8.2lf%s\\t"' +\
        ' GPRINT:'+variable_name+':AVERAGE:"AVG\:%8.2lf%s\\n"' 

        
    return graph_cmd

# ----------------------------------
# -- Graphs viewing page function --
# ----------------------------------
def graph_tabs(request):
    tabnames = ["Hourly", "Daily", "Weekly", "Monthly", "Yearly"]
    timestamps = ["e-3h", "e-1d", "e-1w", "e-1m", "e-1y"]
    
    return render_to_response('graph_tabs.html', 
                              {'tabnames':   tabnames,
                               'timestamps': timestamps}) 
    
# ----------------------------------
# -- Site-level graphing function --
# ----------------------------------
def site_level(request, site_name, attribute, start_time, small=False):
    """ Site-level summarized graph """
    if attribute in ['online', 'nearline']:
        graph_cmd = site_storage_graph(site_name, attribute, start_time, small)
    elif attribute == 'cpu':
        graph_cmd = site_cpu_graph(site_name, start_time, small)
    elif attribute == 'job':
        graph_cmd = site_job_graph(site_name, start_time, small)
        
    return graph_render(graph_cmd)
    
# ------------------------------------
# -- Entity-level graphing function --
# ------------------------------------
def entity_level(request, entity_type, uniqueid, attribute, start_time):
    """ Entity-level summarized graph """
    if entity_type == 'SE' and attribute in ['online', 'nearline']:
        graph_cmd = se_storage_graph(uniqueid, attribute, start_time)
    elif entity_type == 'SubCluster' and attribute == 'cpu':
        graph_cmd = subcluster_cpu_graph(uniqueid, start_time)
    elif entity_type == 'Cluster' and attribute == 'job':
        graph_cmd = cluster_job_graph(uniqueid, start_time)
    else: # single attribute 
        graph_cmd = attribute_graph_cmd(entity_type, uniqueid, attribute, start_time)
        
    return graph_render(graph_cmd)

# --------------------------------
# -- VO-level graphing function --
# --------------------------------
def vo_level(request, site_name, vo, attribute, start_time, small=False):
    """ VO-level summarized graph """
    if attribute == 'job':
        graph_cmd = vo_job_graph(site_name, vo, start_time, small)
        
    return graph_render(graph_cmd)

# -----------------------------------
# -- Queue-level graphing function --
# -----------------------------------
def queue_level(request, vo, ce, attribute, start_time):
    """ Queue-level summarized graph """
    if attribute == 'job':
        graph_cmd = queue_job_graph(vo, ce, start_time)
        
    return graph_render(graph_cmd)

# -----------------------------------
# -- Nagios-level graphing function --
# -----------------------------------
def nagios_level(request, host_name, check_name, data_source, start_time):
    """ Nagios monitoring graph """
    rrd_dir = '/var/lib/pnp4nagios'
    
    # mapping pnp4nagios data-source name
    datasource_names = {"check-bdii-freshness": {"freshness": "1", "entries": "2"},
                        "check-bdii-sites"    : {"time": "1", "entries": "2"},
                        "check-bdii-services" : {"time": "1", "entries": "2"},
                        "check-ce"            : {"errors": "1", "warnings": "2", "info": "3"},
                        "check-sanity"        : {"errors": "1", "warnings": "2", "info": "3"},
                        "check-se"            : {"errors": "1", "warnings": "2", "info": "3"},
                        "check-service"       : {"errors": "1", "warnings": "2", "info": "3"},
                        "check-site"          : {"errors": "1", "warnings": "2", "info": "3"}}
    # mapping units
    label_names = {"freshness": "seconds",
                  "entries":    "entries",
                  "time":       "seconds",
                  "errors":     "error messages",
                  "warnings":   "warning messages",
                  "info":       "information messages"}
    
    datasource_colors = {"freshness": "#CBE9E6",
                         "entries":   "#CCFF66",
                         "time":      "#D8BFD8",
                         "errors":    "#FFBBBB",
                         "warnings":  "#F9FD9E",
                         "info":      "#DBDBDB"}
    
    title= "BDII: %s, Check Command: %s" %(host_name, check_name)
    label = label_names[data_source]
    graph_cmd = rrdgraph_cmd_options(start_time, title, label)
    rrd_file = '%s/%s/%s.rrd' %(rrd_dir, str(host_name).replace('/',''), check_name)
    datasource = datasource_names[check_name][data_source]
    graph_cmd += \
        ' DEF:var1="%s":%s:AVERAGE' %(rrd_file, datasource) +\
        ' AREA:var1%s:"%s"' %(datasource_colors[data_source], data_source.capitalize()) +\
        ' GPRINT:var1:LAST:"NOW\:%8.2lf %s"' +\
        ' GPRINT:var1:MAX:"MAX\:%8.2lf %s"' +\
        ' GPRINT:var1:AVERAGE:"AVG\:%8.2lf %s\\n"' 

    return graph_render(graph_cmd)

# --------------------------------------
# -- Storage space graphing functions --
# --------------------------------------
def site_storage_graph(site_name, attribute, start_time, small=False):
    """ Site-level summarized storage space"""
    site_entity = get_unique_entity(site_name, 'Site')
    service_list = get_services([site_entity])
    uniqueids = []
    for service in service_list:
        if service.type == 'SE': uniqueids.append(service.uniqueid)

    graph_cmd = storage_graph_cmd(uniqueids, attribute, start_time, site_name, small)
        
    return graph_cmd

def se_storage_graph(uniqueid, attribute, start_time):
    """ SE-level storage space """
    graph_cmd = storage_graph_cmd([uniqueid], attribute, start_time)

    return graph_cmd

def storage_graph_cmd(uniqueids, attribute, start_time, site_name='', small=False):
    """ To compose RRD graph command """
    if uniqueids == []:
        # need to refactor for the empty result
        return 'N/A'
    rrd_dir = '/var/cache/gstat/rrd/SE'

    if site_name == '':
        title= "%s Storage Space (GlueSE: %s)" %(attribute.capitalize(), uniqueids[0])
    else:
        title= "%s Storage Space (Site: %s)" %(attribute.capitalize(), site_name)
    label = "GB"
    graph_cmd = rrdgraph_cmd_options(start_time, title, label, small)

    datasources = {'online':   ['totalonlinesize', 'usedonlinesize'],
                   'nearline': ['totalnearlinesize', 'usednearlinesize']}

    cdef_total = []
    cdef_used = []
    count = 0
    for uniqueid in uniqueids:
        rrd_file = '%s/%s/%s.rrd' %(rrd_dir, str(uniqueid).replace('/',''), attribute)
        if(not os.path.exists(rrd_file)):
            continue
        count += 1
        vname_total = 't_%s' %(count)
        vname_used  = 'u_%s' %(count)
        if len(uniqueids) == 1:
            cdef_total.append(vname_total)
            cdef_used.append(vname_used)
        else:
            cdef_total += ['TIME', str(int(time.time())-600), 'GT', vname_total, vname_total, 'UN', '0', vname_total, 'IF', 'IF']
            cdef_used += ['TIME', str(int(time.time())-600), 'GT', vname_used, vname_used, 'UN', '0', vname_used, 'IF', 'IF']
        if count != 1:
            cdef_total.append('+')
            cdef_used.append('+')
       
        graph_cmd += \
        ' DEF:%s="%s":%s:AVERAGE' %(vname_total, rrd_file, datasources[attribute][0])+\
        ' DEF:%s="%s":%s:AVERAGE' %(vname_used, rrd_file, datasources[attribute][1])
    graph_cmd += \
        ' CDEF:total=%s' %(','.join(cdef_total)) +\
        ' CDEF:used=%s' %(','.join(cdef_used))
    graph_cmd += \
        ' CDEF:free=total,used,-' +\
        ' AREA:used#669900:"Used%sSize"' %(attribute.capitalize()) +\
        rrdgraph_cmd_gprint('used', small) +\
        ' AREA:free#CCFF66:"Total%sSize":STACK' %(attribute.capitalize()) +\
        rrdgraph_cmd_gprint('total', small)
    graph_cmd += \
        ' LINE2:total#CCFF66:""'

    return graph_cmd 

# -----------------------------------
# -- CPU number graphing functions --
# -----------------------------------
def site_cpu_graph(site_name, start_time, small=False):
    """ Site-level summarized CPU number """
    site_entity = get_unique_entity(site_name, 'Site')  
    service_list = get_services([site_entity])
    sub_cluster_list = get_gluesubclusters(service_list)
    uniqueids = [subcluster.uniqueid for subcluster in sub_cluster_list]
    graph_cmd = cpu_graph_cmd(uniqueids, start_time, site_name, small)
        
    return graph_cmd

def subcluster_cpu_graph(uniqueid, start_time):
    """ SubCluster-level CPU number """
    graph_cmd = cpu_graph_cmd([uniqueid], start_time)
        
    return graph_cmd

def cpu_graph_cmd(uniqueids, start_time, site_name='', small=False):
    """ Compose RRD graph command for CPU number """
    if uniqueids == []:
        # need to refactor for the empty result
        return 'N/A'
    rrd_dir = '/var/cache/gstat/rrd/SubCluster'

    if site_name == '':
        title = "CPU Number (GlueSubCluster: %s)" %(uniqueids[0])
    else:
        title = "CPU Number (Site: %s)" %(site_name)
    label = "CPU"  
    graph_cmd = rrdgraph_cmd_options(start_time, title, label, small)

    datasources = {'cpu':   ['physicalcpus', 'logicalcpus']}

    cdef_physical = []
    cdef_logical = []
    count = 0
    for uniqueid in uniqueids:
        # rrdtool does not like the same variable name
        # rrdtool only allows variable names up to 19 characters
        rrd_file = '%s/%s/%s.rrd' %(rrd_dir, str(uniqueid).replace('/',''), 'cpu')
        if(not os.path.exists(rrd_file)):
            continue
        count += 1
        vname_physical = 'p_%s' %(count)
        vname_logical  = 'l_%s' %(count)
        if len(uniqueids) == 1:
            cdef_physical.append(vname_physical)
            cdef_logical.append(vname_logical)
        else:
            cdef_physical += ['TIME', str(int(time.time())-600), 'GT', vname_physical, vname_physical, 'UN', '0', vname_physical, 'IF', 'IF']
            cdef_logical += ['TIME', str(int(time.time())-600), 'GT', vname_logical, vname_logical, 'UN', '0', vname_logical, 'IF', 'IF']
        if count != 1:
            cdef_physical.append('+')
            cdef_logical.append('+')
    
        graph_cmd += \
        ' DEF:%s="%s":%s:AVERAGE' %(vname_physical, rrd_file, datasources['cpu'][0])+\
        ' DEF:%s="%s":%s:AVERAGE' %(vname_logical, rrd_file, datasources['cpu'][1])
    graph_cmd += \
        ' CDEF:physical=%s' %(','.join(cdef_physical)) +\
        ' CDEF:logical=%s' %(','.join(cdef_logical))
    graph_cmd += \
        ' LINE3:physical#CAF100:"PhysicalCPUs"' +\
        rrdgraph_cmd_gprint('physical', small) +\
        ' LINE3:logical#4682B4:"LogicalCPUs  "' +\
        rrdgraph_cmd_gprint('logical', small)      

    return graph_cmd 

# ------------------------------------
# -- Jobs number graphing functions --
# ------------------------------------

def site_job_graph(site_name, start_time, small=False):
    """ Site-level Jobs number """
    site_entity = get_unique_entity(site_name, 'Site')
    service_list = get_services([site_entity])
    ce_list = []
    for service in service_list:
        if service.type == 'CE': ce_list.append(service)
    queue_dict = {}
    for ce in ce_list:
        vos = get_vos([ce])
        for vo in vos:
            if vo.uniqueid not in queue_dict:
                queue_dict[vo.uniqueid] = []
            queue_dict[vo.uniqueid].append(ce.uniqueid)           

    graph_cmd = job_graph_cmd('site', queue_dict, start_time, site_name, small)
        
    return graph_cmd

def cluster_job_graph(ce_uniqueid, start_time):
    """ Cluster-level Jobs number """
    ce_entity = get_unique_entity(ce_uniqueid, 'CE')
    vo_list = get_vos([ce_entity])
    queue_dict = {}
    for vo in vo_list:
        if vo.uniqueid not in queue_dict:
            queue_dict[vo.uniqueid] = [ce_uniqueid]
            
    graph_cmd = job_graph_cmd('cluster', queue_dict, start_time)
        
    return graph_cmd

def vo_job_graph(site_name, vo_uniqueid, start_time, small=False):
    """ VO-level Jobs number """
    site_entity = get_unique_entity(site_name, 'Site')
    service_list = get_services([site_entity])
    ce_list = []
    for service in service_list:
        if service.type == 'CE': ce_list.append(service)
    queue_dict = {vo_uniqueid:[]}
    for ce in ce_list:
        vos = get_vos([ce])
        if vo_uniqueid in [vo.uniqueid for vo in vos]:
            queue_dict[vo_uniqueid].append(ce.uniqueid)
            
    graph_cmd = job_graph_cmd('vo', queue_dict, start_time, small=small)
        
    return graph_cmd

def queue_job_graph(vo_uniqueid, ce_uniqueid, start_time):
    """ Queue-level Jobs number """
    queue_dict = {vo_uniqueid: [ce_uniqueid]}
    graph_cmd = job_graph_cmd('queue', queue_dict, start_time)
        
    return graph_cmd

def job_graph_cmd(level, queue_dict, start_time, site_name='', small=False):
    """ Compose RRD graph command for Jobs number """
    if queue_dict == {}:
        # need to refactor for the empty result
        return 'N/A'
    rrd_dir = '/var/cache/gstat/rrd/VO'

    if level == 'site': # site-level
        title = "Job Number (Site: %s)" %(site_name)
    elif level == 'queue': # queue level
        title="Job Number (Cluster: %s, VO: %s)" %(queue_dict.values()[0][0], queue_dict.keys()[0])
    elif level == 'cluster': # cluster-level
        title = "Job Number (Cluster: %s)" %(queue_dict.values()[0][0])
    elif level == 'vo': # vo-level
        title = "Job Number (VO: %s)" %(queue_dict.keys()[0])
        
    label = "Jobs"
    graph_cmd = rrdgraph_cmd_options(start_time, title, label, small)

    datasources = {'job':  ['totaljobs', 'runningjobs', 'waitingjobs']}

    cdef_total = []
    cdef_running = []
    cdef_waiting = []
    count = 0
    for vo in queue_dict.keys():
        clusters = queue_dict[vo]
        for cluster in clusters:
            rrd_file = '%s/%s/%s/%s.rrd' %(rrd_dir, str(vo).replace('/',''), str(cluster).replace('/',''), 'job')
            if(not os.path.exists(rrd_file)):
                continue
            count += 1
            vname_total   = 't_%s' %(count)
            vname_running = 'r_%s' %(count)
            vname_waiting = 'w_%s' %(count)
            if len(clusters) == 1: 
                cdef_total.append(vname_total)
                cdef_running.append(vname_running)
                cdef_waiting.append(vname_waiting)
            else:
                cdef_total   += ['TIME', str(int(time.time())-600), 'GT', vname_total,   vname_total,   'UN', '0', vname_total,   'IF', 'IF']
                cdef_running += ['TIME', str(int(time.time())-600), 'GT', vname_running, vname_running, 'UN', '0', vname_running, 'IF', 'IF']
                cdef_waiting += ['TIME', str(int(time.time())-600), 'GT', vname_waiting, vname_waiting, 'UN', '0', vname_waiting, 'IF', 'IF']
            if count != 1:
                cdef_total.append('+')
                cdef_running.append('+')
                cdef_waiting.append('+')
            graph_cmd += \
            ' DEF:%s="%s":%s:AVERAGE' %(vname_total,   rrd_file, datasources['job'][0]) +\
            ' DEF:%s="%s":%s:AVERAGE' %(vname_running, rrd_file, datasources['job'][1]) +\
            ' DEF:%s="%s":%s:AVERAGE' %(vname_waiting, rrd_file, datasources['job'][2])
    graph_cmd += \
        ' CDEF:total=%s'   %(','.join(cdef_total)) +\
        ' CDEF:running=%s' %(','.join(cdef_running)) +\
        ' CDEF:waiting=%s' %(','.join(cdef_waiting))
    graph_cmd += \
        ' AREA:total#CDE9E6:"TotalJobs    "' +\
        rrdgraph_cmd_gprint('total', small) +\
        ' LINE3:running#4682B4:"RunningJobs"' +\
        rrdgraph_cmd_gprint('running', small) +\
        ' LINE3:waiting#D8BFD8:"WaitingJobs "' +\
        rrdgraph_cmd_gprint('waiting', small)
        
    return graph_cmd 

# ----------------------------------------
# -- Single attribute graphing function --
# ----------------------------------------
def attribute_graph_cmd(entity_type, uniqueid, attribute, start_time):
    rrd_dir = '/var/cache/gstat/rrd/%s' %(entity_type)
    rrd_file = '%s/%s/%s.rrd' %(rrd_dir, str(uniqueid).replace('/',''), attribute)
    
    title = "%s (%s)" %(attribute, uniqueid)
    if   entity_type == 'SE':         label = 'GB'
    elif entity_type == 'SubCluster': label = 'CPU'
    elif entity_type == 'VO':         lable = 'Jobs'
    graph_cmd = rrdgraph_cmd_options(start_time, title, label, small=False)
    graph_cmd += \
        ' DEF:attr="%s":%s:AVERAGE' %(rrd_file, attribute) +\
        ' LINE2:attr#0000FF:"%s"' %(attribute) +\
        rrdgraph_cmd_gprint('attr')         
    
    return graph_cmd
