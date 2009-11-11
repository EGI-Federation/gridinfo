from django.test import TestCase
from django.test.client import Client

class GeoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def testIndexWithSlash(self):
        response = self.client.get('/gstat/geo/')
        self.assertRedirects(response,
                           '/gstat/geo/openlayers',
                           status_code = 301,
                           target_status_code = 200)

    def testIndexWithoutSlash(self):
        response = self.client.get('/gstat/geo')
        self.assertRedirects(response,
                           '/gstat/geo/openlayers',
                           status_code = 301,
                           target_status_code = 200)

    def testOpenLayers(self):
        response = self.client.get('/gstat/geo/openlayers')
        self.failUnlessEqual(response.status_code, 200)

    def testKml(self):
        response = self.client.get('/gstat/geo/kml')
        self.failUnlessEqual(response.status_code, 200)
