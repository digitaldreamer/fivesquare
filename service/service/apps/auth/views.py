import json

from datetime import datetime
from cornice import Service
from pyramid.exceptions import Forbidden
from pyramid.view import view_config

from auth.security import create_access_token
from auth.models import User
from auth.schemas import AuthSchema, NewUserSchema, UserSchema, UserPasswordSchema
from service import logger


auth = Service(name='authenticate', path='/authenticate', description='Authentication')
users = Service(name='users', path='/users', description='Users')
user = Service(name='user', path='/users/{user_id}', description='User')
user_password = Service(name='user_password', path='/users/{user_id}/password', description='User Password')


class AuthViews(object):
    @auth.get()
    def auth_get(request):
        """
        a simple endpoint to run tests through
        """
        request.response.body = json.dumps({'hello': 'world'})
        request.response.content_type = 'application/json'
        return request.response

    @auth.post(schema=AuthSchema)
    def auth_post(request):
        """
        an endpoint to authenticate users and retrieve their access token

        Parameters:
            email - the user's email
            password - the user's password

        Returns:
            returns a user if passes, otherwise sends 401 auth error

            {
                'access_token': '',
                'user_id': ''
            }
        """
        email = request.validated['email']
        password = request.validated['password']
        user = User.authenticate_user(email, password)
        response_body = {}

        if user:
            logger.debug('user:{} authenticated'.format(email))
            access_token = create_access_token(user)
            response_body = json.dumps({
                'access_token': access_token,
                'user_id': str(user.id),
            })
        else:
            logger.debug('user:{} failed authentication'.format(email))
            request.response.status_int = 401
            response_body = json.dumps({
                'status': 'error',
                'message': 'user failed to authenticate',
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response


class UserViews(object):
    @users.post(schema=NewUserSchema)
    def users_post(request):
        """
        an endpoint to create new users

        new users are not active by default
        """
        email = request.validated['email']
        password = request.validated['password']

        user = User.create(email, password)

        if user:
            # TODO: send activation email
            logger.debug('new user created')
            response_body = user.json
        else:
            logger.debug('failed to create new user')
            request.response.status_int = 400
            response_body = json.dumps({
                'status': 'error',
                'message': 'email already exists'
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response

    @user.get()
    def user_get(request):
        user_id = request.matchdict['user_id']
        user = User.get_by_id(user_id)

        if user:
            logger.debug('got user:{}'.format(user_id))
            response_body = user.json
        else:
            logger.debug('could not find user:{}'.format(user_id))
            request.response.status_int = 404
            response_body = json.dumps({
                'status': 'error',
                'message': 'user does not exist'
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response

    @user.put(schema=UserSchema)
    def user_put(request):
        """
        Update user
        """
        user_id = request.matchdict['user_id']
        user = User.get_by_id(user_id)

        if user:
            user.active = request.validated['active']
            user.email = request.validated['email']

            # save
            if user.save():
                logger.debug('user:{} updated'.format(user_id))
                response_body = json.dumps({
                    'status': 'success',
                    'message': 'user updated'
                })
            else:
                logger.debug('failed to save user:{}'.format(user_id))
                request.response.status_int = 400
                response_body = json.dumps({
                    'status': 'error',
                    'message': 'failed to update user'
                })
        else:
            logger.debug('failed to update user:{} user not found'.format(user_id))
            request.response.status_int = 404
            response_body = json.dumps({
                'status': 'error',
                'message': 'could not find user'
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response

    @user_password.put(schema=UserPasswordSchema)
    def user_password_put(request):
        """
        Update user's password
        """
        user_id = request.matchdict['user_id']
        user = User.get_by_id(user_id)

        if user:
            # check for fields to update
            user.password = request.validated['password']

            # save
            if user.save():
                logger.debug('user:{} updated'.format(user_id))
                response_body = json.dumps({
                    'status': 'success',
                    'message': 'user password updated'
                })
            else:
                logger.debug('failed to save user:{} password'.format(user_id))
                request.response.status_int = 400
                response_body = json.dumps({
                    'status': 'error',
                    'message': 'failed to update user'
                })
        else:
            logger.debug('failed to update user:{} password, user not found'.format(user_id))
            request.response.status_int = 404
            response_body = json.dumps({
                'status': 'error',
                'message': 'could not find user'
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response
