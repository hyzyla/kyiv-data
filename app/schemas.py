from typing import Tuple

from marshmallow import post_load, validate, validates, ValidationError

from app.enums import TicketSource, TicketStatus
from app.main import ma, db
from app.models import Ticket, District, Subject, City

CREATE_TICKET_STATUSES: Tuple[str, ...] = TicketStatus.get_values()


class PageSchema(ma.Schema):
    pages = ma.Integer(dump_to='num_pages', dump_only=True)
    page = ma.Integer(dump_only=True)
    per_page = ma.Integer(dump_to='per_page', dump_only=True)
    total = ma.Integer(dump_to='total_items', dump_only=True)


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
    work_taken_by = ma.auto_field()
    approx_done_date = ma.auto_field()
    created_at = ma.auto_field()
    subject_id = ma.auto_field()
    district_id = ma.auto_field()
    city_id = ma.auto_field()
    source = ma.auto_field()

    @post_load
    def _(self, data, **kwargs):
        return {**data, 'source': TicketSource(data['source']), 'meta': {}}


class CreateTicketSchema(ma.Schema):
    external_id = ma.Integer(required=True, validate=validate.Range(min=0), strict=True)
    number = ma.String(required=True, validate=validate.Length(max=100))
    title = ma.String(required=True, validate=validate.Length(max=1024))
    text = ma.String(required=True, validate=validate.Length(max=8192))
    status = ma.String(required=True, validate=validate.OneOf(CREATE_TICKET_STATUSES))
    address = ma.String(required=True, validate=validate.Length(max=1024))
    work_taken_by = ma.String(required=True, validate=validate.Length(max=1024))
    approx_done_date = ma.Date(required=True)
    subject_id = ma.Integer(required=True, validate=validate.Range(min=0), strict=True)
    district_id = ma.Integer(required=False, validate=validate.Range(min=0), strict=True)
    city_id = ma.Integer(required=True, validate=validate.Range(min=0), strict=True)

    @validates('subject_id')
    def validate_subject(self, subject_id: int, **kwargs):
        subject = db.session.query(Subject).get(subject_id)
        if subject is None:
            return ValidationError('Теми не знайдено')

    @validates('district_id')
    def validate_district(self, district_id: int, **kwargs):
        if district_id is None:
            return

        district = db.session.query(District).get(district_id)
        if district is None:
            return ValidationError('Район не знайдено')

    @validates('city_id')
    def validate_district(self, city_id: int, **kwargs):
        city = db.session.query(City).get(city_id)
        if city is None:
            return ValidationError('Місто не знайдено')

    @post_load
    def _(self, data, **kwargs):
        return {**data, 'source': TicketSource.api, 'meta': {}}


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
create_ticket_schema = CreateTicketSchema()
tickets_schema = TicketPageSchema()
districts_schema = DistrictSchema(many=True)
subjects_schema = SubjectSchema(many=True)
titles_schema = TitlesSchema(many=True)
cities_schema = CitySchema(many=True)
