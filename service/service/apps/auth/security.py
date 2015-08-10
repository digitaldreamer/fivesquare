import json
import jwt

from datetime import datetime

from auth.models import User
from service.utils.http import Http401
from service.utils.jsonencoder import iso_to_datetime
from service import logger
from storage.mongo import mongodb


def valid_key(request):
    """
    Check to see if a valid key has been sent

    If the key is valid it sets the user on the request.validated object

    ``request.validated['user']``
    """
    access_token = request.GET.get('access_token')
    validated = False

    # check which mode to authorize access
    if access_token:
        validated = validate_access_token(access_token)
    else:
        logger.debug('Invalid Access Token')
        raise Http401()

    # check if validation passed
    if validated:
        request.validated['user'] = validated.get('user')
    else:
        raise Http401()


def create_access_token(user):
    """
    Creates an access token for the user

    parameters
    ==========

    * user (auth.models.User) - a user object

    returns
    =======

    access_token (string)
    """
    from settings import config

    data = {
        'user_id': str(user.id),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(data, config.get('pepper', ''), algorithm='HS256')

    # TODO: save the access_token in the database

    return access_token


def validate_access_token(access_token):
    """
    Check to see if the access_token is valid

    parameters
    ==========

    * access_token - a token created with create_access_token

    returns
    =======

    returns True or False depending on if the access_token is valid

    """
    from settings import config

    validated = False

    # TODO: check the database for the existence of the access_token
    # the theory is that the access_token then can be explicitly removed
    # i.e. resetting the user's password

    try:
        decoded = jwt.decode(access_token, config.get('pepper', ''), algorithms=['HS256'])
    except jwt.DecodeError:
        logger.debug('jwt DecodeError')
    else:
        now = datetime.utcnow()
        then = datetime.fromtimestamp(decoded['iat'])

        age = now - then
        user = User.get_by_id(decoded['user_id'])

        # TODO: make the age configurable
        # for now the access_token is valid for 5 hours
        if age.seconds > 60 * 60 * 5:
            logger.debug('Stale Key, timestamp expired')
        elif user:
            validated = {
                'user': user,
            }
            logger.debug('Valid Key user:{}'.format(user.id))

    return validated
