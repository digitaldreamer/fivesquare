import os
import unittest

from pyramid import testing

from auth.models import User
from reviews.models import Review
from businesses.models import Business


class ReviewModel(unittest.TestCase):
    def setUp(self):
        from paste.deploy import appconfig

        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.settings = appconfig('config:{}'.format(os.environ['PYRAMID_SETTINGS']), relative_to='.')
        self.config = testing.setUp(settings=self.settings)
        self.created_ids = []

        user = User.create('hello@example.com', 'world')
        self.user = User.get_by_email('hello@example.com')
        self.business = self.create_business()

    def tearDown(self):
        self.reset()
        testing.tearDown()

    def test_reviews(self):
        review = Review.create(self.user.id, self.business, 1, 'This is a review', tags=['hello', 'world'])
        self.created_ids.append(review.id)

        review = Review.create(self.user.id, self.business, 5, 'This is a another review', tags=['hello', 'something'])
        self.created_ids.append(review.id)

        self.business = Business.get_by_id(self.business.id)
        self.assertTrue(self.business.rating == 3)
        self.assertTrue('hello' in self.business.tags)
        self.assertTrue('world' in self.business.tags)
        self.assertTrue('something' in self.business.tags)

        review.delete()
        self.business = Business.get_by_id(self.business.id)
        self.assertTrue(self.business.rating == 1)
        self.assertFalse('something' in self.business.tags)

        review = Review.create(self.user.id, self.business, 5, 'This is a another review', tags=['hello', 'something'])
        self.created_ids.append(review.id)

    def create_business(self):
        address = {
            'street1': 'Central Park',
            'city': 'New York',
            'state': 'NY'
        }
        business = Business.create('Central Park', address)
        return business

    def reset(self):
        """
        clean up any remaining test users
        """
        return
        for _id in self.created_ids:
            review = Review.get_by_id(_id)

            if review:
                review.delete()

        self.user.delete()
        self.business.delete()
