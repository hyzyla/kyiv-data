from typing import Optional

from app.main import db
from app.models import Ticket


def select_last_ticket() -> Optional[Ticket]:
    return (
        db.session.query(Ticket)
        .order_by(Ticket.external_id.desc())
        .first()
    )

