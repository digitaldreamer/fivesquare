import requests

from service import logger

GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


class GoogleMaps(object):
    """
    Light Google Maps API Wrapper
    """
    API_KEY = ''

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def geocode(self, address):
        """
        Geocodes an address into latitude and longitude coordinates
        from the google maps api

        https://developers.google.com/maps/documentation/geocoding/intro
        """
        params = {
            'address': address,
            'key': self.API_KEY,
        }
        location = {
            'lat': 0,
            'lng': 0,
        },

        requests.packages.urllib3.disable_warnings()
        response = requests.get(GOOGLE_MAPS_URL, params=params, verify=False)
        response_json = response.json()

        if response_json.get('status') == 'OK':
            logger.debug('GeoCoded address:{}'.format(address))
            position = response_json['results'][0]['geometry']['location']
            location = {
                'lat': position['lat'],
                'lng': position['lng'],
            }
        else:
            logger.debug('Failed to GeoCode address:{}'.format(address))

        return location


if __name__ == '__main__':
    GOOGLE_MAPS_API_KEY = 'AIzaSyC_dZ5OqZJ0rosdfUKmGs_Nwf_f1bM8bK0'
    google_maps = GoogleMaps(GOOGLE_MAPS_API_KEY)
    location = google_maps.geocode('Central Park, New York, NY')
    print location
