import argparse
import getpass
import sys

from pyramid.paster import bootstrap
from storage.mongo import mongodb


def prompt(env):
    mongodb.users.remove()
    mongodb.businesses.remove()
    mongodb.reviews.remove()

def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='configuration.ini file')
    args = parser.parse_args(argv[1:])
    env = bootstrap(args.file)
    prompt(env)
