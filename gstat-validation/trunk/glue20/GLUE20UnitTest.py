#!/usr/bin/env python

import sys
from GLUE20DataTypes import GLUE20DataTypes
from lib.UnitTest import UnitTest

class GLUE20UnitTest(UnitTest):

  def checkMandatoryAttributes(self, mandatoryAttributes, entry, log):
    uniqueid = entry['dn'][0]
    for attr in mandatoryAttributes:
      if attr in entry:
        log.debug("The mandatory attribute %s is present in %s" % (attr, uniqueid))
      else:
        log.error("The mandatory attribute %s is not present in %s" % (attr, uniqueid))

  def checkSingleValueAttributes(self, singleValueAttributes, entry, log):
    uniqueid = entry['dn'][0]
    for attr in singleValueAttributes:
      if attr in entry:
        if len(entry[attr]) > 1:
          log.error("The single value attribute %s has more than one value in %s" % (attr, uniqueid))
        else:
          log.debug("The single value attribute %s is present in %s" % (attr, uniqueid))

  def checkUniqueID(self, uniqueid, ldif_lower, log):
    keyuniqueid = 'id: ' + uniqueid
    if ldif_lower.count(keyuniqueid) == 0:
      log.error("The id %s was not found: This may be due to a program error" % (uniqueid))
    elif ldif_lower.count(keyuniqueid) > 1:
      log.error("The id %s is not unique" % (uniqueid))
    else:
      log.debug("The id %s was found and it is unique" % (uniqueid))

  def checkRelations(self, relations, entry, ldif_lower, log):
    for key, subject in relations.iteritems():
      if key in entry:
        for value in entry[key]:
          if ldif_lower.count(subject + ': ' + value.lower()) == 0:
            log.error("The FK %s with value %s was not found" % (key, value))
          else:
            log.debug("The FK %s with value %s was found" % (key, value))

  def checkDataTypes(self, dataTypes, entry, log):
    uniqueid = entry['dn'][0]
    inst = GLUE20DataTypes()
    for key, values in entry.iteritems():
      if key == 'dn' or key == 'objectclass' or key.endswith('foreignkey'):
        continue
      elif key in dataTypes:
        for value in values:
          datatype = dataTypes[key]
          check = getattr(inst, 'check' + datatype)
          if not check(value):
            log.error("The field %s with value %s does not follow the type %s in %s" % (key, value, datatype, uniqueid))
      else:
        log.error("The data type %s was not found in the list" % (key))

  def run(self, entry, ldif, ldif_lower, log):
    log.debug("Testing %s" % (entry['dn']))
    if self.uniqueid != '':
      self.checkUniqueID(entry[self.uniqueid][0], ldif_lower, log)
    else:
      log.error('No uniqueid specified for %s' % (entry['dn'][0]))
    if len(self.mandatoryAttributes) > 0:
      self.checkMandatoryAttributes(self.mandatoryAttributes, entry, log)
    else:
      log.debug('No mandatory attributes specified')
    if len(self.singleValueAttributes) > 0:
      self.checkSingleValueAttributes(self.singleValueAttributes, entry, log)
    else:
      log.debug('No single value attributes specified')
    if len(self.relations) > 0:
      self.checkRelations(self.relations, entry, ldif_lower, log)
    else:
      log.debug('No relations specified')
    if len(self.dataTypes) > 0:
      self.checkDataTypes(self.dataTypes, entry, log)
    else:
      log.debug('No data types specified')
