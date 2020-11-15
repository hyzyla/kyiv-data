from flask import redirect

from app.main import app, db
from app.models import Ticket, District, Subject
from app.schemas import tickets_schema, districts_schema, subjects_schema, titles_schema
from app.utils import get_search_filters


@app.route("/")
def read_root():
    return redirect('/admin/ticket')


@app.route('/api/search')
def search():

    filters = get_search_filters()
    tickets_page = (
        db.session.query(Ticket)
        .filter(*filters)
        .order_by(Ticket.external_id.desc())
        .paginate(error_out=False, max_per_page=10000)
    )
    return tickets_schema.dumps(tickets_page)


@app.route('/api/districts')
def get_districts():
    # Do not optimize without any reason for that
    districts = (
        db.session.query()
        .add_columns(
            District.id,
            District.name,
            db.func.count(Ticket.id).label('tickets_count')
        )
        .select_from(District)
        .outerjoin(Ticket, Ticket.district_id == District.id)
        .group_by(District.id)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
    return districts_schema.dumps(districts)


@app.route('/api/subjects')
def get_subjects():
    subjects = (
        db.session.query()
        .add_columns(
            Subject.id,
            Subject.name,
            db.func.count(Ticket.id).label('tickets_count')
        )
        .select_from(Subject)
        .outerjoin(Ticket, Ticket.subject_id == Subject.id)
        .group_by(Subject.id)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
    return subjects_schema.dumps(subjects)


@app.route('/api/titles')
def get_titles():
    subjects = (
        db.session.query()
        .add_columns(
            Ticket.title,
            db.func.count(Ticket.id).label('tickets_count')
        )
        .select_from(Ticket)
        .group_by(Ticket.title)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
    return titles_schema.dumps(subjects)
