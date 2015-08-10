################
HINGE FIVESQUARE
################

This is the documentation for the Fivesquare tech test for Hinge.

See the `wiki <https://github.com/digitaldreamer/fivesquare/wiki/Task>`_ to review the task.

Check out the `API documentation <http://hinge-api-interview-juniper.herokuapp.com/>`_ for instructions.

The project is built with Pyramid. Cornice and Colander is used to power the RESTful API.

BCrypt is used to hash passwords and JWT is used to create access tokens.

The Google Maps API is used to geocode Business Addresses.

Sphinx is used to generate the API documentation.

WARNING: all endpoints in practice should be run through ssl/https, but for the purpose of this demo the server will run through http.


REFERENCE
=========

| website/api docs: http://hinge-api-interview-juniper.herokuapp.com/
| api root: http://hinge-api-interview-juniper.herokuapp.com/api/v1
| repo: https://github.com/digitaldreamer/fivesquare
| wiki: https://github.com/digitaldreamer/fivesquare/wiki


SETUP
=====

This project assumes you have run `stardust <https://github.com/digitaldreamer/stardust>`_ initialization. You can also run ``make ubuntu`` to build your local environment if needed.

initialize virtual environment with requirements.txt::

    cd /path/to/project
    make ubuntu

    cd /path/to/env/dir
    virtualenv fivesquare
    source fivesquare/bin/activate
    pip install -r /path/to/requirements.txt

    cd /path/to/service
    python setup.py develop

There are scripts to help manage the database. They can be run by passing the config file.

* reset_db - resets all data in the database
* load_db - loads and initializes data used for testing
* create_user - creates a new user

NOTE: because of how settings are loaded you also need to have the ``PYRAMID_SETTINGS`` environment variable set if not running develop.ini.::

    export PYRAMID_SETTINGS=production.ini#main
    reset_db production.ini
    load_db production.ini
    create_user production.ini

``load_db`` should be run before running the test scripts and can be used to seed data into the system.

This loads a default user with the following credentials::

    email: test@example.com
    password: test

The user can be used to authenticate to get an access_token for the requests that need authorization.


RUNNING LOCAL
=============

The default make command will run the server locally. MongoDB is required and Redis is optional depending on your settings.

The following commands are all the same::

    cd /path/to/service
    make
    make run
    pserve development.ini --reload

The server will be served from:

| docs
| http://localhost:8000
|
| api
| http://localhost:8000/api/v1


POSTMAN
=======

https://www.getpostman.com/

The postman collection file in ``/postman`` can be used to test the endpoints.

You'll need to start a new environment with the following variables defined:

* host
* access_token


MAKEFILE
========

There is a ``Makefile`` in the /service directory to help automate commands. Here's a list of targets.

=======  ===========
command  description
=======  ===========
run      (default) runs the pyramid pserve local server
build    Second column of row 2.
ubuntu   installs the dependencies into an ubuntu server
redis    used to connect to the rediscloud cli
clean    cleans all compiled files
tailog   tail the heroku server logs
=======  ===========

TESTS
=====

Nose is used for tests. Some of the tests depend on the database to be initialized through the ``load_db`` script. See the SETUP section for details.

::

    # examples
    cd /path/to/service

    nosetests
    nosetests service.apps.auth
    nosetests service.apps.auth.tests:UserAPI
    nosetests service.apps.auth.tests:UserAPI.test_user_creation
