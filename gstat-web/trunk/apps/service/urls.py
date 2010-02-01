from django.conf.urls.defaults import *

urlpatterns = patterns('service.views',   
                       (r'^(?P<type>\w+)/$', 'main'),
                       (r'^(?P<type>\w+)/(?P<output>json)$', 'main'),
                       (r'^(?P<type_name>.+)/(?P<host_name>.+)/(?P<check_name>.+)/$', 'status'),
                       (r'^(?P<type>.+)/(?P<uniqueid>.+)/$', 'treeview'),  
)
