from django.conf.urls.defaults import *
from django.views.generic.list_detail import *

urlpatterns = patterns('',
    url(r'^json/(.*)','glue.views.json'),
)
