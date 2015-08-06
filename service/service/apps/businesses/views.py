import json

from cornice import Service
from pyramid.exceptions import Forbidden
from pyramid.view import view_config

# from auth.models import User
# from auth.schemas import AuthSchema, UserSchema, NewUserSchema
from service import logger


businesses = Service(name='businesses', path='/businesses', description='Businesses')
business = Service(name='business', path='/businesses/{business_id}', description='Business')
business_reviews = Service(name='business_reviews', path='/businesses/{business_id}/reviews', description='Business Reviews')
business_review = Service(name='business_review', path='/businesses/{business_id}/reviews/{review_id}', description='Business Review')


class BusinessViews(object):
    @businesses.get()
    def businesses_get(request):
        """
        a simple endpoint to run tests through

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
        request.response.body = json.dumps({'hello': 'world'})
        request.response.content_type = 'application/json'
        return request.response
