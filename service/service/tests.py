import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from main.views import home
        request = testing.DummyRequest()
        data = home(request)
        self.assertEqual(data['project'], 'service')
