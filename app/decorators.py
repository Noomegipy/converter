import marshmallow

from app.errors import get_validation_error, post_validation_error


def validate_request(get=None, post=None):
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            if get:
                try:
                    request.get = get().load(request.args)
                except marshmallow.ValidationError:
                    return get_validation_error
            if post:
                try:
                    request.post = post().load(request.json)
                except marshmallow.ValidationError:
                    return post_validation_error
            return func(view, request, *args, **kwargs)
        return wrapper
    return decorator
