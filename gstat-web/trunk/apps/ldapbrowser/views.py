from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from django.shortcuts import render_to_response, get_object_or_404
from topology.models import Entity
import gsutils
import string

def index(request, url="", ldapurl=""):
    query = Entity.objects.filter(type='bdii_top')
    hostnames = []
    for bdii in query:
        label = bdii.uniqueid[7:string.rfind(bdii.uniqueid, ':')]
        # Select the default host to show
        if (url == label): hostnames.append([label, bdii.uniqueid, 1])
        else: hostnames.append([label, bdii.uniqueid, 0])
    if ldapurl == "": display = 'block';
    else: display = 'none';
    return render_to_response('ldapbrowser.html',
                              {'hostnames': hostnames, 'ldapurl': ldapurl,
                               'display': display, 'ldapbrowser_active': 1})

def browse(request):
    # Parsing of needed attributes
    if 'dn' in request.GET: dn = request.GET['dn']
    else: return HttpResponse('')
    if 'entry' in request.GET: filter = 'base'
    else: filter = 'one dn'
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
        tuple = result.values()[0] # Only 1 tuple is present
        for key in tuple.keys():
            for value in tuple[key]:
                table.append([key, value])
        return render_to_response('entrypage.html', {'table':table, 'dn':dn})
    else:
        keys = [x.lower() for x in result.keys()]
        keys.sort()
        return HttpResponse(unicode(keys))
