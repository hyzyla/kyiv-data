from marshmallow import post_load, validate, validates, ValidationError
from marshmallow_enum import EnumField

from app.extensions import ma, db
from app.tickets.enums import TicketSource, TicketPriority, TicketStatus
from app.tickets.models import (
    Ticket, District, Subject, City, TicketLocation,
    TicketTag, TicketPhoto
)


class PageSchema(ma.Schema):
    pages = ma.Integer(dump_to='num_pages', dump_only=True)
    page = ma.Integer(dump_only=True)
    per_page = ma.Integer(dump_to='per_page', dump_only=True)
    total = ma.Integer(dump_to='total_items', dump_only=True)


class TicketLocationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TicketLocation

    lat = ma.auto_field()
    lng = ma.auto_field()


class TicketTagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TicketTag

    name = ma.auto_field()


class TicketPhotoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TicketPhoto

    id = ma.String()  # TODO: to soft UUID


class TicketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Ticket

    id = ma.auto_field()
    external_id = ma.auto_field()
    user_id = ma.auto_field()
    number = ma.auto_field()
    title = ma.auto_field()
    text = ma.auto_field()
    status = ma.auto_field()
    address = ma.auto_field()
    link = ma.auto_field()
    priority = EnumField(TicketPriority, by_value=True)
    location = ma.Nested(TicketLocationSchema)
    tags = ma.List(ma.Nested(TicketTagSchema))
    photos = ma.List(ma.Nested(TicketPhotoSchema))
    work_taken_by = ma.auto_field()
    approx_done_date = ma.auto_field()
    created_at = ma.auto_field()
    subject_id = ma.auto_field()
    district_id = ma.auto_field()
    city_id = ma.auto_field()
    source = EnumField(TicketStatus, by_value=True)

    @post_load
    def _(self, data, **kwargs):
        return {**data, 'meta': {}}


class CreateTicketSchema(ma.Schema):
    title = ma.String(required=False, validate=validate.Length(max=1024))
    subject_id = ma.Integer(required=False, validate=validate.Range(min=0), strict=True)
    text = ma.String(required=True, validate=validate.Length(max=8192))
    tags = ma.List(ma.Nested(TicketTagSchema), required=False)
    address = ma.String(required=True, validate=validate.Length(max=1024))
    location = ma.Nested(TicketLocationSchema, required=False)
    priority = EnumField(TicketPriority, by_value=True, required=False)
    link = ma.URL(required=False)
    photos = ma.List(ma.Nested(TicketPhotoSchema), required=False)
    district_id = ma.Integer(required=False, validate=validate.Range(min=0), strict=True)
    city_id = ma.Integer(required=False, validate=validate.Range(min=0), strict=True)

    @validates('subject_id')
    def validate_subject(self, subject_id: int, **kwargs):
        if subject_id is None:
            return

        subject = db.session.query(Subject).get(subject_id)
        if subject is None:
            return ValidationError('Теми не знайдено')

    @post_load
    def _(self, data, **kwargs):
        return {
            **data,
            'source': TicketSource.api,
            'meta': {},
            'status': TicketStatus.new.value,
        }


class TicketPageSchema(PageSchema):
    items = ma.Nested(TicketSchema, many=True, dump_only=True)


class DistrictSchema(ma.SQLAlchemySchema):
    class Meta:
        model = District

    id = ma.Integer()
    name = ma.String()
    tickets_count = ma.Integer()


class SubjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subject

    id = ma.Integer()
    name = ma.String()
    tickets_count = ma.Integer()


class CitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = City

    id = ma.Integer()
    name = ma.String()


class TitlesSchema(ma.Schema):
    title = ma.String(dump_only=True)
    tickets_count = ma.Integer(dump_only=True)


ticket_schema = TicketSchema()
ticket_photo_schema = TicketPhotoSchema()
create_ticket_schema = CreateTicketSchema()
tickets_schema = TicketPageSchema()
districts_schema = DistrictSchema(many=True)
subjects_schema = SubjectSchema(many=True)
titles_schema = TitlesSchema(many=True)
cities_schema = CitySchema(many=True)
tags_schema = TicketTagSchema(many=True)
