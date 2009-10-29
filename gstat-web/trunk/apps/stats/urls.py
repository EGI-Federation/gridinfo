from django.conf.urls.defaults import *

urlpatterns = patterns('stats.views',
    (r'^$', 'main'),
    (r'^(?P<type>\w+)/$', 'main'),
    (r'^(?P<type>\w+)/(?P<value>\w+)/$', 'main'),
)

