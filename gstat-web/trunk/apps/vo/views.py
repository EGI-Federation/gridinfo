from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils import html
from core.utils import *
import gsutils
import socket
import re
import time


def treeview(request, vo_name=""):
    #vo_list = get_groups('VO')
    vo_site_ce = get_vo_site_service(vo_name, 'CE')
    vo_site_se = get_vo_site_service(vo_name, 'SE')
    
    # decide expanded tree node
    collapse = {}
    collapse[vo_name] = "expanded"
    
    tree_vo = []

    site_ce = []
    if vo_name in vo_site_ce:
        site_names = vo_site_ce[vo_name].keys()
        site_names.sort()
        for site_name in site_names:
            site_ce.append( ( site_name, tuple(sorted(vo_site_ce[vo_name][site_name])) ) )
    site_se = []  
    if vo_name in vo_site_se:
        site_names = vo_site_se[vo_name].keys()
        site_names.sort()
        for site_name in site_names:
            site_se.append( ( site_name, tuple(sorted(vo_site_se[vo_name][site_name])) ) )
    if vo_name:    
        tree_vo.append( ( vo_name, tuple(site_ce), tuple(site_se) ) )
        
        
    # decide the default viewing content in iframe of treeview page
    url = ""
    if type == "bdii_top":
        # e.g. /gstat/site/CERN-PROD/bdii_top/bdii118.cern.ch/all/
        url = "/".join(["", "gstat", "site", site_name, type, attribute, "all"])
    elif type == "bdii_site":
        # e.g. /gstat/site/CERN-PROD/bdii_site/bdii116.cern.ch/all/
        url = "/".join(["", "gstat", "site", site_name, type, attribute, "all"])
    elif type == "subcluster_cpu":
        # e.g. /gstat/rrd/Site/CERN-PROD/cpu/
        url = "/".join(["", "gstat", "rrd", "Site", site_name, "cpu"])
    elif type == "se_online":
        # e.g. /gstat/rrd/Site/CERN-PROD/online/
        url = "/".join(["", "gstat", "rrd", "Site", site_name, "online"])
    elif type == "se_nearline":
        # e.g. /gstat/rrd/Site/CERN-PROD/nearline/
        url = "/".join(["", "gstat", "rrd", "Site", site_name, "nearline"])
    elif type == "vo_job":
        # e.g. /gstat/rrd/VOSite/CERN-PROD/alice/job/
        url = "/".join(["", "gstat", "rrd", "VOSite", site_name, attribute, "job"])
    elif type == "vo_online":
        # e.g. /gstat/rrd/VOSite/CERN-PROD/alice/online/
        url = "/".join(["", "gstat", "rrd", "VOSite", site_name, attribute, "online"])
    elif type == "vo_nearline":
        # e.g. /gstat/rrd/VOSite/CERN-PROD/alice/nearline/
        url = "/".join(["", "gstat", "rrd", "VOSite", site_name, attribute, "nearline"])

    return render_to_response('treeview_vo.html', {'vo_name':          vo_name,
                                                   'collapse':         collapse,
                                                   'tree_vo':          tree_vo,
                                                   'url':              url,
                                                   'filters_enabled':  True})


