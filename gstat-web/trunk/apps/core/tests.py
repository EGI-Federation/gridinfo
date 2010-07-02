from django.test import TestCase
from django.test.client import Client

class CoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def testIndex(self):
        response = self.client.get('/')
        self.assertRedirects(response,
                           '/gstat/geo/openlayers',
                           status_code = 302,
                           target_status_code = 200)

    def testFilter(self):
        response = self.client.get('/gstat/core/filter')
        self.failUnlessEqual(response.status_code, 200)

    def testFilter(self):
        response = self.client.get('/gstat/core/filter/GRID')
        self.failUnlessEqual(response.status_code, 200)

    def testFilter(self):
        response = self.client.get('/gstat/core/filter/EGEE_ROC')
        self.failUnlessEqual(response.status_code, 200)
        
    def testFilter(self):
        response = self.client.get('/gstat/core/filter/EGI_NGI')
        self.failUnlessEqual(response.status_code, 200)

    def testFilter(self):
        response = self.client.get('/gstat/core/filter/WLCG_TIER')
        self.failUnlessEqual(response.status_code, 200)

    def testFilter(self):
        response = self.client.get('/gstat/core/filter/Country')
        self.failUnlessEqual(response.status_code, 200)