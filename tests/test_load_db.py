import json

import pytest


@pytest.mark.asyncio
async def test_create_currencies_merge_0(converter_app, flush_redis):
    currencies = {
            "RUB": {"EUR": "0.011", "USD": "0.013"},
            "USD": {"RUB": "75.27", "EUR": "89.19"},
        }
    request_data = {
        "currencies": currencies
    }
    request, response = await converter_app.asgi_client.post(
        '/database?merge=0',
        data=json.dumps(request_data)
    )
    saved_currencies = await converter_app.redis.get("currencies")
    assert response.status == 200
    assert saved_currencies
    assert json.loads(saved_currencies) == currencies


@pytest.mark.asyncio
async def test_create_currencies_merge_1(converter_app, flush_redis):
    converter_app.redis.set("currencies", json.dumps(
        {
            "RUB": {"EUR": "0.1", "USD": "0.2"},
            "USD": {"RUB": "0.3", "EUR": "0.4"},
        }
    ))

    currencies = {
            "RUB": {"EUR": "0.9"},
            "USD": {"AED": "0.33"},
            "AED": {"RUB": "12"}
        }
    request_data = {
        "currencies": currencies
    }
    request, response = await converter_app.asgi_client.post(
        '/database?merge=1',
        data=json.dumps(request_data)
    )
    saved_currencies = await converter_app.redis.get("currencies")
    assert response.status == 200
    assert saved_currencies
    expected = {
        "RUB": {"EUR": "0.9", "USD": "0.2"},
        "USD": {"RUB": "0.3", "EUR": "0.4", "AED": "0.33"},
        "AED": {"RUB": "12"}
    }
    assert json.loads(saved_currencies) == expected
    assert response.json() == {
        "currencies": expected
    }


@pytest.mark.asyncio
async def test_create_currencies_merge_1_empty_db(converter_app, flush_redis):

    currencies = {
            "RUB": {"EUR": "0.9"},
            "USD": {"AED": "0.33"},
            "AED": {"RUB": "12"}
        }
    request_data = {
        "currencies": currencies
    }
    request, response = await converter_app.asgi_client.post(
        '/database?merge=1',
        data=json.dumps(request_data)
    )
    saved_currencies = await converter_app.redis.get("currencies")
    assert response.status == 200
    assert saved_currencies
    assert json.loads(saved_currencies) == currencies
    assert response.json() == {
        "currencies": currencies
    }


@pytest.mark.asyncio
async def test_create_currencies_400(converter_app, flush_redis):
    currencies = {
            "RUB": {"EUR": "0.9"},
            "USD": {"AED": "0.33"},
            "AED": {"RUB": "evil_string"}
        }
    request_data = {
        "currencies": currencies
    }

    request, response = await converter_app.asgi_client.post(
        '/database?merge=50',
        data=json.dumps(request_data)
    )
    assert response.status == 400
    assert response.json() == {
        'error': {
            "code": "validation_error",
            "description": "invalid get params"
        }
    }

    request, response = await converter_app.asgi_client.post(
        '/database?merge=0',
        data=json.dumps(request_data)
    )
    assert response.status == 400
    assert response.json() == {
        'error': {
            "code": "validation_error",
            "description": "invalid post params"
        }
    }


@pytest.mark.asyncio
async def test_get_currencies(converter_app, flush_redis):
    converter_app.redis.set("currencies", json.dumps(
        {
            "RUB": {"EUR": "0.1", "USD": "0.2"},
            "USD": {"RUB": "0.3", "EUR": "0.4"},
        }
    ))

    request, response = await converter_app.asgi_client.get(
        '/database',
    )
    assert response.status == 200
    assert response.json() == {
        "currencies": {
            "RUB": {"EUR": "0.1", "USD": "0.2"},
            "USD": {"RUB": "0.3", "EUR": "0.4"},
        }
    }


@pytest.mark.asyncio
async def test_get_currencies_empty(converter_app, flush_redis):
    request, response = await converter_app.asgi_client.get(
        '/database',
    )
    assert response.status == 200
    assert response.json() == {"currencies": {}}
