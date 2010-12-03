from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import html
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from topology.models import Entity
from topology.models import Entityrelationship
from core.utils import *
import gridmap
import sys

# Stable view
def index(request):
    return render_to_response('gridmap.html', {'filters_enabled': True})


def mappings(request):
    vos = Entity.objects.filter(type='VO')
    content = {}
    for vo in vos:
        content[vo.uniqueid] = None
    content = '{"vomap": %s}' % (json.dumps(content))
    return HttpResponse(content, mimetype='application/json')  

def samservices(request):
    content = '{"siteservices": ["ArcCE", "CE", "OSGBestm", "OSGCE", "OSGSRMv1", "OSGSRMv2", "SRMv2", "sBDII"], "allservices": ["APEL", "ArcCE", "BDII", "CE", "CREAMCE", "FTS", "LFC", "LFC_C", "LFC_L", "MPI", "MyProxy", "OSGBestm", "OSGCE", "OSGGdFTP", "OSGSRMv1", "OSGSRMv2", "RB", "RGMA", "SE", "SRM", "SRMv1", "SRMv2", "VOBOX", "VOMS", "gCE", "gRB", "sBDII"]}'
    return HttpResponse(content, mimetype='application/json')  


# Generates the JSON required for the GridMap
# JSON structure:
# {
# "regions" : {"REGION": [x, y, w, h] , ... },
# sitedata": {"SITE": [metric, ...4, {"host": [metric, ...], ... }], ... }
# topodata : { "REGION" : ["SITE", ...] , ... }
# "sites": {"SITE": [ x, y, w, h] , ... },
# "metricnames": ["metric", ... ]
# }
#
# Call gridmap.create_GridMap_layout function
def treemap_old(request, type='EGEE_ROC'):

    # Get the list of sites and the grouping (topology)
    groups = get_groups(type=type)
    topology = {}
    site_list = []
    for group in groups:
        topology[group.uniqueid]=[]
        sites = get_sites(type=type, value=group.uniqueid, groups=[group])
        site_list.extend(sites)        
        for site in sites:
            topology[group.uniqueid].append(site.uniqueid)

    # Get the list of clusters
    clusters_list = get_services(site_list, service_type="CE")

    # Create a mapping between sites and clusters
    cluster_site_mapping = {}
    relationships = Entityrelationship.objects.select_related('object').filter(predicate='SiteService', object__in=clusters_list)
    # relationships = Entityrelationship.objects.filter(predicate='SiteService').filter(object__type__exact='CE')
    for relation in relationships:
        cluster_site_mapping[relation.object.uniqueid] = relation.subject.uniqueid

    #Get a list of subclusters
    sub_clusters_list = get_gluesubclusters(clusters_list)
   
    # Build sitedata data structure
    sitedata = {} 
    for sub_cluster in sub_clusters_list:
        try:
            site = cluster_site_mapping[sub_cluster.gluecluster_fk]
        except:
            sys.stderr.write("Could not find site for %s \n" % (sub_cluster.gluecluster_fk))
        metric = int(sub_cluster.logicalcpus)
        if( not sitedata.has_key(site)):
            sitedata[site] = [0, {}]
        sitedata[site][0] += metric
        sitedata[site][1][sub_cluster.uniqueid] = [metric]

    posx = 0
    posy = 0
    width = 1253  # request.GET["width"]
    height = 403  # request.GET["height"]
    title_height = 12

    regions, sites = gridmap.create_GridMap_layout(posx, posy, width, height, title_height, topology, sitedata, lambda x: x[0] )

    content = {}
    content["regions"] = regions
    content["sitedata"] = sitedata
    content["topodata"] = topology       
    content["sites"] = sites
    content["metricnames"] = {}
    content = json.dumps(content)
    return HttpResponse(content, mimetype='application/json')  

def statuslatest(request, type='EGEE_ROC'):

    groups = get_groups(type=type)
    topology = {}
    site_list = []
    for group in groups:
        topology[group.uniqueid]=[]
        sites = get_sites(type=type, value=group.uniqueid, groups=[group])
        site_list.extend(sites)

    site_bdii_list = get_services(site_list, service_type="bdii_site")
    hostnames = []
    for bdii in site_bdii_list:
        hostnames.append(bdii.hostname)

    # Create a mapping between sites and bdiis                               
    bdii_site_mapping = {}
    relationships = Entityrelationship.objects.select_related('object').filter(predicate='SiteService', object__in=site_bdii_list)
    for relation in relationships:
        bdii_site_mapping[relation.object.hostname] = relation.subject.uniqueid

    # Get metric result
    #nagios_status = get_nagios_status_dict()
    #(status, has_been_checked) = get_hosts_overall_nagios_status(nagios_status, hostnames, '^check-.+')
    #site_number_or_status = get_nagios_status_str(status, has_been_checked)

    data ={}
    for host in hostnames:
        data[bdii_site_mapping[host]] = ["ok"]


    content = {}
    content["msec"] = 166
    content["data"] = data
    content["ts"] = 1239005986
    content["metricnames"] =  ["Default", "ArcCE", "CE", "OSGBestm", "OSGCE", "OSGGdFTP", "OSGSRMv1", "OSGSRMv2", "SRMv2", "sBDII"]
    content = json.dumps(content)
    return HttpResponse(content, mimetype='application/json')  

def treemap_newer(request, type='EGEE_ROC'):

    # Get the list of sites and the grouping (topology)
    groups = get_groups(type=type)
    topology = {}
    site_list = []
    for group in groups:
        topology[group.uniqueid]=[]
        sites = get_sites(type=type, value=group.uniqueid, groups=[group])
        site_list.extend(sites)        
        for site in sites:
            topology[group.uniqueid].append(site.uniqueid)

    # Get the list of clusters
    clusters_list = get_services(site_list, service_type="CE")

    # Create a mapping between sites and clusters
    cluster_site_mapping = {}
    relationships = Entityrelationship.objects.select_related('object').filter(predicate='SiteService', object__in=clusters_list)
    # relationships = Entityrelationship.objects.filter(predicate='SiteService').filter(object__type__exact='CE')
    for relation in relationships:
        cluster_site_mapping[relation.object.uniqueid] = relation.subject.uniqueid

    #Get a list of subclusters
    sub_clusters_list = get_gluesubclusters(clusters_list)
   
    # Build sitedata data structure
    sitedata = {} 
    for sub_cluster in sub_clusters_list:
        try:
            site = cluster_site_mapping[sub_cluster.gluecluster_fk]
        except:
            sys.stderr.write("Could not find site for %s \n" % (sub_cluster.gluecluster_fk))
        metric = int(sub_cluster.logicalcpus)
        if( not sitedata.has_key(site)):
            sitedata[site] = [0, {}]
        sitedata[site][0] += metric
        sitedata[site][1][sub_cluster.uniqueid] = [metric]

    status_data = get_status_for_sites(site_list)

    color_map = { "OK" : "#32CD32",
                  "WARN" : "#FFA500",
                  "CRITCAL" : "#FF0000",
                  "N/A" : "#808080" }
        

    content = { "id": type, "name": type }
    content["data"] = { "$area": 195, "$color": 5 }
    parents = []
    for region in topology.keys():
        children = []
        parent_size = 0
        for site in topology[region]:

            try: 
                size = sitedata[site][0]
                parent_size += size
                status = color_map[status_data[site]]
                
                object = { "id": site, "name": site, "children": [] }
                object["data"] = { "$area": size, "$color": status }
                children.append(object)
            except KeyError:
                pass        
        parent = { "id": region, "name": region }
        parent["data"] = { "$area": parent_size, "$color": 5 }
        parent["children"] = children
        parents.append(parent)

    content["children"] = parents
        
            
#    content["sitedata"] = sitedata
 #   content["topodata"] = topology       
#    content["sites"] = sites
#    content["metricnames"] = {}
    content = json.dumps(content)
    return HttpResponse(content, mimetype='application/json')  

def treemap(request, type='EGEE_ROC', value='ALL'):
    data = []

    groups = get_groups(type=type)
    topology = {}
    site_list = []
    for group in groups:
        topology[group.uniqueid]=[]
        sites = get_sites(type=type, value=group.uniqueid, groups=[group])
        site_list.extend(sites)       
        for site in sites:
            topology[group.uniqueid].append(site.uniqueid)

    site_data  = get_installed_capacities(site_list)
    status_data = get_status_for_sites(site_list)
    data = []
    for group in topology.keys():
        row = []
        for site_id in topology[group]:
            try: 
                site_state = [ site_id,  site_data[site_id][1], status_data[site_id]]
                row.append(site_state)  
            except KeyError:
                pass
        data.append([group,row]) 

    content = json.dumps(data)
    return HttpResponse(content, mimetype='application/json')  
