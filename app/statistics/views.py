from flask import Blueprint

from app.lib.utils import api_response
from app.statistics import db, schemas

blueprint = Blueprint("statistics", __name__, url_prefix="/api/stats")


@blueprint.route('/districts/tickets')
def get_districts_tickets():

    stat = db.get_districts_tickets_stat()
    data = schemas.districts_tickets.dumps(stat)
    return api_response(data)


@blueprint.route('/subjects/tickets')
def get_subjects_tickets():

    stat = db.get_subjects_tickets_stat()
    data = schemas.subjects_tickets.dumps(stat)
    return api_response(data)


@blueprint.route('/titles/tickets')
def get_titles_tickets():

    stat = db.get_titles_tickets_stat()
    data = schemas.titles_tickets.dumps(stat)
    return api_response(data)
