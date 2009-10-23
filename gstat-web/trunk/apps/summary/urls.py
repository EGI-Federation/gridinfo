from django.conf.urls.defaults import *

urlpatterns = patterns('summary.views',
    (r'^$', 'main'),
    url(r'^json$', 'main', kwargs={'output': 'json'}),
    (r'^(?P<type>\w+)/$', 'main'),
    url(r'^(?P<type>\w+)/json$', 'main',kwargs={'output': 'json'} ),
    (r'^(?P<type>\w+)/(?P<value>\w+)/$', 'main'),
    url(r'^(?P<type>\w+)/(?P<value>\w+)/json', 'main', kwargs={'output': 'json'}),
)

