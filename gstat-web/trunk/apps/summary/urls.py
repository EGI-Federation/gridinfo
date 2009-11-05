from django.conf.urls.defaults import *

urlpatterns = patterns('summary.views',
    (r'^(?P<type>\w+)/(?P<value>[A-Za-z0-9- :/."_=]+)/json/$', 'main', {'output': 'json'}),
    (r'^(?P<type>\w+)/json/$', 'main', {'output': 'json'}),
    (r'^(?P<type>\w+)/(?P<value>[A-Za-z0-9- :/."_=]+)/$', 'main'),
    (r'^json/$', 'main', {'output': 'json'}),
    (r'^(?P<type>\w+)/$', 'main'),
    (r'^$', 'main'),
)
