from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from topology.models import Entity
import os

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
        options = [['ALL', 'ALL']]
        site_list = Entity.objects.filter(type=type).order_by('uniqueid')
        for site in site_list:
            options.append([site.uniqueid, site.uniqueid])

    response = render_to_response('json', {'options': options})
    response['Content-Type'] = 'text/json'
    response['Content-Description'] = 'JSON Filter'
    response['Pragma'] = 'no-cache'
    return response
