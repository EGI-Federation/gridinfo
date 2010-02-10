from django.conf.urls.defaults import *

urlpatterns = patterns('gridmap.views',
    (r'^$', 'index'),
    (r'^samservices$', 'samservices'),
    (r'^mappings$', 'mappings'),
    (r'^treemap$', 'treemap'),
    (r'^statuslatest$', 'statuslatest'),
)
