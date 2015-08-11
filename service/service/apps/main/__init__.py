def includeme(config):
    config.include('main.routes')
    config.scan('main.views')
