from http import HTTPStatus

from flask import current_app


def api_response(data: str, status: int = HTTPStatus.OK):
    return current_app.response_class(
        response=data,
        status=status,
        mimetype='application/json',
    )
