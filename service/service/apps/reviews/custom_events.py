# subscribe to event
from pyramid.events import subscriber

from businesses.models import Business
from service import logger


class ReviewUpdated(object):
    def __init__(self, review):
        logger.debug('new review updated event')
        self.review = review


@subscriber(ReviewUpdated)
def update_business(event):
    """
    compiles rating and tags for a business when a review is updated
    """
    from reviews.models import Review

    review = event.review
    business = Business.get_by_id(review.reviewed_id)

    if business:
        business.rating = Review.rating_for_reviewed(review.reviewed_id)
        business.tags = Review.tags_for_reviewed(review.reviewed_id)
        business.save()
        logger.debug('updated business:{} reviews'.format(business.id))
    else:
        logger.debug('failed to update business:{} reviews'.format(review.reviewd_id))
