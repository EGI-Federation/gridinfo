from django.conf.urls.defaults import *

urlpatterns = patterns('gridsite.views',
    (r'^(?P<site_name>.+)/graphs/(?P<attribute>.+)/(?P<vo_name>[^/]*)/$', 'vo_graphs'),
    (r'^(?P<site_name>.+)/graphs/(?P<attribute>.+)/$', 'site_graphs'),
    (r'^(?P<site_name>.+)/(?P<type>.+)/$', 'status'),
    (r'^(?P<site_name>.+)/$', 'overview'),
)
