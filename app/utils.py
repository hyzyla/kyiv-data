from datetime import datetime
from http import HTTPStatus
from typing import List, Tuple
from functools import wraps
import re

import jwt
from flask import request
from jwt import InvalidSignatureError

from app.config import settings
from app.lib.errors import InvalidTokenError
from app.lib.types import DataDict
from app.main import db, app
from app.models import Ticket
from app.types import UserCtx

TOKEN_RE = re.compile(r'^(Bearer)?\s*(?P<token>.*)$', re.IGNORECASE)

FILTER_OPTIONS = [
    (Ticket.number, 'number'),
    (Ticket.text, 'text'),
    (Ticket.id, 'id'),
    (Ticket.external_id, 'external_id'),
    (Ticket.address, 'address'),
    (Ticket.approx_done_date, 'approx_done_date'),
    (Ticket.created_at, 'created_at'),
    (Ticket.status, 'status'),
    (Ticket.subject_id, 'subject_id'),
    (Ticket.title, 'title'),
    (Ticket.source, 'source'),
    (Ticket.district_id, 'district_id'),
    (Ticket.work_taken_by, 'work_taken_by'),
    (Ticket.user_id, 'user_id'),
]


def _parse_query(query: str) -> Tuple[str, str]:
    parts = query.split(':', maxsplit=1)
    if len(parts) == 2:
        return parts[0].lower(), parts[1]
    return 'eq', query


def _build_expressions(column: db.Column, name: str) -> List:
    queries: List[str] = request.args.getlist(name)
    if queries is None:
        return []

    expressions = []
    for query in queries:
        expr = _build_expression(column, query)
        if expr is not None:
            expressions.append(expr)

    return expressions


def _build_expression(column: db.Column, query: str):
    op, query = _parse_query(query)
    if op == 'eq':
        return column == query
    elif op == 'neq':
        return column != query
    elif op == 'gt':
        return column > query
    elif op == 'gte':
        return column >= query
    elif op == 'lt':
        return column < query
    elif op == 'lte':
        return column <= query
    elif op == 'like':
        return column.ilike(query)

    return None


def get_search_filters():
    filters = []
    for column, param in FILTER_OPTIONS:
        expr = _build_expressions(column, name=param)
        if expr:
            filters.extend(expr)

    return filters


def create_ticket(data: DataDict, ctx: UserCtx) -> Ticket:
    ticket = Ticket(**data, user_id=ctx.user_id, created_at=datetime.utcnow())
    db.session.add(ticket)
    db.session.commit()
    return ticket


def _validate_service_token():
    token = request.headers.get('Authorization')
    if token != settings.AUTH_TOKEN:
        raise InvalidTokenError(
            message=(
                'Не валідний сервісний токен. Передайте токен згенерований '
                'адміністором системи у заголовку запиту Authorization'
            ),
            extra={'is_token_empty': bool(bool)}
        )


def _validate_user_token() -> UserCtx:
    auth = request.headers.get('Custom-Token')
    match = TOKEN_RE.match(auth)
    token: str = match.group('token')
    try:
        payload = jwt.decode(
            jwt=token,
            algorithms='HS256',
            verify=True,
            options={'verify_signature': False}
        )
    except InvalidSignatureError():
        raise InvalidTokenError()

    return UserCtx(user_id=payload['sub'], token=token)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        _validate_service_token()
        ctx = _validate_user_token()

        return func(ctx, *args, **kwargs)

    return wrapper


def api_response(data: str, status: int = HTTPStatus.OK):
    return app.response_class(
        response=data,
        status=status,
        mimetype='application/json',
    )
