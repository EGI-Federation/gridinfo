from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from topology.models import Entity
import os
from django.utils import simplejson as json

known_types = ['Country',
               'EGEE_ROC',
               'EGI_NGI',
               'GRID',
               'VO',
               'WLCG_TIER']

def initial(request):
        return HttpResponseRedirect("/gstat/geo/openlayers")

def about(request):
    return render_to_response('about.html')

def filter(request, type=''):
    options = []
    # If no type, return all types
    if (type == ''):
        options = [['Select...', '-1']]
        for key, value in known_types.iteritems():
            options.append([value, key])
    # If the type is known, return all values of that type
    elif (type in known_types):
        options = [{"key": 'ALL', "value": 'ALL'}]
        site_list = Entity.objects.filter(type=type).order_by('uniqueid')
        for site in site_list:
            options.append({"key": site.uniqueid, "value": site.uniqueid})

    content = '{"options": %s}' % (json.dumps(options))
    return HttpResponse(content, mimetype='application/json')
