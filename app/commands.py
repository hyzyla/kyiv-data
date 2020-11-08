import logging
import csv
import re
from time import sleep

import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import insert as pg_insert

from typing import Dict, List, Optional

import requests

from app.config import settings
from app.constants import DISTRICTS
from app.db import select_last_ticket
from app.main import app, db
from app.models import Ticket, Street

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
    if int(response.headers['X-RateLimit-Remaining']) < 2:
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


def _process_district_tickets_page(page, last_id: int, district_id: str):
    tickets_ids: List[str] = []
    for item in reversed(page['data']):
        if last_id and item['id'] <= last_id:
            continue
        tickets_ids.append(item['id'])
    (
        db.session
        .query(Ticket)
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


@app.cli.command()
def get_districts_tickets():
    logger.info('Getting tickets districts')

    for district in DISTRICTS:
        district_id = str(district['id'])
        get_district_tickets(district_id)


@app.cli.command()
def get_ticket_progress():
    ticket = select_last_ticket()
    progress = _fetch_ticket_progress(ticket.external_id)
    from pprint import pprint

    pprint(progress)


@app.cli.command()
def load_streets_data():
    streets = []
    with open('data/streets.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            data = {}
            for key, name in STREET_CSV_MAP.items():
                value = line[name]
                value = '' if value == '-' else value
                data[key] = value or None
            streets.append(data)

    statement = pg_insert(Street).values(streets)
    statement = statement.on_conflict_do_update(
        constraint='streets_pkey',
        set_={
            'name': sa.func.trim(statement.excluded.name),
            'category': statement.excluded.category,
            'district': statement.excluded.district,
            'document': statement.excluded.document,
            'document_date': statement.excluded.document_date,
            'document_title': statement.excluded.document_title,
            'document_number': statement.excluded.document_number,
            'old_category': statement.excluded.old_category,
            'old_name': statement.excluded.old_name,
            'comment': statement.excluded.comment,
        },
    )
    db.session.execute(statement)
    db.session.commit()


def split_address(address: str):
    address = address.lower()
    cyrillic_re = r'[а-яА-ЯЇїІіЄєҐґ’\d\w\"|\'|\.]'
    name_re = fr'({cyrillic_re}({cyrillic_re}|-|\s)+{cyrillic_re})'
    type_re = fr'(просп.|вул.|Вул.|пл.|пров.|бульв.|шосе|наб.|дорога|туп.|узвіз|проїзд)'
    old_re = fr'({name_re}\s*(\,\s*{name_re}\s*)*\))'
    number_re = fr'.*'
    pattern_re = (
        fr'^'  # World start
        fr'('
        fr'((?P<type_l>{type_re})\s*((?P<name_l>{name_re})\s*(?P<old_l>\{old_re}?))|'
        fr'(((?P<name_r>{name_re})\s*(?P<old_r>\{old_re}?)\s*(?P<type_r>{type_re}))\s*'
        fr')'
        fr'\,\s*'
        fr'{number_re}'  # building number
        fr'$'  # Word end
    )

    r = re.compile(pattern_re, re.IGNORECASE)
    result = [m.groupdict() for m in r.finditer(address)]
    if len(result) != 1:
        raise ValueError(address)
    item = result[0]
    b = {
        'type': item['type_l'] or item['type_r'],
        'name': item['name_l'] or item['name_r'],
        'old': item['old_l'] or item['old_r'],
    }
    print(b)


@app.cli.command()
def split_address():
    tickets = db.session.query(Ticket).filter(Ticket.address.isnot(None)).all()
    for ticket in tickets:
        split_address(ticket.address)
