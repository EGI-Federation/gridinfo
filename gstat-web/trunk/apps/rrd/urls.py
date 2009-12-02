from django.conf.urls.defaults import *

urlpatterns = patterns('rrd.views',
    # nagios-level
    (r'^Nagios/(?P<host_name>[^/]*)/(?P<check_name>[\w-]+)/(?P<data_source>[\w-]+)/(?P<start_time>[\w-]+)/$', 'nagios_level'),
    # vo-level
    (r'^VO/(?P<site_name>[^/]*)/(?P<vo>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'vo_site_level'),
    (r'^VO/(?P<site_name>[^/]*)/(?P<vo>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/(?P<small>small)/$', 'vo_site_level'),
    # vo-cluster-level                       
    (r'^VOCluster/(?P<vo>[^/]*)/(?P<cluster>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'vo_cluster_level'), 
    # vo-se-level                       
    (r'^VOSE/(?P<vo>[^/]*)/(?P<se>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'vo_se_level'), 
    # site-level
    (r'^Site/(?P<site_name>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'site_level'),
    (r'^Site/(?P<site_name>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/(?P<small>small)/$', 'site_level'),
    # graphs viewing tabs page
    (r'^Nagios/.+/.+/.+/$', 'graph_tabs'),
    (r'^VO/.+/.+/.+/$', 'graph_tabs'),
    (r'^VOCluster/.+/.+/.+/$', 'graph_tabs'),
    (r'^VOSE/.+/.+/.+/$', 'graph_tabs'),
    # entity-level and attribute-level
    (r'^(?P<entity_type>\w+)/(?P<uniqueid>[^/]*)/(?P<attribute>[\w-]+)/(?P<start_time>[\w-]+)/$', 'entity_level'),
    # graphs viewing tabs page
    (r'^.+/.+/.+/$', 'graph_tabs'),
)

