from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import html
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from topology.models import Entity

# Stable view
def index(request):
    return render_to_response('gridmap.html')

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

def treemap(request):
    content =''
    return HttpResponse(content, mimetype='application/json')  

def statuslatest(request):
    content =''
    return HttpResponse(content, mimetype='application/json')  
