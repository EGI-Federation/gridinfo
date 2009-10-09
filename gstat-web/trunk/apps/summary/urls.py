from django.conf.urls.defaults import *

urlpatterns = patterns('summary.views',
    (r'^$', 'summary'),
    (r'(?P<type>top)/$', 'bdii_view'),
    (r'(?P<type>site)/$', 'bdii_view'),
    (r'^grid/$', 'grid'),
    (r'^grid/EGEE/$', 'egee'),
    (r'^grid/egee_roc/$', 'egee_roc'),
    (r'^grid/egee_roc/(?P<roc_name>.+)/$', 'egee_roc_specified'),
    (r'^grid/egee_service/(?P<service_name>.+)/$', 'egee_service_specified'),
    (r'^grid/WLCG/$', 'wlcg_tier'),
    (r'^grid/wlcg_tier/(?P<tier_name>.+)/$', 'wlcg_tier_specified'),
    (r'^grid/(?P<grid_name>.+)/$', 'grid_specified'),
    (r'^country/$', 'country'),
    (r'^country/(?P<country_name>.+)/$', 'country_specified'),
)

