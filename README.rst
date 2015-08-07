################
HINGE FIVESQUARE
################

This is the documentation for the Fivesquare tech task for Hinge.

See the `wiki<https://github.com/digitaldreamer/fivesquare/wiki/Task>`_ to review the task.

Check out the `API documentation<http://hinge-api-interview-juniper.herokuapp.com/>` for instructions.


SETUP
=====

initialize virtual environment with requirements.txt::

    cd /path/to/env/dir
    virtualenv fivesquare
    source fivesquare/bin/activate
    pip install -r /path/to/requirements.txt


RUNNING LOCAL
=============


MAKEFILE
========


TESTS
=====

Nose is used for tests

::

    # examples
    cd /path/to/service

    nosetests
    nosetests service.apps.auth
    nosetests service.apps.auth.tests:UserAPI
    nosetests service.apps.auth.tests:UserAPI.test_user_creation


REFERENCE
=========

| repo: https://github.com/digitaldreamer/fivesquare
| wiki: https://github.com/digitaldreamer/fivesquare/wiki
| website/api docs: http://hinge-api-interview-juniper.herokuapp.com/
| api root: http://hinge-api-interview-juniper.herokuapp.com/api/v1
