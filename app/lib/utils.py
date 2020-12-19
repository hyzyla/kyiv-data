import os
import struct
import time
import uuid
from http import HTTPStatus

from flask import current_app


def api_response(data: str, status: int = HTTPStatus.OK):
    return current_app.response_class(
        response=data,
        status=status,
        mimetype='application/json',
    )


def gen_uuid() -> str:
    """Generate timestamped UUID.

    github.com/bitmario/uuid0
    """

    ts = time.time()
    tsi = int(ts * 10000)

    # pack as an 8-byte uint and drop the first 2 bytes
    t_bytes = struct.pack('>Q', tsi)[2:]

    r_bytes = os.urandom(10)

    return str(uuid.UUID(bytes=t_bytes + r_bytes))
