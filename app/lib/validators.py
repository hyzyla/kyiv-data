from typing import TypeVar

from flask import request
from marshmallow import ValidationError, Schema

from app.lib.errors import SchemaValidatorError
from app.lib.types import DataDict


T = TypeVar('T', bound=Schema)


def validate_request_json(schema: T) -> DataDict:
    """ Validate request data by schema """
    _data = request.data
    data = request.get_json(force=True)
    app.logger.info(f'JSON data {type(data)}: {data}')
    try:
        return schema.load(data)
    except ValidationError as err:
        raise SchemaValidatorError(extra=err.messages)
