#wsgi_handler.py

import sys
import os

sys.path.append('/var/www/django-sites/gstat/lib/python2.5/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
