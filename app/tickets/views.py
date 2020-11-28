from http import HTTPStatus

from flask import Blueprint
from flask import redirect

from app.extensions import db
from app.lib.utils import api_response
from app.tickets import validators, utils
from app.tickets.models import Ticket, District, Subject
from app.tickets.schemas import ticket_schema
from app.tickets.schemas import (
    tickets_schema,
    districts_schema,
    subjects_schema,
    titles_schema,
)
from app.tickets.utils import get_search_filters
from app.users.utils import login_required

blueprint = Blueprint("tickets", __name__, url_prefix="/")


@blueprint.route("/")
def read_root():
    return redirect('/admin/ticket')


@blueprint.route('/api/search')
def search():

    filters = get_search_filters()
    tickets_page = (
        db.session.query(Ticket)
        .filter(*filters)
        .order_by(Ticket.external_id.desc())
        .paginate(error_out=False, max_per_page=10000)
    )
    return api_response(tickets_schema.dumps(tickets_page))


@blueprint.route('/api/districts')
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


@blueprint.route('/api/subjects')
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


@blueprint.route('/api/titles')
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


@blueprint.route('/api/tickets', methods=['POST'])
@login_required
def create_ticket(ctx):
    data = validators.create_ticket()
    ticket = utils.create_ticket(data, ctx)
    return api_response(ticket_schema.dumps(ticket), status=HTTPStatus.OK)


@blueprint.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.id == ticket_id).first_or_404()
    return api_response(ticket_schema.dumps(ticket))


@blueprint.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_ticket(ctx, ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.id == ticket_id).first_or_404()
    db.session.delete(ticket)
    db.session.commit()
    return '', HTTPStatus.OK