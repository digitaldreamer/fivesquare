"""
export PYRAMID_SETTINGS=/place/to/development.ini#main

migh want to replace this file with
pyramid.threadlocal.get_current_registry().settings
"""
import os

from paste.deploy.loadwsgi import appconfig


CWD = os.path.abspath(__file__)
PATH = os.sep.join(CWD.split(os.sep)[:-2])

ini = os.environ.get('PYRAMID_SETTINGS', 'development.ini#main')
config_file, section_name = ini.split('#', 1)
file_path = os.sep.join([PATH, config_file])
config = appconfig('config:%s' % file_path, section_name, relative_to='.')
