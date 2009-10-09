from django.conf.urls.defaults import *

urlpatterns = patterns('service.views',   
    (r'^(bdii_top)$', 'bdii'),
    (r'^(bdii_site)$', 'bdii'),
)
