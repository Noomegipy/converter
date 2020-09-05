import json

import decimal

from marshmallow import fields, Schema
from marshmallow.validate import OneOf, Range


class ConvertRequestSchema(Schema):
    from_cur = fields.String(required=True, data_key='from')
    to_cur = fields.String(required=True, data_key='to')
    amount = fields.Decimal(required=True, places=2, validate=[Range(min=0, error="Value must be non negative")])


class ConvertResponseSchema(Schema):
    result = fields.Decimal(as_string=True)


class DatabaseRequestSchema(Schema):
    merge = fields.Integer(required=True, validate=OneOf([0, 1]))


class DatabaseCurrencySchema(Schema):
    currencies = fields.Dict(
        keys=fields.Str(), values=fields.Dict(
            keys=fields.Str(),
            values=fields.Decimal(
                as_string=True,
                validate=[Range(min=0, error="Value must be non negative")],
            )
        ), required=True
    )


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)
