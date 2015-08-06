import os
import unittest

from pyramid import testing
from auth.models import User
from auth.exceptions import UserSaveError


class UserModel(unittest.TestCase):
    def setUp(self):
        from paste.deploy import appconfig

        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
        self.config = testing.setUp(settings=self.settings)
        self.reset()

    def tearDown(self):
        self.reset()
        testing.tearDown()

    def test_user_management(self):
        """
        test user creation and deletion
        """
        # creation
        user = User.create('world@example.com', 'world')
        self.assertTrue(user)

        # retrieve
        self.assertTrue(User.get_by_id(user.id))
        self.assertTrue(User.get_by_email(user.email))

        # duplicated users
        self.assertFalse(User.create('world@example.com', 'world'))

        try:
            user2 = User(email='world@example.com', password='world')
            user2.save()
        except UserSaveError:
            pass
        else:
            self.assertFalse('The user wrongly saved')

        # deletion
        self.assertTrue(user.delete())
        user4 = User.get_by_email('world@example.com')
        self.assertFalse(user4)

    def test_user(self):
        user = self.create_user()
        self.email(user)
        self.password(user)
        self.authentication(user)
        self.assertTrue(user.delete())

    def create_user(self):
        # check user
        user = User.create('hello@example.com', 'hello')
        self.assertTrue(user)
        return user

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
        emails = ['hello@example.com', 'hello2@example.com', 'world@example.com']

        for email in emails:
            user = User.get_by_email(email)

            if user:
                user.delete()


class AuthAPI(unittest.TestCase):
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

        self.user = User.create('hello@example.com', 'hello')

    def tearDown(self):
        self.user.delete()
        testing.tearDown()

    def test_auth_get(self):
        response = self.testapp.get('/authenticate', status=200)
        self.assertTrue('hello' in response.json)
        self.assertTrue(response.json['hello'] == 'world')

    def test_auth_post(self):
        response = self.testapp.post_json('/authenticate', {}, status=400)

        payload = {
            'email': 'wrong',
            'password': 'wrong',
        }
        response = self.testapp.post_json('/authenticate', payload, status=401)

        payload = {
            'email': 'hello@example.com',
            'password': 'hello',
        }
        response = self.testapp.post_json('/authenticate', payload, status=200)


class UserAPI(unittest.TestCase):
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

    def tearDown(self):
        user = User.get_by_email('hello@example.com')

        if user:
            user.delete()

        testing.tearDown()

    def test_user_creation(self):
        response = self.testapp.post_json('/users', {}, status=400)

        payload = {
            'email': 'hello@example.com',
            'password': 'hello',
        }
        response = self.testapp.post_json('/users', payload, status=200)
        self.assertTrue(response.json['id'])

        # check duplicate
        response = self.testapp.post_json('/users', payload, status=400)

        # check database and clean up
        user = User.get_by_email('hello@example.com')
        self.assertTrue(user)
        self.assertTrue(user.delete())
