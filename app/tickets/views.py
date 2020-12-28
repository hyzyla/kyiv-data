import io
from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint, request, current_app
from flask import redirect

from app.extensions import db, storage
from app.lib.utils import api_response, gen_uuid
from app.tickets import validators, utils
from app.tickets.enums import TicketSource
from app.tickets.models import Ticket, District, Subject, TicketPhoto, TicketTag
from app.tickets.schemas import ticket_schema, ticket_photo_schema, tags_schema, \
    sources_schema
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
def get_districts_stat():
    # TODO: remove this API
    from app.statistics.schemas import districts_tickets as schema
    from app.statistics.db import get_districts_tickets_stat

    stat = get_districts_tickets_stat()
    return api_response(schema.dumps(stat))


@blueprint.route('/api/subjects')
def get_subjects_stat():
    # TODO: remove this api
    from app.statistics.schemas import subjects_tickets as schema
    from app.statistics.db import get_subjects_tickets_stat

    stat = get_subjects_tickets_stat()
    return api_response(schema.dumps(stat))


@blueprint.route('/api/titles')
def get_titles_stat():
    # TODO: remove this API
    from app.statistics.schemas import titles_tickets as schema
    from app.statistics.db import get_titles_tickets_stat

    stat = get_titles_tickets_stat()
    return api_response(schema.dumps(stat))


@blueprint.route('/api/tickets/titles')
def get_titles():
    titles = utils.get_tickets_titles()
    return api_response(titles_schema.dumps(titles))


@blueprint.route('/api/tickets/districts')
def get_districts():
    districts = utils.get_districts()
    return api_response(districts_schema.dumps(districts))


@blueprint.route('/api/tickets/subjects')
def get_subjects():
    subjects = utils.get_subjects()
    return api_response(subjects_schema.dumps(subjects))


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


@blueprint.route('/api/tickets/photos/<photo_id>', methods=['GET'])
def get_photo(photo_id):
    photo = db.session.query(TicketPhoto).filter(TicketPhoto.id == photo_id).first_or_404()
    data = storage.connection.get_object(
        bucket_name='photos',
        object_name=photo.id,
    )
    return current_app.response_class(
        response=data,
        status=HTTPStatus.OK,
        mimetype=photo.content_type,
    )


@blueprint.route('/api/tickets/photos', methods=['POST'])
@login_required
def upload_photo(ctx):
    file = request.get_data()

    # TODO: add validation for content type
    content_type = request.headers.get('Content-Type')
    photo = TicketPhoto(id=gen_uuid(), content_type=content_type)
    db.session.add(photo)
    storage.connection.put_object(
        bucket_name='photos',
        object_name=photo.id,
        data=io.BytesIO(file),
        length=len(file),
        content_type=content_type
    )
    db.session.commit()
    return api_response(ticket_photo_schema.dumps(photo))


@blueprint.route('/api/tickets/tags', methods=['GET'])
def get_tags():
    tags = db.session.query(TicketTag.name).group_by(TicketTag.name).all()
    return api_response(tags_schema.dumps(tags))


@blueprint.route('/api/tickets/sources', methods=['GET'])
def get_sources():
    data = [
        {'value': TicketSource.cc1551.value, 'name': '1551'},
        {'value': TicketSource.api.value, 'name': 'Офіс Трансформації'},
    ]
    return api_response(sources_schema.dumps(data))
