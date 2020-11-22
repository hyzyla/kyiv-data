from app.lib.validators import validate_request_json
from app.schemas import ticket_schema, TicketSchema


def create_ticket() -> TicketSchema:
    return validate_request_json(schema=ticket_schema)
