def includeme(config):
    # config.include('auth.routes')
    config.scan('auth.views')
