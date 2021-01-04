from flask import Blueprint

from app.lib.utils import api_response
from app.statistics import db, schemas
from app.tickets.utils import get_search_filters

blueprint = Blueprint("statistics", __name__, url_prefix="/api/stats")


@blueprint.route('/districts/tickets')
def get_districts_tickets():
    filters = get_search_filters()
    stat = db.get_districts_tickets_stat(filters=filters)
    data = schemas.districts_tickets.dumps(stat)
    return api_response(data)


@blueprint.route('/subjects/tickets')
def get_subjects_tickets():
    filters = get_search_filters()
    stat = db.get_subjects_tickets_stat(filters=filters)
    data = schemas.subjects_tickets.dumps(stat)
    return api_response(data)


@blueprint.route('/titles/tickets')
def get_titles_tickets():
    filters = get_search_filters()
    stat = db.get_titles_tickets_stat(filters=filters)
    data = schemas.titles_tickets.dumps(stat)
    return api_response(data)
