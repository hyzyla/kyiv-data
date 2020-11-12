from app.main import ma
from app.models import Ticket


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


class PageSchema(ma.Schema):
    pages = ma.Integer(dump_to='num_pages', dump_only=True)
    page = ma.Integer(dump_only=True)
    per_page = ma.Integer(dump_to='per_page', dump_only=True)
    total = ma.Integer(dump_to='total_items', dump_only=True)


class TicketPageSchema(PageSchema):
    items = ma.Nested(TicketSchema, many=True, dump_only=True)


tickets_schema = TicketPageSchema()
