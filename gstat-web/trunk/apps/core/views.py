from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from topology.models import Entity
import os

known_types = {'grids': 'GRID',
               'rocs': 'EGEE_ROC',
               'tiers': 'WLCG_TIER',
               'countries': 'Country'}

def initial(request):
    file = 'firstRun'
    if (os.access(file, os.F_OK)):
        os.remove(file)
        #return HttpResponseRedirect('/gstat/register')
        return render_to_response('registerform.html')
    else:
        return HttpResponseRedirect("/gstat/geo/openlayers")

def about(request):
    return render_to_response('about.html')

def register(request):
    return render_to_response('registerform.html')

def filter(request, type=''):
    options = []
    # If no type, return all types
    if (type == ''):
        options = [['Select...', '-1']]
        for key, value in known_types.iteritems():
            options.append([value, key])
    # If the type is known, return all values of that type
    elif (type in known_types):
        options = [['ALL', 'all']]
        site_list = Entity.objects.filter(type=known_types[type]).order_by('uniqueid')
        for site in site_list:
            options.append([site.uniqueid, site.uniqueid])

    response = render_to_response('xml', {'options': options})
    response['Content-Type'] = 'text/xml'
    response['Content-Disposition'] = 'attachment; filename=filter.xml'
    response['Content-Description'] = 'XML Filter'
    return response
