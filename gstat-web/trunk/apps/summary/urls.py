from django.conf.urls.defaults import *

urlpatterns = patterns('summary.views',
    (r'^(?P<type>\w+)/(?P<value>[A-Za-z0-9- :/."_=]+)/json/$', 'get_json'),
    (r'^(?P<type>\w+)/json/$', 'get_json'),
    (r'^(?P<type>\w+)/(?P<value>[A-Za-z0-9- :/."_=]+)/$', 'main'),
    (r'^json/$', 'get_public_json'),
    (r'^(?P<type>\w+)/$', 'main'),
    (r'^$', 'main'),
)
