from django.conf.urls.defaults import *

urlpatterns = patterns('bdii.views',
                       (r'^$', 'main'),
                       (r'^(?P<output>json)$', 'main'),
                       (r'^(?P<type>\w+)/$', 'main'),
                       (r'^(?P<type>\w+)/(?P<output>json)$', 'main'),

)

