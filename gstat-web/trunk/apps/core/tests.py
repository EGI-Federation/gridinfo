from django.test import TestCase
from django.test.client import Client

class GeoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def testIndex(self):
        response = self.client.get('/')
        self.assertRedirects(response,
                             '/gstat/geo/openlayers',
                             status_code=302,
                             target_status_code=200)