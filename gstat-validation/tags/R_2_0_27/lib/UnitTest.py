#!/usr/bin/env python

import testingutils
import logging
import sys

class UnitTest:

  def error_messages(self): abstract

  def run(self, entry, ldif, ldif_lower, log): abstract

  def main(self, modelName):
    config = testingutils.parse_options()
    log = logging.getLogger(self.__class__.__name__)
    hdlr = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(config['debug'])
    #my_errors = testingutils.error_logger(self.__class__.__name__, self.error_messages())

    if config.has_key('file'):
      source = "file://%s" % (config['file'])
    if config.has_key('host'):
      source = "ldap://%s:%s/%s?filter=%s" % (config['host'], config['port'], config['bind'], filter)

    ldif = testingutils.fast_read_ldif(source)
    ldif_lower = ldif.lower()
    dns_dict = testingutils.get_dns(ldif)
    count = 0
    for dn in dns_dict:
      entry = ldif[dns_dict[dn][0]:dns_dict[dn][1]].strip()
      entry = testingutils.convert_entry(entry)
      for object_class in entry['objectclass']:
        if ( object_class.lower() == modelName ):
          self.run(entry, ldif, ldif_lower, log)
