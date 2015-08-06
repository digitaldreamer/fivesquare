import bcrypt

from bson import ObjectId
from datetime import datetime

from auth.exceptions import UserSaveError
from main.models import MongoObject
from service import logger
from storage.mongo import mongodb


class User(MongoObject):
    collection = 'users'

    def __init__(self, email='', password='', active=False, mongo=None):
        super(User, self).__init__(mongo=mongo)

        if not mongo:
            self.data.update({
                'active': 'false',
                'email': '',
                'password': '',
            })

        if email:
            self.email = email
        if password:
            self.password = password

    @property
    def email(self):
        return self.data.get('email', '')

    @email.setter
    def email(self, email):
        self.data['email'] = email

    @property
    def password(self):
        return self.data.get('password', '')

    @password.setter
    def password(self, password):
        from settings import config

        pepper = config.get('pepper', '')
        hashed = bcrypt.hashpw(str(password) + pepper, bcrypt.gensalt())
        self.data['password'] = hashed

    def toJSON(self):
        """
        returns a cleaned jsonable object
        """
        data = super(User, self).toJSON()
        data.pop('password')
        return data

    def authenticate(self, password):
        """
        checks to see if the password matches the user's saved password
        """
        from settings import config

        validated = False
        pepper = config.get('pepper', '')

        hashed = bcrypt.hashpw(str(password) + pepper, self.data.get('password', '').encode('utf8'))

        if hashed == self.data.get('password', ''):
            validated = True

        return validated

    def save(self):
        """
        saves the user
        """
        existing_user = User.get_by_email(self.email)

        # check for duplicate emails
        if existing_user and existing_user.id != self.id:
            raise UserSaveError('email already exists')

        return super(User, self).save()

    @classmethod
    def authenticate_user(cls, email, password):
        """
        returns the user if the email and passwords authenticate,
        otherwise returns None
        """
        user = cls.get_by_email(email)

        if user and not user.authenticate(password):
            user = None

        return user

    @classmethod
    def get_by_email(cls, email):
        user = None

        mongo_user = mongodb[cls.collection].find_one({'email': email})

        if mongo_user:
            user = User(mongo=mongo_user)

        return user

    @classmethod
    def create(cls, email, password, active=False):
        """
        creates, saves, and returns a new user
        """
        # check for dumplicate emails
        if cls.get_by_email(email):
            return None

        user = User(email=email, password=password, active=active)
        user.save()

        return user
