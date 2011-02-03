#!/usr/bin/python
import glue2.data

def is_DN(value):
   return True

def is_ObjectClass(value):

   if value in glue2.data.schema:
      return True
   else:
      return False
def is_string( value):
   if value == '':
      return False
   else:
      return True

def is_extended_boolean_t( value):
   value = value.lower()
   if value in ['false', 'true', 'undefined']:
      return True
   else:
      return False
   
def is_URI( value):
   # RFC 3986: http://www.ietf.org/rfc/rfc3986.txt
   # Check URL (subtype of URI)
   uri = "^[a-zA-Z][a-zA-Z0-9+-.]*://[a-zA-Z0-9_.]+(:[0-9]+)*(/[a-zA-Z0-9_]*)*(\?[a-zA-Z0-9+-:@?./]+)?(#[a-zA-Z0-9+-:#@?./]+)?$"
   if re.match(uri, value):
      return True
   else:
      # Check other URIs
      uri = "^[a-zA-Z][a-zA-Z0-9+-.@:]*:[a-zA-Z0-9+-.@:]*$"
      if re.match(uri, value):
         return True
      else:
         return False

def is_url( value):
   # RFC 1738: http://www.ietf.org/rfc/rfc1738.txt
   # Protocols accepted: http|ftp|https|ftps|sftp
   # Protocols rejected on purpose: gopher|news|nntp|telnet|mailto|file|etc.
   url = "(((http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&amp;%_\./-~-]*)?"
   if re.match(url, value):
      return 1
   else:
      return 0
   
def is_real_32( value):
   # IEE 754-2008: http://en.wikipedia.org/wiki/IEEE_754-2008
   # I just check it is a floating point number
   floatingpoint = "[0-9]+(.[0-9]+)*"
   if re.match(floatingpoint, value):
      return True
   else:
      return False

def is_contact_type( value):
   value = value.lower()
   if value in ['general', 'security', 'sysadmin', 'usersupport']:
      return True
   else:
      return False

def is_u_int_64( value):
   # Check http://en.wikipedia.org/wiki/Integer_(computer_science)
   if re.match("^[0-9]+$", value):
      if long(value) <= 18446744073709551615L:
         return True
      return False

def is_datetime_t( value):
   # Check http://www.w3.org/TR/xmlschema-2/#dateTime
   dateTime = "^-?[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])T([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z?$"
   if re.match(dateTime, value):
      return True
   return False

def is_email( email):
   if len(email) > 7:
      if re.match("mailto:[ ]*.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
         return True
   return False

if __name__ == '__main__':
   pass
