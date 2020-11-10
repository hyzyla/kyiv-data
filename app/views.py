from flask import jsonify

from app.main import app, db
from app.models import Ticket
from app.schemas import tickets_schema
from app.utils import get_search_filters


@app.route("/")
def read_root():
    return jsonify({'world': 'OK!'})


@app.route('/api/search')
def search():
    filters = get_search_filters()
    tickets_page = (
        db.session
        .query(Ticket)
        .filter(*filters)
        .order_by(Ticket.external_id.desc())
        .paginate(error_out=False, max_per_page=10000)
    )
    return tickets_schema.dumps(tickets_page)
