import os
import unittest

from pyramid import testing
from businesses.models import Business


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
        business = self.create_business()
        # self.email(user)
        # self.password(user)
        # self.authentication(user)
        # self.assertTrue(user.delete())

    def create_business(self):
        # check business
        address = {
            'street1': 'Central Park',
            'city': 'New York',
            'state': 'NY'
        }
        business = Business.create('Central Park', address)
        self.created_ids.append(business.id)
        self.assertTrue(business)

        return business

    def email(self, user):
        """
        check updating and email retrieval
        """
        self.assertEqual(user.email, 'hello@example.com')
        self.assertTrue(User.get_by_email(user.email))

        # change email
        user.email = 'hello2@example.com'
        user.save()

        self.assertEqual(user.email, 'hello2@example.com')
        self.assertTrue(User.get_by_email(user.email))
        self.assertFalse(User.get_by_email('hello@example.com'))

        # reset email
        user.email = 'hello@example.com'
        user.save()

    def password(self, user):
        # password
        self.assertTrue(user.authenticate('hello'))
        user.password = 'world'
        user.save()

        # check updating password
        user2 = User.get_by_id(user.id)
        self.assertFalse(user2.authenticate('hello'))
        self.assertTrue(user2.authenticate('world'))

        # reset password
        user.password = 'hello'
        user.save()

    def authentication(self, user):
        user2 = User.authenticate_user(user.email, 'hello')

        self.assertTrue(user.id == user2.id)
        self.assertFalse(User.authenticate_user(user.email, 'world'))
        self.assertFalse(User.authenticate_user('world@example.com', 'hello'))

    def reset(self):
        """
        clean up any remaining test users
        """
        for business_id in self.created_ids:
            business = Business.get_by_id(business_id)

            if business:
                business.delete()


# class AuthAPI(unittest.TestCase):
#     def setUp(self):
#         from service import main
#         from paste.deploy import appconfig
#         from webtest import TestApp

#         # set settings
#         os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
#         self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
#         app = main({}, **self.settings)
#         self.testapp = TestApp(app)
#         self.config = testing.setUp(settings=self.settings)

#         self.user = User.create('hello@example.com', 'hello')

#     def tearDown(self):
#         self.user.delete()
#         testing.tearDown()

#     def test_auth_get(self):
#         response = self.testapp.get('/api/v1/authenticate', status=200)
#         self.assertTrue('hello' in response.json)
#         self.assertTrue(response.json['hello'] == 'world')

#     def test_auth_post(self):
#         response = self.testapp.post_json('/api/v1/authenticate', {}, status=400)

#         payload = {
#             'email': 'wrong',
#             'password': 'wrong',
#         }
#         response = self.testapp.post_json('/api/v1/authenticate', payload, status=401)

#         payload = {
#             'email': 'hello@example.com',
#             'password': 'hello',
#         }
#         response = self.testapp.post_json('/api/v1/authenticate', payload, status=200)
#         self.assertTrue(response.json['access_token'] and response.json['user_id'])


# class UserAPI(unittest.TestCase):
#     def setUp(self):
#         from service import main
#         from paste.deploy import appconfig
#         from webtest import TestApp

#         # set settings
#         os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
#         self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
#         app = main({}, **self.settings)
#         self.testapp = TestApp(app)
#         self.config = testing.setUp(settings=self.settings)

#     def tearDown(self):
#         user = User.get_by_email('hello@example.com')

#         if user:
#             user.delete()

#         testing.tearDown()

#     def test_user_creation(self):
#         response = self.testapp.post_json('/api/v1/users', {}, status=400)

#         payload = {
#             'email': 'hello@example.com',
#             'password': 'hello',
#         }
#         response = self.testapp.post_json('/api/v1/users', payload, status=200)
#         self.assertTrue(response.json['id'])

#         # check duplicate
#         response = self.testapp.post_json('/api/v1/users', payload, status=400)

#         # check database and clean up
#         user = User.get_by_email('hello@example.com')
#         self.assertTrue(user)
#         self.assertTrue(user.delete())

