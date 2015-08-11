import argparse
import getpass
import sys

from pyramid.paster import bootstrap

from auth.models import User
from businesses.models import Business
from reviews.models import Review


def create_businesses():
    businesses = []
    address = {
        'street1': 'Time Square',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('Time Square', address)
    businesses.append(business)

    address = {
        'street1': 'Battery Park',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('Battery Park', address)
    businesses.append(business)

    address = {
        'street1': 'Flushing Medows',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('Flushing Medows', address)
    businesses.append(business)

    address = {
        'street1': 'Central Park',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('Central Park', address)
    businesses.append(business)

    address = {
        'street1': '2200 Broadway',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('2200', address)
    businesses.append(business)

    address = {
        'street1': '1800 Broadway',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('1800', address)
    businesses.append(business)

    address = {
        'street1': '1500 Broadway',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('1500', address)
    businesses.append(business)

    address = {
        'street1': '1200 Broadway',
        'city': 'New York',
        'state': 'NY'
    }
    business = Business.create('1200', address)
    businesses.append(business)

    return businesses

def create_reviews(user, business):
    reviews = []

    review = Review.create(user.id, business, 1, 'This is not good.', tags=['hello', 'world'])
    reviews.append(review)

    review = Review.create(user.id, business, 1, 'This is also not good.', tags=['hello', 'example'])
    reviews.append(review)

    review = Review.create(user.id, business, 5, 'This is awesome.', tags=['awesome'])
    reviews.append(review)

    return reviews

def run(env):
    user = User.create('test@example.com', 'test')
    print 'created user'

    businesses = create_businesses()
    business = businesses[0]
    print 'created businesses'

    reviews = create_reviews(user, business)
    print 'created reviews'


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='configuration.ini file')
    args = parser.parse_args(argv[1:])
    env = bootstrap(args.file)
    run(env)
