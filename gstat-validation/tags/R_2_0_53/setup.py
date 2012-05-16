#!/usr/bin/env python

from distutils.core import setup

setup(name='gstat-validation',
      version='2.0.53',
      description='Gstat Valiation Scripts',
      long_description ='Valiation scripts for an LDAP based information system using the Glue 1.2 schema',
      author='Jingya You',
      author_email='jingya.you@cern.ch',
      license='EGEE',
      url='http://goc.grid.sinica.edu.tw/gocwiki/GSIndex',
      scripts = ['bin/gstat-validate-ce', 'bin/gstat-validate-sanity-check', 'bin/gstat-validate-site', 'bin/gstat-validate-se', 'bin/gstat-validate-service'],
      py_modules=['gsutils'],
      package_dir = {'': 'src'},
      data_files = [
        ('/var/lib/gstat/', ['data/locations', 'data/wlcg-tier', 'data/service-types', 'data/NGI.xml']),
        ],
      )