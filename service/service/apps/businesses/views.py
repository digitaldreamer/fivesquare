import json
import urllib

from cornice import Service
from pyramid.exceptions import Forbidden
from pyramid.view import view_config

from auth.security import valid_key
from businesses.models import Business
from businesses.schemas import BusinessSchema, BusinessesSchema, NewBusinessSchema
from reviews.models import Review
from reviews.schemas import ReviewSchema
from service import logger
from service.utils.jsonencoder import ComplexEncoder
from storage.redis import redis_cache


businesses = Service(name='businesses', path='/businesses', description='Businesses')
business = Service(name='business', path='/businesses/{business_id}', description='Business')
business_reviews = Service(name='business_reviews', path='/businesses/{business_id}/reviews', description='Business Reviews')
business_review = Service(name='business_review', path='/businesses/{business_id}/reviews/{review_id}', description='Business Review')


class BusinessViews(object):
    @businesses.get(schema=BusinessesSchema)
    def businesses_get(request):
        """
        Returns the businesses

        # all results with pagination
        http://localhost:8000/api/v1/businesses?limit=100&offset=0

        # filter results from location to the max distance radius
        http://localhost:8000/api/v1/businesses?lng=-73.988395&lat=40.7461666&distance=3

        playing with table formatting

        =====  =====  =======
        A      B      A and B
        =====  =====  =======
        False  False  False
        True   False  False
        False  True   False
        True   True   True
        =====  =====  =======


        ======  =====  ======
        Inputs Output
        -------------  ------
        A       B      A or B
        ======  =====  ======
        False   False  False
        True    False  True
        False   True   True
        True    True   True
        ======  =====  ======


        =====  =====
        col 1  col 2
        =====  =====
        1      Second column of row 1.
        2      Second column of row 2.

               Second line of paragraph.
        3      - Second column of row 3.

               - Second item in bullet
                   list (row 3, column 2).
        \      Row 4; column 1 will be empty.
        =====  =====

        """
        location = []
        lat = request.validated['lat']
        lng = request.validated['lng']
        distance = request.validated['distance']
        units = request.validated['units']
        limit = request.validated['limit']
        offset = request.validated['offset']

        if lat and lng:
            location = [lng, lat]

        businesses = Business.businesses(location=location, distance=distance, units=units, limit=limit, offset=offset)

        # TODO: this count is wrong when location limiting
        if location:
            businesses_count = len(businesses)
        else:
            businesses_count = Business.count()

        businesses_jsonable = []

        for business in businesses:
            businesses_jsonable.append(business.toJSON())

        response_body = {
            'businesses': businesses_jsonable,
            'count': businesses_count,
        }
        logger.debug('Retrieved businesses')

        request.response.body = json.dumps(response_body, cls=ComplexEncoder)
        request.response.content_type = 'application/json'
        return request.response

    @businesses.post(schema=NewBusinessSchema, validators=valid_key)
    def businesses_post(request):
        """
        create a new business

        requires authentication with access_token
        """
        user = request.validated['user']
        name = request.validated['name']
        address = {
            'street1': request.validated['street1'],
            'street2': request.validated['street2'],
            'city': request.validated['city'],
            'state': request.validated['state'],
            'postal_code': request.validated['postal_code'],
        }

        business = Business.create(name, address)

        if business:
            logger.debug('Created new business:{}'.format(business.id))
            response_body = {
                'id': business.id
            }
        else:
            logger.debug('Failed to create new business.')
            requests.response.status_int = 500
            response_body = {
                'status': 'error',
                'message': 'failed to create new business',
            }

        request.response.body = json.dumps(response_body, cls=ComplexEncoder)
        request.response.content_type = 'application/json'
        return request.response

    @business.get(schema=BusinessSchema)
    def business_get(request):
        """
        Returns the business

        """
        business_id = request.matchdict['business_id']
        include_reviews = request.validated['reviews']
        business = Business.get_by_id(business_id)

        # a light redis check is an example of how queries can be further optimized
        if include_reviews:
            cache_key = 'business:{}:reviews-true'.format(business_id)
        else:
            cache_key = 'business:{}:reviews-false'.format(business_id)

        cached = redis_cache.get(cache_key)

        if cached and business:
            response_body = cached
        elif business:
            response_body = business.toJSON()

            if include_reviews:
                response_body['reviews'] = Review.reviews_for_reviewed(business.collection, business.id)

            response_body = json.dumps(response_body, cls=ComplexEncoder)
            redis_cache.set(cache_key, response_body)
            logger.debug('Retrieved business:{}'.format(business.id))
        else:
            logger.debug('Failed to retrieve business:{}'.format(business_id))
            request.response.status_int = 404
            response_body = json.dumps({
                'status': 'error',
                'message': 'failed to find business'
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response


class BusinessReviewViews(object):
    @business_reviews.get()
    def reviews_get(request):
        """
        Returns the business reviews
        """
        business_id = request.matchdict['business_id']
        business = Business.get_by_id(business_id)

        if business:
            response_body = {
                'reviews': Review.reviews_for_reviewed(business.collection, business.id)
            }
            logger.debug('Retrieved business:{} reviews'.format(business.id))
        else:
            logger.debug('Failed to retrieve business:{} reviews'.format(business_id))
            request.response.status_int = 404
            response_body = {
                'status': 'error',
                'message': 'failed to find business'
            }

        request.response.body = json.dumps(response_body, cls=ComplexEncoder)
        request.response.content_type = 'application/json'
        return request.response

    @business_reviews.post(schema=ReviewSchema, validators=valid_key)
    def reviews_post(request):
        """
        creates new business review

        auth required with access_token
        """
        business_id = request.matchdict['business_id']
        business = Business.get_by_id(business_id)
        user = request.validated['user']
        text = request.validated['text']
        rating = request.validated['rating']
        tags = request.validated['tags']

        if tags:
            tags = tags.split(':')
        else:
            tags = []

        if business and user:
            review = Review.create(user.id, business, rating, text, tags)
            response_body = {
                'id': review.id,
            }

            # kill cache
            cache_key = 'business:{}*'.format(business.id)
            redis_cache.delete_pattern(cache_key)
        else:
            logger.debug('Failed to create review for business:{}'.format(business_id))
            request.response.status_int = 400
            response_body = {
                'status': 'error',
                'message': 'failed to create review for business'
            }

        request.response.body = json.dumps(response_body, cls=ComplexEncoder)
        request.response.content_type = 'application/json'
        return request.response

    @business_review.get()
    def review_get(request):
        """
        Returns the business review
        """
        business_id = request.matchdict['business_id']
        review_id = request.matchdict['review_id']
        business = Business.get_by_id(business_id)
        review = Review.get_by_id(review_id)

        if business and review and business.id == review.reviewed_id:
            response_body = review.json
            logger.debug('Retrieved business:{} review:{}'.format(business.id, review.id))
        else:
            logger.debug('Failed to retrieve business:{} review:'.format(business_id, review_id))
            request.response.status_int = 404
            response_body = json.dumps({
                'status': 'error',
                'message': 'failed to find business review'
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response
