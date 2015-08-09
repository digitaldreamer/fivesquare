import pyramid
import pymongo

from bson import ObjectId

from auth.models import User
from main.models import MongoObject
from reviews.custom_events import ReviewUpdated
from service import logger
from storage.mongo import mongodb


class Review(MongoObject):
    collection = 'reviews'

    def __init__(self, user_id=None, reviewed_collection='', reviewed_id=None, rating=0, text='', tags=[], mongo=None):
        super(Review, self).__init__(mongo=mongo)

        if not mongo:
            self.data.update({
                'user_id': user_id,
                'reviewed_collection': reviewed_collection,
                'reviewed_id': reviewed_id,
                'rating': 0,
                'text': '',
                'tags': [],
            })

        if rating:
            self.rating = rating
        if text:
            self.text = text
        if tags:
            self.tags = tags

        self.data['user_id'] = ObjectId(self.data['user_id'])
        self.data['reviewed_id'] = ObjectId(self.data['reviewed_id'])

    @property
    def user_id(self):
        return self.data['user_id']

    @property
    def reviewed_collection(self):
        return self.data['reviewed_collection']

    @property
    def reviewed_id(self):
        return self.data['reviewed_id']

    @property
    def user(self):
        user = User.get_by_id(self.data['user_id'])
        return user

    @property
    def rating(self):
        return self.data.get('rating', 0)

    @rating.setter
    def rating(self, rating):
        self.data['rating'] = rating

    @property
    def text(self):
        return self.data.get('text', '')

    @text.setter
    def text(self, text):
        self.data['text'] = text

    @property
    def tags(self):
        return self.data.get('tags', [])

    @tags.setter
    def tags(self, tags):
        self.data['tags'] = tags

    def save(self):
        saved = super(Review, self).save()
        Review.update_reviewed(self.reviewed_collection, self.reviewed_id)
        return saved

    def delete(self):
        deleted = super(Review, self).delete()
        Review.update_reviewed(self.reviewed_collection, self.reviewed_id)
        return deleted

    @classmethod
    def reviews_for_reviewed(cls, reviewed_id, offset=0, limit=100):
        """
        Return the reviews for a reviewed object
        """
        reviews = []
        mongo_businesses = mongodb[cls.collection].find({'reviewed_id': ObjectId(reviewed_id)}).sort('created', pymongo.DESCENDING).limit(limit).skip(offset)

        for mongo_review in mongo_reviews:
            review = cls(mongo=mongo_review)
            reviews.append(review)

        return reviews

    @classmethod
    def tags_for_reviewed(cls, reviewed_id):
        """
        returns the unique tags that belong to the reviewed object
        """
        tags = mongodb[cls.collection].distinct('tags', {'reviewed_id': ObjectId(reviewed_id)})
        return tags

    @classmethod
    def update_reviewed(cls, reviewed_collection, reviewed_id):
        """
        update ratings and tags

        this is called on review change in the assumption that
        updates are far less frequent than reads
        """
        mongo_entry = mongodb[reviewed_collection].find_one({'_id': reviewed_id})
        mongo_entry['rating'] = Review.rating_for_reviewed(reviewed_id)
        mongo_entry['tags'] = Review.tags_for_reviewed(reviewed_id)
        mongo_entry = mongodb[reviewed_collection].update({'_id': reviewed_id}, mongo_entry)

    @classmethod
    def rating_for_reviewed(cls, reviewed_id):
        """
        returns the average rating for the reviewed object
        """
        rating = 0
        results = mongodb[cls.collection].aggregate([
            {'$match': {'reviewed_id': ObjectId(reviewed_id)}},
            {
                '$group': {
                    '_id': '$reviewed_id',
                    'rating': {'$avg': '$rating'}
                }
            }])

        for result in results:
            rating = result.get('rating', 0)

        return rating

    @classmethod
    def create(cls, user_id, reviewed, rating, text, tags=[]):
        """
        creates, saves, and returns a new review
        """
        review = cls(
            user_id = user_id,
            reviewed_collection = reviewed.collection,
            reviewed_id = reviewed.id,
            rating = rating,
            text = text,
            tags = tags,
        )
        review.save()
        return review

