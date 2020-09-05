import json
from functools import partial

import aioredis

from app.schemas import DecimalEncoder


async def get_redis_pool(host='redis', database=None):
    redis = await aioredis.create_redis_pool(
        f'redis://{host}', db=database)
    return redis


class CurrenciesRedis:
    def __init__(self, pool, loads=None, dumps=None):
        self.pool = pool
        self.loads = loads or json.loads
        self.dumps = dumps or partial(json.dumps, cls=DecimalEncoder)

    async def get_currencies(self):
        currencies = await self.pool.get("currencies")
        if not currencies:
            return None
        return self.loads(currencies)

    async def set_currencies(self, currencies):
        await self.pool.set("currencies", self.dumps(currencies))
