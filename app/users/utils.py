from functools import wraps

import jwt
from flask import request
from jwt import PyJWTError

from app.lib.config import settings
from app.lib.errors import InvalidTokenError
from app.tickets.utils import TOKEN_RE
from app.users.types import UserCtx


def _validate_service_token():
    token = request.headers.get('Authorization')
    if token != settings.AUTH_TOKEN:
        raise InvalidTokenError(
            message=(
                'Не валідний сервісний токен. Передайте токен згенерований '
                'адміністором системи у заголовку запиту Authorization'
            ),
            extra={'is_token_empty': bool(bool)},
        )


def _validate_user_token() -> UserCtx:
    auth = request.headers.get('Custom-Token')
    if not auth:
        raise InvalidTokenError(message='Токен користувача не знайдено')

    match = TOKEN_RE.match(auth)
    token: str = match.group('token')
    try:
        payload = jwt.decode(jwt=token, algorithms='HS256', verify=False, options={'verify_signature': False})
    except PyJWTError as error:
        raise InvalidTokenError(extra={'reason': str(error)})

    return UserCtx(user_id=payload['sub'], token=token)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        _validate_service_token()
        ctx = _validate_user_token()

        return func(ctx, *args, **kwargs)

    return wrapper
