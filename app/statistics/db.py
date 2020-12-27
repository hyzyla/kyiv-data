from app.extensions import db
from app.tickets.models import Ticket, Subject, District


def get_titles_tickets_stat():
    return (
        db.session.query(Ticket.title, db.func.count(Ticket.id).label('tickets_count'))
        .select_from(Ticket)
        .filter(Ticket.title.isnot(None))
        .group_by(Ticket.title)
        .order_by(Ticket.title)
        .all()
    )


def get_subjects_tickets_stat():
    return (
        db.session.query()
        .add_columns(Subject.id, Subject.name, db.func.count(Ticket.id).label('tickets_count'))
        .select_from(Subject)
        .outerjoin(Ticket, Ticket.subject_id == Subject.id)
        .group_by(Subject.id)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )


def get_districts_tickets_stat():
    return (
        db.session.query()
        .add_columns(District.id, District.name, db.func.count(Ticket.id).label('tickets_count'))
        .select_from(District)
        .outerjoin(Ticket, Ticket.district_id == District.id)
        .group_by(District.id)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
