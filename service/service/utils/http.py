import json

from webob import Response, exc


class Http400(exc.HTTPError):
    def __init__(self, msg='Bad Request'):
        body = {'status': 400, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 400
        self.content_type = 'application/json'


class Http401(exc.HTTPError):
    def __init__(self, msg='Unauthorized'):
        body = {'status': 401, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 401
        self.content_type = 'application/json'


class Http403(exc.HTTPError):
    def __init__(self, msg='Forbidden'):
        body = {'status': 403, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 403
        self.content_type = 'application/json'


class Http404(exc.HTTPError):
    def __init__(self, msg='Not Found'):
        body = {'status': 404, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 404
        self.content_type = 'application/json'


class Http500(exc.HTTPError):
    def __init__(self, msg='Internal Server Error'):
        body = {'status': 500, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 500
        self.content_type = 'application/json'


class Http501(exc.HTTPError):
    def __init__(self, msg='Not Implemented'):
        body = {'status': 501, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 501
        self.content_type = 'application/json'
