from datetime import datetime

from sqlalchemy import BigInteger, Text, DateTime, Date, Float
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.extensions import db
from app.lib.utils import gen_uuid
from app.tickets.enums import TicketSource, TicketPriority


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(BigInteger, primary_key=True)

    # ID and number from contact center
    external_id = db.Column(BigInteger, index=True)
    number = db.Column(Text)

    title = db.Column(Text, nullable=False, index=True)
    text = db.Column(Text, nullable=False)
    status = db.Column(Text, nullable=False)
    address = db.Column(Text)
    priority = db.Column(db.Enum(TicketPriority, native_enum=False, length=100))
    link = db.Column(Text)
    work_taken_by = db.Column(Text)
    approx_done_date = db.Column(Date)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    subject_id = db.Column(BigInteger, nullable=False, index=True)
    user_id = db.Column(Text, nullable=False)

    district_id = db.Column(BigInteger, index=True)
    city_id = db.Column(BigInteger, nullable=False)

    source = db.Column(db.Enum(TicketSource, native_enum=False, length=100))

    location = db.relationship('TicketLocation', uselist=False)
    tags = db.relationship('TicketTag', uselist=True)
    photos = db.relationship('TicketPhoto', uselist=True)

    # All data saved in JSON
    meta = db.Column(JSONB, nullable=False)


class TicketLocation(db.Model):
    id = db.Column(UUID, primary_key=True, default=gen_uuid)
    lat = db.Column(Float, nullable=False)
    lng = db.Column(Float, nullable=False)
    ticket_id = db.Column(db.ForeignKey('tickets.id'), unique=True)


class TicketTag(db.Model):
    id = db.Column(UUID, primary_key=True, default=gen_uuid)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    ticket_id = db.Column(db.ForeignKey('tickets.id'))


class TicketPhoto(db.Model):
    __tablename__ = 'tickets_photos'

    id = db.Column(UUID, primary_key=True, default=gen_uuid)
    ticket_id = db.Column(db.ForeignKey('tickets.id'), nullable=True)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)


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
