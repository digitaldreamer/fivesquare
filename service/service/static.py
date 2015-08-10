import os

from pyramid.static import static_view
from service import PROJECT_BASE_PATH


# configure the catch-all static_view
static_path = os.path.sep.join([PROJECT_BASE_PATH, 'docs', '_build', 'html'])
static_view = static_view(static_path, use_subpath=True)
