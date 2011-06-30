#!/usr/bin/env python

import unittest
import re
import sys
sys.path.append('..')
from GLUE20DataTypes import GLUE20DataTypes

class GLUE20DataTypesTest(unittest.TestCase):

  def setUp(self):
    self.obj = GLUE20DataTypes()

  def testCheckString(self):
    self.assertTrue(self.obj.checkString('foobar'))
    self.assertFalse(self.obj.checkString(''))

  def testCheckExtendedBoolean_t(self):
    self.assertTrue(self.obj.checkExtendedBoolean_t('true'))
    self.assertTrue(self.obj.checkExtendedBoolean_t('false'))
    self.assertTrue(self.obj.checkExtendedBoolean_t('undefined'))
    self.assertFalse(self.obj.checkExtendedBoolean_t('foobar'))
    self.assertFalse(self.obj.checkExtendedBoolean_t('1'))
    self.assertFalse(self.obj.checkExtendedBoolean_t(''))

  def testCheckURI(self):
    self.assertTrue(self.obj.checkURI('urn:example:animal:ferret:nose'))
    self.assertTrue(self.obj.checkURI('foo://example.com:8042/over/there'))
    self.assertTrue(self.obj.checkURI('foo://example.com/over/there'))
    self.assertTrue(self.obj.checkURI('foo://example.com/over/there/'))
    self.assertTrue(self.obj.checkURI('foo://192.168.0.1/over/there'))
    self.assertTrue(self.obj.checkURI('foo://192.168.0.1'))
    self.assertTrue(self.obj.checkURI('foo://192.168.0.1/'))
    self.assertTrue(self.obj.checkURI('foo://example.com'))
    self.assertTrue(self.obj.checkURI('foo://example.com/'))
    self.assertTrue(self.obj.checkURI('foo://example.com:8042/over/there?test'))
    self.assertTrue(self.obj.checkURI('foo://example.com:8042/over/there?test#test'))
    self.assertTrue(self.obj.checkURI('foo://example.com:8042/over/there?test?test#test'))
    self.assertTrue(self.obj.checkURI('foo://example.com:8042/over/there?test?test#test?test'))
    self.assertTrue(self.obj.checkURI('foo://example.com:8042/over/there?test?test#test?test#test'))
    self.assertTrue(self.obj.checkURI('mailto:david@cern.ch'))
    self.assertFalse(self.obj.checkURI('foo'))
    self.assertFalse(self.obj.checkURI('foo:/bar'))

  def testCheckURL(self):
    self.assertTrue(self.obj.checkURL('http://example.com:8042/over/there'))
    self.assertTrue(self.obj.checkURL('ftp://example.com:8042/over/there'))
    self.assertTrue(self.obj.checkURL('https://example.com:8042/over/there'))
    self.assertTrue(self.obj.checkURL('ftps://example.com:8042/over/there'))
    self.assertTrue(self.obj.checkURL('sftp://example.com:8042/over/there'))
    self.assertTrue(self.obj.checkURL('http://example.com/over/there'))
    self.assertTrue(self.obj.checkURL('http://example.com/over/there/'))
    self.assertTrue(self.obj.checkURL('http://192.168.0.1/over/there'))
    self.assertTrue(self.obj.checkURL('http://192.168.0.1'))
    self.assertTrue(self.obj.checkURL('http://192.168.0.1/'))
    self.assertTrue(self.obj.checkURL('http://example.com'))
    self.assertTrue(self.obj.checkURL('http://example.com/'))
    self.assertTrue(self.obj.checkURL('http://example.com:8042/over/there?test'))
    self.assertTrue(self.obj.checkURL('http://example.com:8042/over/there?test#test'))
    self.assertTrue(self.obj.checkURL('http://example.com:8042/over/there?test?test#test'))
    self.assertTrue(self.obj.checkURL('http://example.com:8042/over/there?test?test#test?test'))
    self.assertTrue(self.obj.checkURL('http://example.com:8042/over/there?test?test#test?test#test'))
    self.assertTrue(self.obj.checkURL('ftp://example.com/over/there'))
    self.assertFalse(self.obj.checkURL('mailto:david@cern.ch'))
    self.assertFalse(self.obj.checkURL('gopher://example.com/over/there'))
    self.assertFalse(self.obj.checkURL('news://example.com'))
    self.assertFalse(self.obj.checkURL('nntp://example.com'))
    self.assertFalse(self.obj.checkURL('telnet://example.com'))
    self.assertFalse(self.obj.checkURL('file://example.com/over/there'))
    self.assertFalse(self.obj.checkURL('foo://example.com:8042/over/there'))
    self.assertFalse(self.obj.checkURL('foo'))
    self.assertFalse(self.obj.checkURL('foo:/bar'))
    self.assertFalse(self.obj.checkURL('urn:example:animal:ferret:nose'))

  def testCheckReal32(self):
    self.assertTrue(self.obj.checkReal32('3'))
    self.assertTrue(self.obj.checkReal32('3333333'))
    self.assertTrue(self.obj.checkReal32('3.4'))
    self.assertTrue(self.obj.checkReal32('33333223.1222323234'))
    self.assertTrue(self.obj.checkReal32('3.'))
    self.assertFalse(self.obj.checkReal32('aaaa'))
    self.assertFalse(self.obj.checkReal32('-'))
    self.assertFalse(self.obj.checkReal32('NULL'))

  def testCheckContactType(self):
    self.assertTrue(self.obj.checkContactType('general'))
    self.assertTrue(self.obj.checkContactType('security'))
    self.assertTrue(self.obj.checkContactType('sysadmin'))
    self.assertTrue(self.obj.checkContactType('usersupport'))
    self.assertFalse(self.obj.checkContactType('foobar'))
    self.assertFalse(self.obj.checkContactType('1'))

  def testCheckUInt64(self):
    self.assertTrue(self.obj.checkUInt64('0'))
    self.assertTrue(self.obj.checkUInt64('1'))
    self.assertTrue(self.obj.checkUInt64('999'))
    self.assertTrue(self.obj.checkUInt64('18446744073709551615'))
    self.assertFalse(self.obj.checkUInt64('-1'))
    self.assertFalse(self.obj.checkUInt64('1.1'))
    self.assertFalse(self.obj.checkUInt64('18446744073709551616'))

  def testCheckDateTime_t(self):
    self.assertTrue(self.obj.checkDateTime_t('2009-10-10T11:05:30'))
    self.assertTrue(self.obj.checkDateTime_t('-2009-10-10T11:05:30'))
    self.assertTrue(self.obj.checkDateTime_t('2009-10-10T11:05:30Z'))
    self.assertTrue(self.obj.checkDateTime_t('-2009-10-10T11:05:30Z'))
    self.assertTrue(self.obj.checkDateTime_t('9999-12-31T23:59:59'))
    self.assertTrue(self.obj.checkDateTime_t('0000-01-01T00:00:00'))
    self.assertFalse(self.obj.checkDateTime_t('2009-13-10T11:05:30'))
    self.assertFalse(self.obj.checkDateTime_t('2009-12-32T11:05:30'))
    self.assertFalse(self.obj.checkDateTime_t('2009-12-10T24:05:30'))
    self.assertFalse(self.obj.checkDateTime_t('2009-12-10T11:60:30'))
    self.assertFalse(self.obj.checkDateTime_t('2009-12-10T11:05:60'))
    self.assertFalse(self.obj.checkDateTime_t('2009-12-10T11:05:60Z01:00:00'))

if __name__ == '__main__':
  unittest.main()
