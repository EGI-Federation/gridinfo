from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from django.shortcuts import render_to_response, get_object_or_404
from topology.models import Entity
import gsutils
import string

# Development view
def index(request):
    qs = Entity.objects.filter(type='bdii_top')
    hostnames = []
    for bdii in qs:
        label = bdii.uniqueid[7:string.rfind(bdii.uniqueid, ':')]
        hostnames.append([label, bdii.uniqueid])
    user_agent = request.META['HTTP_USER_AGENT'];
    if (user_agent.find('Firefox') != -1 or user_agent.find('Opera') != -1):
        return render_to_response('ldapbrowseradv.html'
                                  , {'hostnames': hostnames,
                                     'ldapbrowser_active': 1})
    else:
        return render_to_response('ldapbrowser.html'
                                  , {'hostnames': hostnames,
                                     'ldapbrowser_active': 1})

# Stable view
def browse(request):
    # Parsing of needed attributes
    if 'dn' in request.GET: 
        dn = request.GET['dn']
    else: 
        return HttpResponse('')
    
    if 'entry' in request.GET: 
        filter = 'base'
    else: 
        filter = 'one dn'

    if 'host' in request.GET:
        str = request.GET['host'][7:]
        [host, str] = str.split(':')
        [port, basedn] = str.split('/')
    else:
        host = 'prod-bdii.cern.ch'
        port = 2170
        
    # Main work
    result = gsutils.read_ldif(host, port, dn, "-s " + filter)
    if (filter == "base" ):
        table = []
        for key in result[dn].keys():
            for value in result[dn][key]:
                table.append([key, value])
        return render_to_response('entrypage.html', {'table':table, 'dn':dn})
    else:
        keys=result.keys()
        keys.sort()
        return HttpResponse(unicode(keys))