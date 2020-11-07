from sqlalchemy import BigInteger, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import JSONB

from app.main import db


class Column(db.Column):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = Column(BigInteger, primary_key=True)

    # ID from contact center
    external_id = Column(BigInteger, index=True)
    number = Column(Text)
    title = Column(Text)
    text = Column(Text)
    status = Column(Text)
    address = Column(Text, nullable=True)
    work_taken_by = Column(Text)
    approx_done_date = Column(Date)
    created_at = Column(DateTime)
    subject_id = Column(Text)

    # All data saved in JSON
    meta = Column(JSONB)
