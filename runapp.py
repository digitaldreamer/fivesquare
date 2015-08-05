import os

from paste.deploy import loadapp
from waitress import serve


if __name__ == "__main__":
    cwd = os.getcwd()
    # os.chdir(os.path.sep.join([cwd, 'service']))
    path = os.path.sep.join([cwd, 'service'])

    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:production.ini', relative_to=path)
    serve(app, host='0.0.0.0', port=port)
