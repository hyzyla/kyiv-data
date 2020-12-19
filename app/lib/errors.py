from http import HTTPStatus
from typing import Optional

from app.lib.types import DataDict


class BaseError(Exception):
    message: str = 'Помилка'
    code: int = HTTPStatus.BAD_REQUEST

    def __init__(self, message: Optional[str] = None, extra: Optional[DataDict] = None) -> None:
        self.extra = extra
        self.message = message or self.message

    def to_dict(self) -> DataDict:
        return {'message': self.message, 'code': self.code, 'extra': self.extra}


class InvalidTokenError(BaseError):
    message = 'Невалідний токен доступу'
    code = HTTPStatus.FORBIDDEN


class SchemaValidatorError(BaseError):
    message = 'Запит не відповідає схемі'
