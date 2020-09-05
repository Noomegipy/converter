from decimal import Decimal

from sanic.views import HTTPMethodView

from app.schemas import (
    ConvertRequestSchema,
    DatabaseCurrencySchema,
    DatabaseRequestSchema,
    ConvertResponseSchema,
)
from app.decorators import validate_request
from app.errors import currency_not_found
from app.redis import CurrenciesRedis


class Convert(HTTPMethodView):

    def make_response(self, data):  # pylint: disable=no-self-use
        return ConvertResponseSchema().dump(dict(result=data))

    @validate_request(get=ConvertRequestSchema)
    async def get(self, request):
        redis = CurrenciesRedis(pool=request.app.redis)
        from_cur = request.get['from_cur']
        to_cur = request.get['to_cur']
        amount = request.get['amount']

        if from_cur == to_cur:
            return self.make_response(amount.normalize())

        currencies = await redis.get_currencies() or {}
        course = currencies.get(from_cur, {}).get(to_cur)
        if not course:
            return currency_not_found

        result = (amount * Decimal(course)).quantize(Decimal(".0000")).normalize()
        return self.make_response(result)


class LoadDatabase(HTTPMethodView):

    async def get(self, request):
        redis = CurrenciesRedis(pool=request.app.redis)
        currencies = await redis.get_currencies() or {}
        return DatabaseCurrencySchema().dump(dict(currencies=currencies))

    @validate_request(get=DatabaseRequestSchema, post=DatabaseCurrencySchema)
    async def post(self, request):
        new_currencies = request.post['currencies']
        redis = CurrenciesRedis(pool=request.app.redis)

        if request.get['merge']:
            currencies = await redis.get_currencies() or {}
            for currency, courses in new_currencies.items():
                old_courses = currencies.get(currency, {})
                old_courses.update(courses)
                currencies[currency] = old_courses
            new_currencies = currencies

        await redis.set_currencies(new_currencies)
        return DatabaseCurrencySchema().dump(dict(currencies=new_currencies))
