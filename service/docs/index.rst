.. fivesquare documentation master file, created by
   sphinx-quickstart on Wed Aug  5 21:13:59 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fivesquare's documentation!
======================================

All endpoints are rooted from the API Base URL::

    http://hinge-api-interview-juniper.herokuapp.com/api/v1


ENDPOINTS
---------

| :doc:`/authenticate <services/auth>`
| :doc:`/businesses <services/businesses>`
| :doc:`/businesses/id/reviews <services/businesses>`
| :doc:`/users <services/auth>`
|


SERVICES
--------

.. toctree::
    :maxdepth: 1

    services/auth
    services/businesses


AUTHENTICATION
--------------

Some services need to be authenticated with an access token to authorize access.

To create an access token send post request to the ``/authenticate`` service.

You can then authenticate the requests by passing the ``access_token`` query parameter::

    /endpont?access_token=<access token>

A default user is create with the ``load_db`` python helper script. See the README for setup instructions.

You can use the user to authenticate with the following credentials::

    {
        "email": "test@example.com",
        "password": "test"
    }

The access token will expire after 5 hours, after which a new access token needs to be generated through the ``/authenticate`` service


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
