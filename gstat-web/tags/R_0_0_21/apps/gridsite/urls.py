from django.conf.urls.defaults import *

urlpatterns = patterns('gridsite.views',
    (r'^(?P<site_name>.+)/treeview/(?P<type>.+)/(?P<attribute>.+)/$', 'treeview'),
    (r'^(?P<site_name>.+)/treeview/(?P<type>.+)/$', 'treeview'),
    (r'^(?P<site_name>.+)/(?P<type_name>.+)/(?P<host_name>.+)/(?P<check_name>.+)/$', 'status'),
    (r'^(?P<site_name>.+)/$', 'overview'),
)
