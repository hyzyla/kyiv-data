from flask import jsonify

from app.main import app, db
from app.models import Ticket, District, Subject
from app.schemas import tickets_schema, districts_schema, subjects_schema
from app.utils import get_search_filters


@app.route("/")
def read_root():
    return jsonify({'world': 'OK!'})


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
    districts = db.session.query(District).all()
    return districts_schema.dumps(districts)


@app.route('/api/subjects')
def get_subjects():
    districts = db.session.query(Subject).all()
    return subjects_schema.dumps(districts)
