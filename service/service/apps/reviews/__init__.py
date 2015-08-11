def includeme(config):
    # config.include('reviews.routes')
    config.scan('reviews.custom_events')
    config.scan('reviews.views')
