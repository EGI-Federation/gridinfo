from django.conf.urls.defaults import *

urlpatterns = patterns('bdii.views',
                       (r'^$', 'main'),
                       url(r'json$', 'main', kwargs={'output': 'json'} ),
                       url(r'^top/$', 'main', kwargs={'type' : 'top'}),
                       url(r'top/json$', 'main', kwargs={'output': 'json', 'type' : 'top'} ),
                       url(r'^site/$', 'main', kwargs={'type' : 'site'}),
                       url(r'^site/json', 'main', kwargs={'output': 'json', 'type' : 'site'}),
)

