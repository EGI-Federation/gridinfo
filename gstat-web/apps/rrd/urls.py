from django.conf.urls.defaults import *

urlpatterns = patterns('rrd.views',
    (r'^(?P<type>\w+)/(?P<uniqueid>[^/]*)/(?P<attribute>[\w-]+)\.png', 'graph_png'),
)

