from typing import Optional

from app.main import db
from app.models import Ticket


def select_last_ticket(district_id: Optional[str] = None) -> Optional[Ticket]:
    query = db.session.query(Ticket)
    if district_id is not None:
        query = query.filter(Ticket.district_id == district_id)

    return query.order_by(Ticket.external_id.desc()).first()
