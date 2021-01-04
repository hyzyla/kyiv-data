import logging
from time import sleep
from typing import Dict, List, Optional

import click
import requests
from flask.cli import AppGroup

from app.extensions import db, storage
from app.lib.config import settings
from app.tickets.constants import DISTRICTS
from app.tickets.db import select_last_ticket, get_kyiv
from app.tickets.enums import TicketSource
from app.tickets.models import Ticket


PAGE_SIZE = 1000
TICKETS_URL = f'https://{settings.CC_HOST}/api/tickets/search'
TICKETS_PROGRESS_URL = f'https://{settings.CC_HOST}/api/ticket-progress/{{ticket_id}}'

MONTH_MAP = {
    'Січень': 1,
    'Лютий': 2,
    'Березень': 3,
    'Квітень': 4,
    'Травень': 5,
    'Червень': 6,
    'Липень': 7,
    'Серпень': 8,
    'Вересень': 9,
    'Жовнеть': 10,
    'Листопад': 11,
    'Грудень': 12,
}

STREET_CSV_MAP = {
    'comment': "Коментар",
    'district': 'Адміністративний район',
    'document': "Документ про присвоєння найменування об'єкта",
    'document_date': "Дата документу про присвоєння найменування об'єкта",
    'document_title': "Заголовок документу про присвоєння найменування об'єкта",
    'document_number': "Номер документу про присвоєння найменування об'єкта",
    'category': "Категорія (тип) об'єкта",
    'old_category': "Колишня категорія (тип) об'єкта",
    'old_name': "Колишнє найменування об'єкта",
    'name': "Повне офіційне найменування об'єкта",
    'id': "Унікальний цифровий код об'єкта",
}

logger = logging.getLogger(__name__)

group = AppGroup('tickets')


def _fetch_tickets_page(
    page_num: int = 1,
    districts_ids: Optional[List[str]] = None,
    tickets_ids: Optional[List[str]] = None,
):
    logger.info(f'Fetch page {page_num}')

    response = requests.get(
        url=TICKETS_URL,
        params={
            'per_page': PAGE_SIZE,
            'page': page_num,
            'include[]': ['rate', 'files'],
            'ticket_ids[]': tickets_ids,
            'district_ids[]': districts_ids,
        },
    )
    rate_limiting = response.headers.get('X-RateLimit-Remaining')
    if rate_limiting and int(rate_limiting) < 2:
        sleep(60)
    response.raise_for_status()
    return response.json()


def _fetch_last_ticket_page(districts_ids: Optional[List[str]] = None):
    page = _fetch_tickets_page(districts_ids=districts_ids)
    total_pages = page['meta']['pagination']['total_pages']
    return _fetch_tickets_page(page_num=total_pages, districts_ids=districts_ids)


def _fetch_last_processed_page(ticket_id: int, districts_ids: Optional[List[str]] = None):
    page_num = 1

    while True:
        page = _fetch_tickets_page(page_num, districts_ids=districts_ids)
        items = page['data']
        if not items:
            return page

        last, first = items[0], items[-1]
        logger.info(f'Fetching last page: {first["id"]} < {ticket_id} < {last["id"]}')
        if first['id'] <= ticket_id <= last['id']:
            return page

        page_num += 1


def _process_page_tickets(page, last_id: int):
    new_tickets: List[Ticket] = []

    kyiv = get_kyiv()

    for item in reversed(page['data']):
        if last_id and item['id'] <= last_id:
            continue
        ticket = Ticket(
            external_id=item['id'],
            number=item['number'],
            title=item['title'],
            text=item['description'],
            user_id=item['user_id'],
            status=item['status'],
            address=item['address'],
            work_taken_by=item['work_taken_by'],
            approx_done_date=item['approx_done_date'],
            created_at=item['created_at'],
            subject_id=item['subject']['id'],
            city_id=kyiv.id,
            source=TicketSource.cc1551,
            meta=item,
        )
        new_tickets.append(ticket)

    db.session.bulk_save_objects(new_tickets)
    db.session.commit()


def _process_district_tickets_page(page, last_id: int, district_id: str):
    tickets_ids: List[str] = []
    for item in reversed(page['data']):
        if last_id and item['id'] <= last_id:
            continue
        tickets_ids.append(item['id'])
    (
        db.session.query(Ticket)
        .filter(Ticket.external_id.in_(tickets_ids))
        .update({'district_id': district_id}, synchronize_session=False)
    )
    db.session.commit()


def _fetch_ticket_progress(ticket_id: str):
    response = requests.get(url=TICKETS_PROGRESS_URL.format(ticket_id))
    response.raise_for_status()
    data = response.json()

    # Normalize data
    data: Dict = data['ticket_progress']
    data.pop('placeholders')
    result = []
    for key, items in data.items():
        month, year = key.split(' - ', maxsplit=2)
        for item in items:
            item['month'] = MONTH_MAP[month]
            item['year'] = int(year)
        result.extend(items)
    return result


@group.command()
def get_new_tickets():
    ticket = select_last_ticket()
    last_id: Optional[int] = ticket and int(ticket.external_id)

    if not ticket:
        page = _fetch_last_ticket_page()
    else:
        page = _fetch_last_processed_page(last_id)

    while True:
        _process_page_tickets(page, last_id)
        current_page: int = page['meta']['pagination']['current_page'] - 1
        if current_page <= 0:
            logger.info('Last page processed')
            break

        page = _fetch_tickets_page(current_page)

    get_districts_tickets()


def get_district_tickets(district_id: str):
    ticket = select_last_ticket(district_id)
    last_id: Optional[int] = ticket and int(ticket.external_id)

    if not ticket:
        page = _fetch_last_ticket_page([district_id])
    else:
        page = _fetch_last_processed_page(last_id, [district_id])

    while True:
        _process_district_tickets_page(page, last_id, district_id)
        current_page: int = page['meta']['pagination']['current_page'] - 1
        if current_page <= 0:
            logger.info(f'Last district {district_id} processed')
            return

        page = _fetch_tickets_page(current_page, districts_ids=[district_id])


def get_districts_tickets():
    logger.info('Getting tickets districts')

    for district in DISTRICTS:
        district_id = str(district['id'])
        get_district_tickets(district_id)


@group.command()
def create_buckets():
    storage.connection.make_bucket('photos')
