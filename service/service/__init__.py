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
    config.include('pyramid_jinja2')
    config.include('cornice')

    # templates
    config.add_notfound_view(notfound, append_slash=False)
    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')
    config.add_renderer('.jinja2', 'pyramid_jinja2.renderer_factory')
    config.add_jinja2_search_path('templates')

    # apps
    config.include('main')
    config.include('businesses', route_prefix='/api/v1')

    # static files
    config.add_route('catchall_static', '/*subpath')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_view('service.static.static_view', route_name='catchall_static')

    return config.make_wsgi_app()
