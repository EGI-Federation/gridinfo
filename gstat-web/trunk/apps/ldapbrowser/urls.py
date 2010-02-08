from django.conf.urls.defaults import *

urlpatterns = patterns('ldapbrowser.views',
    (r'^$', 'index'),
    (r'^browse', 'browse'),
    (r'^site/(?P<url>[A-Za-z0-9- :/."_=]+)$', 'index'),
    (r'^server/(?P<ldapurl>[A-Za-z0-9- :/."_=,]+)$', 'index'),
)
