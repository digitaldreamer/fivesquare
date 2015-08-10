import argparse
import getpass
import sys

from pyramid.paster import bootstrap
from auth.models import User

pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))


def prompt(env):
    email = raw_input('email: ')
    password1, password2 = pprompt()

    while password1 != password2:
        print "Passwords do not match. Try again."
        password1, password2 = pprompt()

    user = User.create(email, password1)

    if user:
        print "user '{}' created".format(user.email)
    else:
        # TODO: better error messaging
        print "error: user {} not created" % email


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='configuration.ini file')
    args = parser.parse_args(argv[1:])
    env = bootstrap(args.file)
    prompt(env)
