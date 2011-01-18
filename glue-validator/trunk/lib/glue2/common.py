import glue2.common
import re

def verify_mandatory_attributes(attributes, entry, log):
    unique_id = entry['dn'][0]
    for attribute in attributes:
        if attribute not in entry:
            log.error("The mandatory attribute %s is not present in %s" % (attribute, unique_id))

def verify_single_valued(attributes, entry, log):
    unique_id = entry['dn'][0]
    for attribute in attributes:
        if attribute in entry:
            if len(entry[attribute]) > 1:
                log.error("The single value attribute %s has more than one value in %s" % (attribute, uniqueid))

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

def verify_data_types(DATA_TYPES, entry, log):
    unique_id = entry['dn'][0]
    for attribute in entry:
        if attribute == 'dn' or attribute == 'objectClass' or attribute.endswith('ForeignKey'):
            continue
        if attribute not in DATA_TYPES:
            log.error("The data type for attribute %s could not be found." % (attribute))
            continue
        for value in entry[attribute]:
            data_type = DATA_TYPES[attribute]
            check = getattr(glue2.common, 'verify_' + data_type)
            if not check(value):
                log.error("The field %s with value %s does not follow the type %s in %s" % (attribute, value, data_type, unique_id))

def verify_string(value):
    if value == '':
        return 0
    else:
        return 1

def verify_extended_boolean_t(value):
    value = value.lower()
    if value in ['false', 'true', 'undefined']:
        return 1
    else:
        return 0

def verify_uri(value):
    # RFC 3986: http://www.ietf.org/rfc/rfc3986.txt
    # Check URL (subtype of URI)
    uri = "^[a-zA-Z][a-zA-Z0-9+-.]*://[a-zA-Z0-9_.]+(:[0-9]+)*(/[a-zA-Z0-9_]*)*(\?[a-zA-Z0-9+-:@?./]+)?(#[a-zA-Z0-9+-:#@?./]+)?$"
    if re.match(uri, value):
        return 1
    else:
        # Check other URIs
        uri = "^[a-zA-Z][a-zA-Z0-9+-.@:]*:[a-zA-Z0-9+-.@:]*$"
        if re.match(uri, value):
            return 1
        else:
            return 0

def verify_url(value):
     # RFC 1738: http://www.ietf.org/rfc/rfc1738.txt
     # Protocols accepted: http|ftp|https|ftps|sftp
     # Protocols rejected on purpose: gopher|news|nntp|telnet|mailto|file|etc.
     url = "(((http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&amp;%_\./-~-]*)?"
     if re.match(url, value):
         return 1
     else:
         return 0

def verify_Real32(self, value):
    # IEE 754-2008: http://en.wikipedia.org/wiki/IEEE_754-2008
    # I just check it is a floating point number
    floatingpoint = "[0-9]+(.[0-9]+)*"
    if re.match(floatingpoint, value):
        return 1
    else:
        return 0

def verify_contact_type(self, value):
    value = value.lower()
    if value in ['general', 'security', 'sysadmin', 'usersupport']:
      return 1
    else:
      return 0

def verify_UInt64(self, value):
    # Check http://en.wikipedia.org/wiki/Integer_(computer_science)
    if re.match("^[0-9]+$", value):
      if long(value) <= 18446744073709551615L:
        return 1
    return 0

def verify_datetime_t(self, value):
    # Check http://www.w3.org/TR/xmlschema-2/#dateTime
    dateTime = "^-?[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])T([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z?$"
    if re.match(dateTime, value):
      return 1
    return 0

def verify_Email(self, email):
    if len(email) > 7:
      if re.match("mailto:[ ]*.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
        return 1
    return 0
