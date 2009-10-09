from django.test import TestCase
from django.test.client import Client

class GeoTestCase(TestCase):
    advBrowser = ['Firefox', 'Opera']
    
    def setUp(self):
        self.client = Client()

    def testIndexWithSlashAdvanced(self):
        for browser in self.advBrowser:
            response = self.client.get('/gstat/ldap/',
                    HTTP_USER_AGENT=browser)
            self.failUnlessEqual(response.status_code, 200)

    def testIndexWithoutSlashAdvanced(self):
        for browser in self.advBrowser:
            response = self.client.get('/gstat/ldap',
                    HTTP_USER_AGENT=browser)
            self.failUnlessEqual(response.status_code, 200)

    def testIndexWithSlashBasic(self):
        response = self.client.get('/gstat/ldap/',
                HTTP_USER_AGENT='')
        self.failUnlessEqual(response.status_code, 200)

    def testIndexWithoutSlashBasic(self):
        response = self.client.get('/gstat/ldap',
                HTTP_USER_AGENT='')
        self.failUnlessEqual(response.status_code, 200)

    def testBrowse(self):
        response = self.client.get('/gstat/ldap/browse')
        self.failUnlessEqual(response.status_code, 200)

    def testBrowseWithDN(self):
        response = self.client.get('/gstat/ldap/browse', {
                'dn': 'o=grid'})
        self.failUnlessEqual(response.status_code, 200)

    def testBrowseEntryWithDN(self):
        response = self.client.get('/gstat/ldap/browse', {
                'dn': 'o=grid',
                'entry': 'true'})
        self.failUnlessEqual(response.status_code, 200)