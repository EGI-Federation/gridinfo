from django.conf.urls.defaults import *

urlpatterns = patterns('vo.views',
    (r'^(?P<vo_name>.+)/(?P<type>\w+)/json/$', 'get_json'),
    (r'^(?P<vo_name>.+)/overview/$', 'overview'),
    (r'^(?P<vo_name>.+)/$', 'treeview'),
    (r'^$', 'treeview'),
)
