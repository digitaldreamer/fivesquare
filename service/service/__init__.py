import os
import sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.sep.join(PROJECT_PATH.split(os.sep)[:-1])

# include paths
sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound

# logging
import logging
logger = logging.getLogger(__name__)

def notfound(request):
    return HTTPNotFound('Page not found.')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/home')

    config.add_route('catchall_static', '/*subpath')
    config.add_view('service.static.static_view', route_name='catchall_static')

    config.add_notfound_view(notfound, append_slash=False)
    config.scan()
    return config.make_wsgi_app()
