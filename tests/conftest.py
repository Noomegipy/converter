import pytest

from app.main import converter
from app.redis import get_redis_pool


@pytest.yield_fixture
async def converter_app():
    converter.redis = await get_redis_pool(host='localhost', database=2)  # db for testing
    yield converter
    converter.redis.close()
    await converter.redis.wait_closed()


@pytest.yield_fixture
async def flush_redis(converter_app):
    await converter_app.redis.flushdb()
