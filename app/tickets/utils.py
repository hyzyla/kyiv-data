from datetime import datetime
from typing import List, Tuple
import re

from flask import request

from app.extensions import db
from app.lib.types import DataDict
from app.tickets.models import Ticket
from app.users.types import UserCtx

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
