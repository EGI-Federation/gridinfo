from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from topology.models import Entity
from topology.models import Entityrelationship
from summary.utils import *
import gsutils
import socket

LEFT_SIDE_MENU_LIST = [
    {'name':'Top BDII', 'url':'/gstat/summary/top/'},
    {'name':'Site BDII', 'url':'/gstat/summary/site/'},
    {'name':'Grid', 'url':'/gstat/summary/grid/'},
    {'name':'EGEE ROC', 'url':'/gstat/summary/grid/egee_roc/'},
    {'name':'WLCG Tier', 'url':'/gstat/summary/grid/WLCG/'},
    {'name':'Country', 'url':'/gstat/summary/country/'}
]
    
def summary(request):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'}]
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []
    
    # Get the list of all sites in the infrastructure
    site_list = getEntitiesByType('Site')

    # To compose the content of table 
    tbody = generateTableContentForSiteList(site_list)

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST,
                                                    'thead': thead, 
                                                    'tbody': tbody})

def bdii_view(request, type):
    global LEFT_SIDE_MENU_LIST

    if (type == 'top'):
        breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                            {'name':'Top BDII View', 'url':'/gstat/summary/top/'}]
        thead=["Hostname", "Instances", "Freshness", "Sites"]
    else:
        breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                            {'name':'Site BDII View', 'url':'/gstat/summary/site/'}]
        thead=["Hostname", "Instances", "Freshness", "Services"]
    
    tbody=[]
    
    nagios_status = getNagiosStatusDict()
    if (type == 'top'):  
        qs = Entity.objects.filter(type='bdii_top')
    else:
        qs = Entity.objects.filter(type='bdii_site')
    alias = {} 
    hosts = [] 

    for bdii in qs:
        hostname=bdii.uniqueid
        index=hostname.find(':')
        if (index > -1 ):
            hostname= hostname[index+3:]
        index=hostname.find(':')
        if (index > -1 ):
            hostname= hostname[:index]
        try:
            ips = socket.gethostbyname_ex(hostname)[2]
            for ip in ips:
                instance = socket.gethostbyaddr(ip)[0]
                if ( alias.has_key(hostname)):
                    alias[hostname].append(instance)
                else:
                    alias[hostname] = [ instance ]
        except Exception, e:
            continue

    for hostname in alias:
        instances = len(alias[hostname])
        freshness = "N/A"
        content =  "N/A"
        for host in alias[hostname]:
            if ( nagios_status.has_key(host)):
                current_state = nagios_status[host]['check-bdii-freshness']['current_state']
                has_been_checked = nagios_status[host]['check-bdii-freshness']['has_been_checked']
                freshness = getNagiosStatusStr(current_state, has_been_checked)
                if (type == 'top'):
                    current_state = nagios_status[host]['check-bdii-sites']['current_state']
                    has_been_checked = nagios_status[host]['check-bdii-sites']['has_been_checked']
                    content = getNagiosStatusStr(current_state, has_been_checked)
                else:
                    current_state = nagios_status[host]['check-bdii-services']['current_state']
                    has_been_checked = nagios_status[host]['check-bdii-services']['has_been_checked']
                    content = getNagiosStatusStr(current_state, has_been_checked)
        link="https://gstat-dev.cern.ch/nagios/cgi-bin/status.cgi?host=" + hostname
        host_name = Cell_Link(hostname, link)
        instance_counts = Cell_Link(instances, link)
        freshness_status = Cell_Status(freshness)
        content_status = Cell_Status(content)
        
        row = [ host_name, instance_counts, freshness_status, content_status ]
        tbody.append(row)
    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})
    
def grid(request):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'}]
    # response a list of Grid infrastructures
    thead = ["Grid Name", "Sites", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    # To get the list of Grid entities
    grids = getEntitiesByType('GRID')
    
    # To compose the content of table 
    tbody = generateTableContent('SiteGrid', grids, '/gstat/summary/grid')
        
    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def grid_specified(request, grid_name):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'},
                        {'name':grid_name, 'url':'/gstat/summary/grid/%s' % grid_name}]
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    grid = Entity.objects.get(uniqueid__iexact=grid_name, type='GRID')    

    # Get the list of sites in a specified Grid
    site_list = getSitesInGroup('SiteGrid', grid)

    # To compose the content of table 
    tbody = generateTableContentForSiteList(site_list)

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def egee(request):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'},
                        {'name':'EGEE',    'url':'/gstat/summary/grid/egee'}]
    thead = ["EGEE Views"]
    tbody = [[Cell_Link('EGEE All Sites',     '/gstat/summary/grid/egee/')],
             [Cell_Link('EGEE ROC',           '/gstat/summary/grid/egee_roc/')],
             [Cell_Link('EGEE Production',    '/gstat/summary/grid/egee_service/prod/')],
             [Cell_Link('EGEE PPS',           '/gstat/summary/grid/egee_service/pps/')],
             [Cell_Link('EGEE Certification', '/gstat/summary/grid/egee_service/cert/')]]

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def egee_roc(request):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'},
                        {'name':'EGEE ROC', 'url':'/gstat/summary/grid/egee_roc/'}]
    # response a list of ROCs in EGEE infrastructure
    thead = ["ROC Name", "Sites", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    # Get the list of EGEE ROCs
    egee_rocs = getEntitiesByType('EGEE_ROC')
    
    # To compose the content of table 
    tbody = generateTableContent('SiteEgeeRoc', egee_rocs, '/gstat/summary/grid/egee_roc')
 
    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})  

def egee_roc_specified(request, roc_name):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'},
                        {'name':'EGEE ROC', 'url':'/gstat/summary/grid/egee_roc/'},
                        {'name':roc_name, 'url':'/gstat/summary/grid/egee_roc/%s' % roc_name}]
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    roc = Entity.objects.get(uniqueid__iexact=roc_name, type='EGEE_ROC')    

    # Get the list of sites in a specified EGEE ROC
    site_list = getSitesInGroup('SiteEgeeRoc', roc)

    # To compose the content of table 
    tbody = generateTableContentForSiteList(site_list)
    
    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def egee_service_specified(request, service_name):
    global LEFT_SIDE_MENU_LIST
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    service = Entity.objects.get(uniqueid__iexact=service_name, type='EGEE_SERVICE')    

    # Get the list of sites in a specified EGEE service
    site_list = getSitesInGroup('SiteEgeeService', service)

    # To compose the content of table 
    tbody = generateTableContentForSiteList(site_list)

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def wlcg_tier(request):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'},
                        {'name':'WLCG Tier', 'url':'/gstat/summary/grid/WLCG/'}]
    thead = ["Tier Name", "Sites", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    # Get the list of WLCG Tiers
    wlcg_tiers = getEntitiesByType('WLCG_TIER') 
    
    # To compose the content of table 
    tbody = generateTableContent('SiteWlcgTier', wlcg_tiers, '/gstat/summary/grid/wlcg_tier')

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def wlcg_tier_specified(request, tier_name):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Grid', 'url':'/gstat/summary/grid/'},
                        {'name':'WLCG Tier', 'url':'/gstat/summary/grid/WLCG/'},
                        {'name':tier_name, 'url':'/gstat/summary/grid/WLCG/%s' % tier_name}]
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    tier = Entity.objects.get(uniqueid__iexact=tier_name,type='WLCG_TIER')    

    # Get the list of sites in a specified WLCGTier
    site_list = getSitesInGroup('SiteWlcgTier', tier)

    # To compose the content of table 
    tbody = generateTableContentForSiteList(site_list)

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})
    
def country(request):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Country', 'url':'/gstat/summary/country/'}]
    thead = ["Country Name", "Sites", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    # Get the list of countries
    countries = getEntitiesByType('Country') 
    
    # To compose the content of table 
    tbody = generateTableContent('SiteCountry', countries, '/gstat/summary/country')

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST, 
                                                    'thead': thead, 
                                                    'tbody': tbody})

def country_specified(request, country_name):
    global LEFT_SIDE_MENU_LIST
    breadcrumbs_list = [{'name':'Summary', 'url':'/gstat/summary/'},
                        {'name':'Country', 'url':'/gstat/summary/country/'},
                        {'name':country_name, 'url':'/gstat/summary/country/%s' % country_name}]
    thead = ["Site Name", "Logical CPUs", "Physical CPUs", "Storage Space", "Waiting Jobs"]
    tbody = []

    country = Entity.objects.get(uniqueid__iexact=country_name, type='Country')    

    # Get the list of sites in a specified WLCGTier
    site_list = getSitesInGroup('SiteCountry', country)

    # To compose the content of table 
    tbody = generateTableContentForSiteList(site_list)

    return render_to_response('single_table.html', {'summary_active': 1,
                                                    'breadcrumbs_list': breadcrumbs_list,
                                                    'side_menu_list': LEFT_SIDE_MENU_LIST,
                                                    'thead': thead, 
                                                    'tbody': tbody})

def generateTableContent(predicate, entity_list, link_prefix):
    # To compose the content of table 
    tbody = []
    for entity in entity_list:
        logicalcpus  = 0
        physicalcpus = 0
        totalsize    = 0
        usedsize     = 0
        runningjobs  = 0
        waitingjobs  = 0
        totaljobs    = 0
        
        # Get the list of sites in a specified Grid
        site_list = getSitesInGroup(predicate, entity)
        
        # To count the CPU and Jobs numbers for all CEs at all sites in certain Grid
        # To count the storage space on all SEs at all sites in certain Grid
        for site in site_list:
            (logicalcpus_, physicalcpus_)            = countCPUsInSite(site)
            (totalsize_, usedsize_)                  = countStoragesInSite(site)
            (runningjobs_, waitingjobs_, totaljobs_) = countJobsInSite(site)

            logicalcpus  += logicalcpus_
            physicalcpus += physicalcpus_
            totalsize    += totalsize_
            usedsize     += usedsize_                            
            runningjobs  += runningjobs_
            waitingjobs  += waitingjobs_
            totaljobs    += totaljobs_
                    
        # need to add a KeyError exception here
        entity_name   = Cell_Link(entity.uniqueid, "%s/%s/" % (link_prefix,entity.uniqueid))
        site_number   = Cell_Link(len(site_list), "")
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

        row = [entity_name, site_number, logical_cpus, physical_cpus, storage_space, jobs]
        tbody.append(row)
        
    return tbody

def generateTableContentForSiteList(site_list):
    tbody = []
    for site in site_list:
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
