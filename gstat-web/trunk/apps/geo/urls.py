from django.conf.urls.defaults import *

urlpatterns = patterns('geo.views',
    (r'^$', 'index'),
    (r'^openlayers$', 'openlayers'),
    (r'^openlayers/fullscreen', 'fullscreen'),
    (r'^gmap$', 'gmap'),
    (r'^kml$', 'kml'),
    (r'^kml/(?P<type>\w+)/(?P<value>[A-Za-z0-9- :/."_]+)$', 'kml'),
    (r'^overlay/(?P<type>[A-Za-z-]+)$', 'overlay'),
)
