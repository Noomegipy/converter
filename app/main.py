import os

from sanic import Sanic
from sanic.request import Request
from sanic.response import json as make_json

from app.views import Convert, LoadDatabase
from app.redis import get_redis_pool


class ConverterRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get = None
        self.post = None


class ConverterApplication(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(
            request_class=ConverterRequest,
            *args,
            **kwargs
        )
        self.redis = None


converter = ConverterApplication(name='converter')


@converter.listener('after_server_start')
async def setup_redis(app, loop):  # pylint: disable=unused-argument
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    app.redis = await get_redis_pool(host=redis_host)


@converter.listener('before_server_stop')
async def teardown_redis(app, loop):  # pylint: disable=unused-argument
    app.redis.close()
    await app.redis.wait_closed()


@converter.middleware('response')
async def handle_dict(request, response):  # pylint: disable=unused-argument
    if isinstance(response, dict):
        return make_json(response)
    return response

converter.add_route(Convert.as_view(), '/convert')
converter.add_route(LoadDatabase.as_view(), '/database')

if __name__ == '__main__':
    converter.run(host='0.0.0.0', port=5000)
