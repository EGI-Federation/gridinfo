from django.conf.urls.defaults import *

urlpatterns = patterns('gridsite.views',
    (r'^(?P<site_name>.+)/topbdii/$', 'topbdii'),
    (r'^(?P<site_name>.+)/topbdii_xml/$', 'topbdii_xml'),
    (r'^(?P<site_name>.+)/topbdii_json/$', 'topbdii_json'),
    (r'^(?P<site_name>.+)/sitebdii/$', 'sitebdii'),
    (r'^(?P<site_name>.+)/ce/$', 'ce'),
    (r'^(?P<site_name>.+)/se/$', 'se'),
    (r'^(?P<site_name>.+)/service/$', 'service'),
    (r'^(?P<site_name>.+)/site/$', 'site'),
    (r'^(?P<site_name>.+)/$', 'overview'),
)
