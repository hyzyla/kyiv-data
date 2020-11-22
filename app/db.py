from typing import Optional

from app.enums import TicketSource
from app.main import db
from app.models import Ticket, City


def select_last_ticket(
    district_id: Optional[str] = None,
    source: TicketSource = TicketSource.cc1551,
) -> Optional[Ticket]:

    query = db.session.query(Ticket).filter(Ticket.source == source)

    if district_id is not None:
        query = query.filter(Ticket.district_id == district_id)

    return query.order_by(Ticket.external_id.desc()).first()


def get_kyiv() -> City:
    return db.session.query(City).filter(City.name == 'Київ').first()
