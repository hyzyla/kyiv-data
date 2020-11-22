from typing import List, Tuple

from flask import request

from app.main import db
from app.models import Ticket
from app.schemas import TicketSchema

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


def create_ticket(data: Ticket) -> Ticket:
    ticket = Ticket(
        **data,
        # external_id=data.external_id,
        # number=data.number,
        # title=data.title,
        # text=data.text,
        # status=data.status,
        # address=data.address,
        # work_taken_by=data.work_taken_by,
        # approx_done_date=data.approx_done_date,
        # created_at=data.created_at,
        # subject_id=data.subject_id,
        # user_id=data.user_id,
        # district_id=data.district_id,
        # city_id=data.city_id,
        # source=data.source,
        # meta=data.meta,
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket
