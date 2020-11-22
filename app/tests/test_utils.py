from sqlalchemy.sql.functions import now

from app.enums import TicketSource
from app.main import db
from app.models import Ticket, City, Subject, District


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
        approx_done_date=approx_done_date or now(),
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


def prepare_city(name: str = 'Київ') -> City:
    city = City(name=name)
    db.session.add(city)
    db.session.commit()
    return city


def prepare_subject(name: str = 'Test subject') -> Subject:
    subject = Subject(name=name)
    db.session.add(subject)
    db.session.commit()
    return subject


def prepare_district(name: str = 'Test district') -> District:
    district = District(name=name)
    db.session.add(district)
    db.session.commit()
    return district
