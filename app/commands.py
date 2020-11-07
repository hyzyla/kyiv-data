import logging

from typing import Dict, List, Optional

import requests

from app.config import settings
from app.db import select_last_ticket
from app.main import app, db
from app.models import Ticket

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
    'Грудень': 12
}

logger = logging.getLogger(__name__)


def _fetch_tickets_page(page_num: int = 1):
    logger.info(f'Fetch page {page_num}')

    response = requests.get(
        url=TICKETS_URL,
        params={
            'per_page': PAGE_SIZE,
            'page': page_num,
            'include[]': ['rate', 'files'],
        }
    )
    response.raise_for_status()
    return response.json()


def _fetch_last_ticket_page():
    page = _fetch_tickets_page()
    total_pages = page['meta']['pagination']['total_pages']
    return _fetch_tickets_page(page_num=total_pages)


def _fetch_last_processed_page(ticket_id: int):
    page_num = 1

    while True:
        page = _fetch_tickets_page(page_num)
        items = page['data']
        if not items:
            raise ValueError()

        last, first = items[0], items[-1]
        logger.info(f'Fetching last page: {first["id"]} < {ticket_id} < {last["id"]}')
        if first['id'] <= ticket_id <= last['id']:
            return page

        page_num += 1


def _process_page_tickets(page, last_id: int):
    new_tickets: List[Ticket] = []
    for item in reversed(page['data']):
        if last_id and item['id'] <= last_id:
            continue
        ticket = Ticket(
            external_id=item['id'],
            number=item['number'],
            title=item['title'],
            text=item['description'],
            status=item['status'],
            address=item['address'],
            work_taken_by=item['work_taken_by'],
            approx_done_date=item['approx_done_date'],
            created_at=item['created_at'],
            subject_id=item['subject']['id'],
            meta=item,
        )
        new_tickets.append(ticket)

    db.session.bulk_save_objects(new_tickets)
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


@app.cli.command()
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
            return

        page = _fetch_tickets_page(current_page)


@app.cli.command()
def get_ticket_progress():
    ticket = select_last_ticket()
    progress = _fetch_ticket_progress(ticket.external_id)
    from pprint import pprint
    pprint(progress)

