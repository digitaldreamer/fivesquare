import pymongo

from main.models import MongoObject
from pymongo import GEO2D

from service import logger
from storage.mongo import mongodb
from maps.maps import GoogleMaps

mongodb.businesses.ensure_index([("location", GEO2D)])


class Business(MongoObject):
    collection = 'businesses'

    def __init__(self, name='', address={}, mongo=None):
        """
        address = {
            'street1': '',
            'street2': '',
            'city': '',
            'state': '',
            'postal_code': '',
        }

        location: [<longitude>, <latitude>]
        """
        super(Business, self).__init__(mongo=mongo)

        if not mongo:
            self.data.update({
                'address': {
                    'street1': '',
                    'street2': '',
                    'city': '',
                    'state': '',
                    'postal_code': '',
                },
                'location': [0, 0],
                'rating': 0,
                'tags': [],
            })

        if name:
            self.name = name
        if address:
            self.address = address

    @property
    def location(self):
        return self.data.get('location', [0, 0])

    @property
    def name(self):
        return self.data.get('name', '')

    @name.setter
    def name(self, name):
        self.data['name'] = name

    @property
    def rating(self):
        return self.data.get('rating', 0)

    @rating.setter
    def rating(self, rating):
        self.data['rating'] = rating

    @property
    def tags(self):
        return self.data.get('tags', [])

    @tags.setter
    def tags(self, tags):
        self.data['tags'] = tags

    @property
    def address(self):
        return self.data.get('address', {})

    @address.setter
    def address(self, address_fields):
        from settings import config

        google_maps = GoogleMaps(config['google_maps.api_key'])

        # set a new address dict and save it to data
        address = {
            'street1': '',
            'street2': '',
            'city': '',
            'state': '',
            'postal_code': '',
        }
        address.update(address_fields)
        self.data['address'] = address

        # geocode the address
        maps_location = google_maps.geocode(self.address_string)
        self.data['location'] = [maps_location['lng'], maps_location['lat']]

    @property
    def address_string(self):
        """
        return the address in one string
        """
        return '{street1} {street2}, {city}, {state}, {postal_code}'.format(**self.data['address'])

    def toJSON(self):
        """
        returns a cleaned jsonable object
        """
        data = super(Business, self).toJSON()
        return data

    @classmethod
    def businesses(cls, location=[], distance=1, units='imperial', offset=0, limit=100):
        """
        Return the businesses

        parameters
        ==========

        * location - [<longitude>, <latitude>]
        * distance - in miles or km depending on units
        * units - metric|imperial
        * offset - the skipped elements in the returned list
        * limit - the returned max number


        returns
        =======

        [business, ...]
        """
        businesses = []

        if location and distance:
            # restrict to location by distance
            if units == 'metric':
                radius = 6371  # kilometers
            else:
                # default to imperial
                radius = 3959  # miles

            max_distance = distance / radius
            mongo_businesses = mongodb[cls.collection].find({'location': {'$nearSphere': location, '$maxDistance': max_distance}}).limit(limit).skip(offset)
        else:
            # search businesses normally
            mongo_businesses = mongodb[cls.collection].find().sort('created', pymongo.ASCENDING).limit(limit).skip(offset)

        # convert mongo objects to business objects
        for mongo_business in mongo_businesses:
            business = cls(mongo=mongo_business)
            businesses.append(business)

        return businesses

    @classmethod
    def create(cls, name, address):
        """
        creates, saves, and returns a new business
        """
        business = cls(name, address)
        business.save()
        return business
