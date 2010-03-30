from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils import html
from core.utils import *
from topology.models import Entity
import gsutils
import socket
import re
import time


def treeview(request, vo_name=""):
    # get vo list
    vo_list = Entity.objects.filter(type="VO").order_by('uniqueid')
    
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

    return render_to_response('treeview_vo.html', {'vo_active':        1,
                                                   'vo_list':          vo_list,
                                                   'vo_name':          vo_name,
                                                   'collapse':         collapse,
                                                   'tree_vo':          tree_vo,
                                                   'url':              url})


