from app.lib.types import DataDict
from app.lib.validators import validate_request_json
from app.schemas import create_ticket_schema


def create_ticket() -> DataDict:
    return validate_request_json(schema=create_ticket_schema)
