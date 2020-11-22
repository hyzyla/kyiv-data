from http import HTTPStatus
from typing import Optional

from app.lib.types import DataDict


class BaseError(Exception):
    message: str = 'Помилка'
    code: int = HTTPStatus.BAD_REQUEST

    def __init__(self, data: Optional[DataDict] = None) -> None:
        self.data = data

    def to_dict(self) -> DataDict:
        return {
            'message': self.message,
            'code': self.code,
            'extra': self.data
        }


class SchemaValidatorError(BaseError):
    message = 'Запит не відповідає схемі'


