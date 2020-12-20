from datetime import date
from typing import Optional

from sqlalchemy.sql.functions import now

from app.extensions import db
from app.tickets.enums import TicketSource
from app.tickets.models import Ticket, Subject, City, District, TicketPhoto, TicketTag


def prepare_ticket(
    external_id=1,
    number='N-100',
    title='Test title',
    text='Test text',
    status='Test status',
    address='Test address',
    work_taken_by='Test executor',
    approx_done_date=None,
    created_at=None,
    subject_id=1,
    user_id='1',
    district_id=1,
    city_id='1',
    source=TicketSource.cc1551,
    meta=None,
) -> Ticket:
    ticket = Ticket(
        external_id=external_id,
        number=number,
        title=title,
        text=text,
        status=status,
        address=address,
        work_taken_by=work_taken_by,
        approx_done_date=approx_done_date or date(year=2020, day=22, month=11),
        created_at=created_at or now(),
        subject_id=subject_id,
        user_id=user_id,
        district_id=district_id,
        city_id=city_id,
        source=source,
        meta=meta or {},
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def prepare_city(id_: int = 1, name: str = 'Київ') -> City:
    city = City(id=id_, name=name)
    db.session.add(city)
    db.session.commit()
    return city


def prepare_ticket_tag(ticket_id: int, name: str) -> TicketTag:
    tag = TicketTag(ticket_id=ticket_id, name=name)
    db.session.add(tag)
    db.session.commit()
    return tag


def prepare_subject(id_: int = 1, name: str = 'Test subject') -> Subject:
    subject = Subject(id=id_, name=name)
    db.session.add(subject)
    db.session.commit()
    return subject


def prepare_photo(id_: Optional[str] = None, content_type: str = 'image/jpeg') -> TicketPhoto:
    photo = TicketPhoto(id=id_, content_type=content_type)
    db.session.add(photo)
    db.session.commit()
    return photo


def prepare_district(name: str = 'Test district') -> District:
    district = District(name=name)
    db.session.add(district)
    db.session.commit()
    return district
