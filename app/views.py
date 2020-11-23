from http import HTTPStatus

from flask import redirect, jsonify

from app import utils, validators
from app.lib.errors import BaseError
from app.main import app, db
from app.models import Ticket, District, Subject, City
from app.schemas import (
    tickets_schema,
    districts_schema,
    subjects_schema,
    titles_schema,
    ticket_schema,
    cities_schema,
)
from app.utils import get_search_filters, login_required, api_response


@app.errorhandler(BaseError)
def handle_base_error(error: BaseError):
    response = jsonify(error.to_dict())
    response.status_code = error.code
    return response


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
    return api_response(tickets_schema.dumps(tickets_page))


@app.route('/api/districts')
def get_districts():
    # Do not optimize without any reason for that
    districts = (
        db.session.query()
        .add_columns(District.id, District.name, db.func.count(Ticket.id).label('tickets_count'))
        .select_from(District)
        .outerjoin(Ticket, Ticket.district_id == District.id)
        .group_by(District.id)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
    return api_response(districts_schema.dumps(districts))


@app.route('/api/subjects')
def get_subjects():
    subjects = (
        db.session.query()
        .add_columns(Subject.id, Subject.name, db.func.count(Ticket.id).label('tickets_count'))
        .select_from(Subject)
        .outerjoin(Ticket, Ticket.subject_id == Subject.id)
        .group_by(Subject.id)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
    return api_response(subjects_schema.dumps(subjects))


@app.route('/api/titles')
def get_titles():
    subjects = (
        db.session.query()
        .add_columns(Ticket.title, db.func.count(Ticket.id).label('tickets_count'))
        .select_from(Ticket)
        .group_by(Ticket.title)
        .order_by(db.text('tickets_count DESC'))
        .all()
    )
    return api_response(titles_schema.dumps(subjects))


@app.route('/api/cities')
def get_cities():
    cities = db.session.query(City).all()
    return api_response(cities_schema.dumps(cities))


@app.route('/api/tickets', methods=['POST'])
@login_required
def create_ticket():
    data = validators.create_ticket()
    ticket = utils.create_ticket(data)
    return api_response(ticket_schema.dumps(ticket), status=HTTPStatus.CREATED)


@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.id == ticket_id).first_or_404()
    return api_response(ticket_schema.dumps(ticket))


@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_note(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.id == ticket_id).first_or_404()
    db.session.delete(ticket)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT
