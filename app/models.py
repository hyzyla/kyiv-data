from sqlalchemy import BigInteger, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.main import db


class Column(db.Column):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = Column(BigInteger, primary_key=True)
    number = Column(Text)
    text = Column(Text)
    # ID from contact center
    external_id = Column(BigInteger, index=True)
    meta = Column(JSONB)
