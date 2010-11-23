from django.conf.urls.defaults import *

urlpatterns = patterns('service.views',  
    (r'^(?P<type>.+)/treeview/(?P<uniqueid>.+)/$', 'treeview'),
    (r'^(?P<type>.+)/treeview/$', 'treeview'),  
    (r'^(?P<type_name>.+)/(?P<host_name>.+)/(?P<check_name>.+)/$', 'status'), 
    (r'^(?P<type>\w+)/(?P<output>json)$', 'main'),
    (r'^(?P<output>json)$', 'main'),
    (r'^(?P<type>\w+)/$', 'main'),
    (r'^$', 'main'),
)
