from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import html
from django.shortcuts import render_to_response
from topology.models import Entity, Entityrelationship
from glue.models import gluesite
from core.utils import countCPUsInSite, countStoragesInSite
import random
from geo import countryInfo

known_types = ['GRID',
               'EGEE_ROC',
               'WLCG_TIER',
               'Country']

predicates  = {'GRID': 'SiteGrid',
               'EGEE_ROC': 'SiteEgeeRoc',
               'WLCG_TIER': 'SiteWlcgTier',
               'Country': 'SiteCountry'}

# Stable view
def index(request):
    #return render_to_response('geo-index.html', {'geo_active': 1})
    return HttpResponsePermanentRedirect('/gstat/geo/openlayers')

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
           {'zoom':zoom, 'lon':lon, 'lat':lat, 'layers':layers, 'geo_active': 1,
            'filters_enabled': True})

# Stable view
def fullscreen(request):
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
    
    kml = '/gstat/geo/kml'
    if 'kml' in request.GET:
        kml = request.GET['kml']

    overlay = ''
    if 'overlay' in request.GET:
        overlay = request.GET['overlay']

    # Render
    return render_to_response('fullscreen.html',
           {'zoom':zoom, 'lon':lon, 'lat':lat, 'layers':layers, 'kml':kml,
            'overlay':overlay})


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
            entities = Entity.objects.filter(type = type)
        else:
            entities = Entity.objects.filter(uniqueid__iexact = value, 
                                             type = type)
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

# Development view
def overlay(request, type=''):
    if (type == 'egee-europe'):
        popups = []
        countries = Entity.objects.filter(type = 'Country')
        egeeEntity = Entity.objects.filter(uniqueid = 'EGEE')[0]
        for country in countries:
            if (country.uniqueid in countryInfo.countriesInEgeeEurope):
                site_list = []
                for er in Entityrelationship.objects.filter(
                                   predicate = 'SiteCountry', object = country):
                    if (len(Entityrelationship.objects.filter(
                                   predicate = 'SiteGrid', object = egeeEntity,
                                   subject = er.subject)) > 0):
                        site_list.append(er.subject)
                if (len(site_list) > 0):
                    logicalcpus  = 0
                    physicalcpus = 0
                    totalsize    = 0
                    usedsize     = 0
                    for site in site_list:
                        (logicalcpus_, physicalcpus_) = countCPUsInSite(site)
                        (totalonlinesize_, usedonlinesize_, totalnearlinesize_, usednearlinesize_)       = countStoragesInSite(site)
                        logicalcpus  += logicalcpus_
                        physicalcpus += physicalcpus_
                        totalsize    += totalonlinesize_ + totalnearlinesize_
                        usedsize     += usedonlinesize_ + usednearlinesize_
                    totalsize = int(totalsize / 1024) # TB
                    usedsize = int(usedsize / 1024) # TB
                    html = "<span style='font-size:xx-small;><tt>"
                    html += countryInfo.countriesInEgeeEurope[country.uniqueid][2]
                    html += "<br/>s:" + str(len(site_list))
                    html += "<br/>c:" + str(physicalcpus)
                    html += "<br/>t:" + str(totalsize)
                    html += "</tt></span>"
                    popups.append([country.uniqueid,
                                   countryInfo.countriesInEgeeEurope[country.uniqueid][0],
                                   countryInfo.countriesInEgeeEurope[country.uniqueid][1],
                                   html])

        response = render_to_response('overlay-egee-europe.js',
                                      {'popups': popups})

    return response