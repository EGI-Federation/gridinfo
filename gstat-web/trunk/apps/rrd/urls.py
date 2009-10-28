from django.conf.urls.defaults import *

urlpatterns = patterns('rrd.views',
    # nagios-level
    (r'^Nagios/(?P<host_name>[^/]*)/(?P<check_name>[\w-]+)/(?P<data_source>[\w-]+)/(?P<start_time>[\w-]+)/$', 'nagios_level'),
    # vo-level
    (r'^VO/(?P<site_name>[^/]*)/(?P<vo>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'vo_level'),
    (r'^VO/(?P<site_name>[^/]*)/(?P<vo>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/(?P<small>small)/$', 'vo_level'),
    # queue-level                       
    (r'^Queue/(?P<vo>[^/]*)/(?P<ce>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'queue_level'), 
    # site-level
    (r'^Site/(?P<site_name>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'site_level'),
    (r'^Site/(?P<site_name>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/(?P<small>small)/$', 'site_level'),
    # graphs viewing tabs page
    (r'^Nagios/.+/.+/.+/$', 'graph_tabs'),
    (r'^VO/.+/.+/.+/$', 'graph_tabs'),
    (r'^Queue/.+/.+/.+/$', 'graph_tabs'),
    # entity-level and attribute-level
    (r'^(?P<entity_type>\w+)/(?P<uniqueid>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'entity_level'),
    # graphs viewing tabs page
    (r'^.+/.+/.+/$', 'graph_tabs'),
)

