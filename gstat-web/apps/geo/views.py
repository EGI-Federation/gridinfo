from django.http import HttpResponse
from django.utils import html
from django.shortcuts import render_to_response
from topology.models import Entity
from topology.models import Entityrelationship
from glue.models import gluesite

known_types = {'grids': 'GRID',
               'rocs': 'EGEE_ROC',
               'tiers': 'WLCG_TIER',
               'countries': 'Country'}

predicates  = {'grids': 'SiteGrid',
               'rocs': 'SiteEgeeRoc',
               'tiers': 'SiteWlcgTier',
               'countries': 'SiteCountry'}

# Stable view
def index(request):
    return render_to_response('geo-index.html', {'geo_active': 1})

# Stable view
def openlayers(request):
    # Restore permalinks values or use default ones
    zoom = 2
    if 'zoom' in request.GET:
        zoom = request.GET['zoom'] 

    lon = 5
    if 'lon' in request.GET:
        lon = request.GET['lon'] 

    lat = 15
    if 'lat' in request.GET:
        lat = request.GET['lat'] 

    layers = 'B000T'
    if 'layers' in request.GET:
        layers = request.GET['layers']         

    # Render
    return render_to_response('openlayers.html',
           {'zoom':zoom, 'lon':lon, 'lat':lat, 'layers':layers, 'geo_active': 1})

# Stable view
def gmap(request):
    return render_to_response('gmap.html', {'geo_active': 1})

# Stable view
def kml(request, type='', value=''):
    sites = []
    if (type == ''):
        sites = gluesite.objects.all();
    if (type in known_types):
        # Get the entities for your type
        if (value == 'ALL'):
            entities = Entity.objects.filter(type = known_types[type])
        else:
            entities = Entity.objects.filter(uniqueid__iexact = value, 
                                             type=known_types[type])
        # Find the related entities
        related_sites = []
        for entity in entities:
            more = [er.subject for er in Entityrelationship.objects.filter(
                                            predicate = predicates[type],
                                            object = entity)]
            related_sites.extend(more)
        
        # Get the equivalent GLUE site for each entity
        for related_site in related_sites:
            more = gluesite.objects.filter(uniqueid__iexact = related_site.uniqueid)
            sites.extend(more)
    
    sites_list = []
    for site in sites:
        sites_list.append([html.escape(site.name),
                           html.escape(site.description),
                           site.longitude,
                           site.latitude])

    response = render_to_response('kml', {'sites': sites_list})
    response['Content-Type'] = 'application/vnd.google-earth.kml+xml'
    response['Content-Disposition'] = 'attachment; filename=gstat-map.kml'
    response['Content-Description'] = 'KML of The Grid sites'
    return response

# Stable view
def filter(request, type=''):
    options = []
    if (type == ''):
        options = [['Select...', '-1']]
        for key, value in known_types.iteritems():
            options.append([value, key])
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
