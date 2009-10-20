from django.conf.urls.defaults import *

urlpatterns = patterns('geo.views',
    (r'^$', 'index'),
    (r'^openlayers', 'openlayers'),
    (r'^gmap', 'gmap'),
    (r'^kml$', 'kml'),
    (r'^kml/(?P<type>\w+)/(?P<value>\w+)$', 'kml'),
)
