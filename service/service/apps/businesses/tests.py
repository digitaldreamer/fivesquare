import os
import unittest
import urllib

from pyramid import testing

from auth.models import User
from businesses.models import Business
from reviews.models import Review


class BusinessModel(unittest.TestCase):
    def setUp(self):
        from paste.deploy import appconfig

        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
        self.config = testing.setUp(settings=self.settings)
        self.created_ids = []

    def tearDown(self):
        self.reset()
        testing.tearDown()

    def test_business(self):
        address = {
            'street1': 'Central Park',
            'city': 'New York',
            'state': 'NY'
        }
        business = self.create_business('Central Park', address)
        self.assertTrue(business)
        self.created_ids.append(business.id)

        self.assertTrue(business.address_string)
        self.assertTrue(business.location[0] and business.location[1])

    def create_business(self, name, address):
        # check business
        business = Business.create(name, address)
        self.created_ids.append(business.id)
        self.assertTrue(business)

        return business

    def reset(self):
        """
        clean up any remaining test users
        """
        for business_id in self.created_ids:
            business = Business.get_by_id(business_id)

            if business:
                business.delete()


class BusinessAPI(unittest.TestCase):
    def setUp(self):
        from service import main
        from paste.deploy import appconfig
        from webtest import TestApp

        # set settings
        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
        app = main({}, **self.settings)
        self.testapp = TestApp(app)
        self.config = testing.setUp(settings=self.settings)

        self.created_ids = []

        # init user
        self.user = User.create('hello@example.com', 'hello')
        payload = {
            'email': 'hello@example.com',
            'password': 'hello',
        }
        response = self.testapp.post_json('/api/v1/authenticate', payload, status=200)
        self.access_token = response.json['access_token']

    def tearDown(self):
        self.reset()
        testing.tearDown()

    def test_pagination(self):
        """
        this requires the base businesses are loaded through load_db
        """
        endpoint = '/api/v1/businesses'
        params = {
            'limit': 2,
            'offset': 0
        }
        response = self.testapp.get(endpoint, params)
        json1 = response.json

        params = {
            'limit': 2,
            'offset': 1
        }
        response = self.testapp.get(endpoint, params)
        json2 = response.json

        self.assertTrue(len(json1['businesses']) == 2)
        self.assertTrue(len(json2['businesses']) == 2)
        self.assertTrue(json1['businesses'][1]['id'] == json2['businesses'][0]['id'])

    def test_location(self):
        params = {
            'lat': 40.746167,
            'lng': -73.988395,
            'distance': .8,
        }
        endpoint = '/api/v1/businesses'
        response = self.testapp.get(endpoint, params)

        names = []

        for business in response.json['businesses']:
            names.append(business['name'])

        self.assertTrue('1200' in names)
        self.assertTrue('1500' in names)
        self.assertFalse('1800' in names)
        self.assertFalse('2000' in names)

    def test_create_and_get_business(self):
        # create business
        params = {
            'access_token': self.access_token,
        }
        payload = {
            'name': 'Test Location',
            'street1': 'Central Park',
            'city': 'New York',
            'state': 'NY',
        }

        endpoint = '/api/v1/businesses'
        response = self.testapp.post_json(endpoint, payload, status=401)

        endpoint = '/api/v1/businesses?' + urllib.urlencode(params)
        response = self.testapp.post_json(endpoint, {}, status=400)
        response = self.testapp.post_json(endpoint, payload, status=200)

        self.assertTrue(response.json['id'])
        self.created_ids.append(response.json['id'])
        _id = response.json['id']

        # get business
        endpoint = '/api/v1/businesses/{}'.format('404')
        response = self.testapp.get(endpoint, status=404)

        endpoint = '/api/v1/businesses/{}'.format(_id)
        response = self.testapp.get(endpoint, status=200)
        self.assertTrue(response.json.get('id', '') == _id)

    def reset(self):
        self.user.delete()

        for _id in self.created_ids:
            business = Business.get_by_id(_id)
            business.delete()


class BusinessReviewsAPI(unittest.TestCase):
    def setUp(self):
        from service import main
        from paste.deploy import appconfig
        from webtest import TestApp

        # set settings
        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
        app = main({}, **self.settings)
        self.testapp = TestApp(app)
        self.config = testing.setUp(settings=self.settings)

        self.created_ids = []

        # init user
        self.user = User.create('hello@example.com', 'hello')
        payload = {
            'email': 'hello@example.com',
            'password': 'hello',
        }
        response = self.testapp.post_json('/api/v1/authenticate', payload, status=200)
        self.access_token = response.json['access_token']

        # init business
        address = {
            'street1': 'Central Park',
            'city': 'New York',
            'state': 'NY',
        }
        self.business = Business.create('Test Location', address)

    def tearDown(self):
        self.reset()
        testing.tearDown()

    def refresh_business(self):
        """
        loads and updates the business with the database
        """
        self.business = Business.get_by_id(self.business.id)

    def test_create_and_get_reviews(self):
        # create reviews
        params = {
            'access_token': self.access_token,
        }
        payload = {
            'rating': 1,
            'text': 'a bad review',
            'tags': 'hello:world',
        }

        endpoint = '/api/v1/businesses/{}/reviews'.format(self.business.id)
        response = self.testapp.post_json(endpoint, payload, status=401)

        endpoint = '/api/v1/businesses/{}/reviews?'.format(self.business.id) + urllib.urlencode(params)
        response = self.testapp.post_json(endpoint, {}, status=400)
        response = self.testapp.post_json(endpoint, payload, status=200)

        self.assertTrue(response.json['id'])
        self.created_ids.append(response.json['id'])

        # another review
        payload = {
            'rating': 1,
            'text': 'another bad review',
        }
        response = self.testapp.post_json(endpoint, payload, status=200)
        self.assertTrue(response.json['id'])
        self.created_ids.append(response.json['id'])

        # another review
        payload = {
            'rating': 5,
            'text': 'a good review',
            'tags': 'something',
        }
        response = self.testapp.post_json(endpoint, payload, status=200)
        self.assertTrue(response.json['id'])
        self.created_ids.append(response.json['id'])

        payload = {
            'rating': 5,
            'text': 'another good review',
        }
        response = self.testapp.post_json(endpoint, payload, status=200)
        self.assertTrue(response.json['id'])
        self.created_ids.append(response.json['id'])

        _id = response.json['id']

        # get reviews
        endpoint = '/api/v1/businesses/{}/reviews'.format(self.business.id)
        response = self.testapp.get(endpoint, status=200)
        self.assertTrue(len(response.json['reviews']) == 4)

        # get review
        endpoint = '/api/v1/businesses/{}/reviews/{}'.format(self.business.id, '404')
        response = self.testapp.get(endpoint, status=404)

        endpoint = '/api/v1/businesses/{}/reviews/{}'.format(self.business.id, _id)
        response = self.testapp.get(endpoint, status=200)
        self.assertTrue(response.json.get('id', '') == _id)

        # check business
        self.refresh_business()
        self.assertTrue(self.business.rating == 3)
        self.assertTrue('hello' in self.business.tags)
        self.assertTrue('world' in self.business.tags)
        self.assertTrue('something' in self.business.tags)

    def reset(self):
        for _id in self.created_ids:
            review = Review.get_by_id(_id)
            review.delete()

        self.user.delete()
        self.business.delete()
