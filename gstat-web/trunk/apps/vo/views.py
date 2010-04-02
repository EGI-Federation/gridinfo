from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils import html
from django.utils import simplejson as json
from core.utils import *
from topology.models import Entity,Entityrelationship
from glue.models import glueservice,gluece, gluevoview
import gsutils
import socket
import re
import time


def overview(request, vo_name=""):

    return render_to_response('overview_vo.html', 
                              {'vo_active': 1})


@cache_page(60 * 10)
def get_json(request, vo_name="", type=""):
    
    voviews = []
    cluster_list = []
    
    if type == "CE_Status":
        site_cluster = get_vo_services(vo_name, 'CE')
        for site in site_cluster:
            cluster_list.extend(site_cluster[site])

    voviews = get_gluevoviews(cluster_list, vo_name)

    data = []
    for voview in voviews:
        row = []
        row.append(voview.localid)
        row.append(voview.totaljobs)
        row.append(voview.runningjobs)
        row.append(voview.waitingjobs)
        row.append(voview.freejobslots)
        row.append(voview.estimatedresponsetime)
        row.append(voview.worstresponsetime)
        row.append(voview.glueceuniqueid)
        #row.append(voview.gluece_fk)
        
        data.append(row)  

    content = '{"aaData": %s}' % (json.dumps(data))
    return HttpResponse(content, mimetype='application/json')  

def treeview(request, vo_name=""):
    
    def __getDirective(item, directive):
        """ parse an object definition, return the directives """
        pattern = re.compile(directive+'[=]*([\S, ]*)\n')
        m = pattern.search(item)
        print m
        if m:
            return m.group(1).strip() 
    
    # get vo list
    vo_list = Entity.objects.filter(type="VO").order_by('uniqueid')
    
    site_cluster = get_vo_services(vo_name, 'CE')
    site_se      = get_vo_services(vo_name, 'SE')
    
    cluster_list = []
    for site in site_cluster:
        cluster_list.extend(site_cluster[site])
    se_list = []
    for site in site_se:
        se_list.extend(site_se[site])
        
    # decide expanded tree node
    collapse = {}
    collapse[vo_name] = "expanded"


    #print "Starting Mapping...."
    #start_time = time.time()
    
    # Get GlueVOView entity mapping information
    ces = gluece.objects.filter(gluecluster_fk__in = [cluster.uniqueid for cluster in cluster_list])
    voviews = gluevoview.objects.filter(gluece_fk__in = [ce.uniqueid for ce in ces])
    vo_voview_mapping = get_vo_to_voview_mapping(voviews)

    cluster_ce_mapping = {}
    for ce in ces:
        if ce.gluecluster_fk not in cluster_ce_mapping:
            cluster_ce_mapping[ce.gluecluster_fk] = []
        cluster_ce_mapping[ce.gluecluster_fk].append(ce.uniqueid)
    
    ce_voview_mapping = {}
    for voview in voviews:
        if voview.gluece_fk not in ce_voview_mapping:
            ce_voview_mapping[voview.gluece_fk] = []
        ce_voview_mapping[voview.gluece_fk].append(voview.localid)
    
    cluster_vo_mapping = {}
    for cluster in cluster_list:
        if cluster.uniqueid in cluster_ce_mapping:
            for ce_uniqueid in cluster_ce_mapping[cluster.uniqueid]:
                if ce_uniqueid in ce_voview_mapping:
                    for voview_localid in ce_voview_mapping[ce_uniqueid]:
                        if cluster.uniqueid not in cluster_vo_mapping:
                            cluster_vo_mapping[cluster.uniqueid] = {}
                        try:
                            cluster_vo_mapping[cluster.uniqueid][ vo_voview_mapping[ce_uniqueid][voview_localid] ] = [ce_uniqueid, voview_localid]
                        except KeyError: continue
    
    # Get GlueSA entity mapping information
    sas = gluesa.objects.filter(gluese_fk__in = [se.uniqueid for se in se_list])
    vo_sa_mapping = get_vo_to_sa_mapping(sas)
    
    se_sa_mapping = {}
    for sa in sas:
        if sa.gluese_fk not in se_sa_mapping:
            se_sa_mapping[sa.gluese_fk] = []
        se_sa_mapping[sa.gluese_fk].append(sa.localid)
        
    se_vo_mapping = {}
    for se in se_list:
        if se.uniqueid in se_sa_mapping:
            for sa_localid in se_sa_mapping[se.uniqueid]:
                if se.uniqueid not in se_vo_mapping:
                    se_vo_mapping[se.uniqueid] = {}
                try:
                    se_vo_mapping[se.uniqueid][ vo_sa_mapping[se.uniqueid][sa_localid] ] = sa_localid
                except KeyError: continue
                
    #print "Time taken = %d" %(time.time() - start_time)    

    # Collect the node info in the vo tree
    tree_vo = []

    job = []
    if site_cluster:
        sites_unsorted = site_cluster.keys()
        sites = sort_objects_by_attr(sites_unsorted, "uniqueid")
        for site in sites:
            site_cluster[site].sort()
            cluster_ce_voview_list = []
            for cluster in site_cluster[site]:
                if cluster.uniqueid in cluster_vo_mapping:
                    if vo_name in cluster_vo_mapping[cluster.uniqueid]:
                        cluster_ce_voview_list.append( ( cluster.uniqueid, cluster_vo_mapping[cluster.uniqueid][vo_name][0], cluster_vo_mapping[cluster.uniqueid][vo_name][1] ) )
            job.append( ( site.uniqueid, tuple( cluster_ce_voview_list ) ) )
    storage = []  
    if site_se:
        sites_unsorted = site_se.keys()
        sites = sort_objects_by_attr(sites_unsorted, "uniqueid")
        for site in sites:
            site_se[site].sort()
            se_sa_list = []
            for se in site_se[site]:
                if se.uniqueid in se_vo_mapping:
                    if vo_name in se_vo_mapping[se.uniqueid]:
                        se_sa_list.append( ( se.uniqueid, se_vo_mapping[se.uniqueid][vo_name] ) )
            storage.append( ( site.uniqueid, tuple( se_sa_list ) ) )
            
    if vo_name:    
        tree_vo.append( ( vo_name, tuple(job), tuple(storage) ) )
        
    # decide the default viewing content in iframe of treeview page
    url = ""
    if vo_name != "":
        url = "/gstat/vo/"+vo_name+"/overview/"

    # get LDAP URI o reference BDII 
    ldapuri = "ldap://lcg-bdii.cern.ch:2170/mds-vo-name=local,o=grid"
    ref_bdii_file="/etc/gstat/ref-bdii.conf"
    try:
        file = open(ref_bdii_file)
        content = file.read().replace("\t"," ")
        file.close
        BDII_HOST = __getDirective(content, "BDII_HOST")
        BDII_PORT = __getDirective(content, "BDII_PORT")
        BDII_BIND = __getDirective(content, "BDII_BIND")
        ldapuri = "ldap://" + BDII_HOST + ":" + BDII_PORT + "/" + BDII_BIND
    except(IOError):
        print "GStat reference BDII file doesn't exist: %s" % ref_bdii_file
        
    return render_to_response('treeview_vo.html', 
                              {'vo_active':        1,
                               'vo_list':          vo_list,
                               'vo_name':          vo_name,
                               'collapse':         collapse,
                               'tree_vo':          tree_vo,
                               'url':              url,
                               'ldapuri':          ldapuri})


