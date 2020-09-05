import json

import pytest


@pytest.mark.asyncio
async def test_convert(converter_app, flush_redis):
    converter_app.redis.set("currencies", json.dumps(
        {
            "RUB": {"EUR": "0.1", "USD": "0.2"},
            "USD": {"RUB": "0.3", "EUR": "0.4"},
            "AED": {"RUB": "1.0009"}
        }
    ))
    from_cur, to_cur, amount = 'RUB', 'EUR', 60
    request, response = await converter_app.asgi_client.get(
        f'/convert?from={from_cur}&to={to_cur}&amount={amount}',
    )
    assert response.status == 200
    assert response.json() == {"result": "6"}


    from_cur, to_cur, amount = 'USD', 'EUR', 0.55
    request, response = await converter_app.asgi_client.get(
        f'/convert?from={from_cur}&to={to_cur}&amount={amount}',
    )
    assert response.status == 200
    assert response.json() == {"result": "0.22"}


    from_cur, to_cur, amount = 'AED', 'RUB', 120000
    request, response = await converter_app.asgi_client.get(
        f'/convert?from={from_cur}&to={to_cur}&amount={amount}',
    )
    assert response.status == 200
    assert response.json() == {"result": "120108"}


@pytest.mark.asyncio
async def test_convert_400(converter_app, flush_redis):
    validation_error = {
        'error': {
            "code": "validation_error",
            "description": "invalid get params"
        }
    }
    currency_not_found = {
        'error': {
            "code": "no_currency",
            "description": "Our system does not support one of your currencies"
        }
    }

    from_cur, to_cur, amount = 'RUB', 'EUR', "evil_amount_string"
    request, response = await converter_app.asgi_client.get(
        f'/convert?from={from_cur}&to={to_cur}&amount={amount}',
    )
    assert response.status == 400
    assert response.json() == validation_error

    from_cur, to_cur, amount = 'RUB', 'EUR', -1
    request, response = await converter_app.asgi_client.get(
        f'/convert?from={from_cur}&to={to_cur}&amount={amount}',
    )
    assert response.status == 400
    assert response.json() == validation_error

    from_cur, to_cur, amount = 'RUB', 'EUR', 200
    request, response = await converter_app.asgi_client.get(
        f'/convert?from={from_cur}&to={to_cur}&amount={amount}',
    )
    assert response.status == 400
    assert response.json() == currency_not_found
