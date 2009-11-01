#!/usr/bin/env python
import os
from distutils.core import setup

def get_files(directory, install_base):
    file_list = []
    files=os.listdir(directory)
    found_files = []
    for file in files:
        if ( os.path.isdir(directory + "/" + file) ):
            if ( not file == ".svn"):
                file_list += get_files(directory + "/" + file, install_base)
        else:
            found_files.append(directory + "/" + file)
            
    if ( len(found_files) > 0 ):
        file_list.append((install_base + "/" + directory, found_files))
    return file_list

media_files = get_files("media", "share/gstat")

setup(name='gstat-web',
      version='0.0.18',
      py_modules=['gsutils'],
      package_dir = {'': 'apps'},
      scripts =['tools/configure-nagios',
                'tools/gstat-update',
                'tools/gstat-update-rrd',
                'tools/import-entities',
                'tools/import-prod-bdii',
                'tools/snapshot'],
      data_files = [
        ('/etc/gstat', ['config/gstat.ini']),
        ('', ['LICENSE']),
        ('/etc/nagios/gstat', ['config/bdii-commands.cfg','config/bdii-services.cfg']),
        ('/etc/httpd/conf.d', ['apache/gstat.conf']),
        ('/etc/cron.d', ['config/gstat-update', 'config/configure-nagios']),
        ('/usr/share/gstat/', ['apache/gstat.wsgi','apps/manage.py']),
     ] + media_files,
      packages=['bdii',
                'core',
                'geo',
                'glue',
                'gridsite',
                'ldapbrowser',
                'newserializers',
                'newserializers/formatters',
                'rrd',
                'service',
                'stats',
                'summary',
                'topology'],
      package_data={'core': ['templates/*.html'], 
                    'geo': ['templates/*.html'],
                    'gridsite': ['templates/*.html'],
                    'ldapbrowser': ['templates/*.html'],
                    'rrd': ['templates/*.html'],
                    'stats': ['templates/*.html'],
                    'summary': ['templates/*.html']},
)
