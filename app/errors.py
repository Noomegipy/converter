from sanic import response


get_validation_error = response.json(
    {
        'error': {
            "code": "validation_error",
            "description": "invalid get params"
        }
    },
    status=400
)


post_validation_error = response.json(
    {
        'error': {
            "code": "validation_error",
            "description": "invalid post params"
        }
    },
    status=400
)

currency_not_found = response.json(
    {
        'error': {
            "code": "no_currency",
            "description": "Our system does not support one of your currencies"
        }
    },
    status=400
)
