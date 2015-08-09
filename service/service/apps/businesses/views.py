import json

from cornice import Service
from pyramid.exceptions import Forbidden
from pyramid.view import view_config

from businesses.models import Business
from businesses.schemas import BusinessesSchema
from service import logger
from service.utils.jsonencoder import ComplexEncoder


businesses = Service(name='businesses', path='/businesses', description='Businesses')
business = Service(name='business', path='/businesses/{business_id}', description='Business')
business_reviews = Service(name='business_reviews', path='/businesses/{business_id}/reviews', description='Business Reviews')
business_review = Service(name='business_review', path='/businesses/{business_id}/reviews/{review_id}', description='Business Review')


class BusinessViews(object):
    @businesses.get(schema=BusinessesSchema)
    def businesses_get(request):
        """
        Returns the businesses

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
        limit = request.validated['limit']
        offset = request.validated['offset']
        businesses = Business.businesses(limit=limit, offset=offset)
        businesses_count = Business.count()
        businesses_jsonable = []

        for business in businesses:
            businesses_jsonable.append(business.toJSON())

        response_body = {
            'businesses': businesses_jsonable,
            'count': businesses_count,
        }

        request.response.body = json.dumps(response_body, cls=ComplexEncoder)
        request.response.content_type = 'application/json'
        return request.response

    @business.get()
    def businesses_get(request):
        """
        Returns the business
        """
        business_id = request.matchdict['business_id']
        business = Business.get_by_id(business_id)

        if business:
            response_body = business.json
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

