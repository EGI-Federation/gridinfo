from django.conf.urls.defaults import *

urlpatterns = patterns('service.views',   
                       (r'^(?P<type>\w+)/$', 'main'),
                       (r'^(?P<type>\w+)/(?P<output>json)$', 'main'),
                       (r'^(?P<type>\w+)/(?P<uniqueid>.+)$', 'service'),
)
