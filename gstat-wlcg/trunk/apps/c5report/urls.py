from django.conf.urls.defaults import *

urlpatterns = patterns('c5report.views',
    (r'^$', 'index'),
    (r'^view/text$', 'viewText'),
    (r'^view/xml$', 'viewXml'),
)
