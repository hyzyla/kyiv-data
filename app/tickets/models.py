from sqlalchemy import BigInteger, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db
from app.lib.db import SoftEnum
from app.tickets.enums import TicketSource


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(BigInteger, primary_key=True)

    # ID from contact center
    external_id = db.Column(BigInteger, nullable=False, index=True)
    number = db.Column(Text, nullable=False)
    title = db.Column(Text, nullable=False, index=True)
    text = db.Column(Text, nullable=False)
    status = db.Column(Text, nullable=False)
    address = db.Column(Text)
    work_taken_by = db.Column(Text, nullable=False)
    approx_done_date = db.Column(Date, nullable=False)
    created_at = db.Column(DateTime, nullable=False)
    subject_id = db.Column(BigInteger, nullable=False, index=True)
    user_id = db.Column(Text, nullable=False)

    district_id = db.Column(BigInteger, index=True)
    city_id = db.Column(db.ForeignKey('cities.id'), nullable=False)
    city = db.relationship('City')

    source = db.Column(SoftEnum(TicketSource), nullable=False)

    # All data saved in JSON
    meta = db.Column(JSONB, nullable=False)


class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(BigInteger, primary_key=True)
    name = db.Column(Text, nullable=False)


class City(db.Model):

    __tablename__ = 'cities'

    id = db.Column(BigInteger, primary_key=True)
    name = db.Column(Text, nullable=False)


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(BigInteger, primary_key=True)
    name = db.Column(Text, nullable=False)

