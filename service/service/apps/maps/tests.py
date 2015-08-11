import os
import unittest

from pyramid import testing

from service.apps.maps.maps import GoogleMaps


class Maps(unittest.TestCase):
    def setUp(self):
        from paste.deploy import appconfig

        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
        self.config = testing.setUp(settings=self.settings)

    def tearDown(self):
        testing.tearDown()

    def test_geocode(self):
        """
        test geocoding a location
        """
        from service.settings import config

        google_maps = GoogleMaps(config['google_maps.api_key'])
        location = google_maps.geocode('Central Park, New York, NY')

        self.assertTrue(location['lat'])
        self.assertTrue(location['lng'])
