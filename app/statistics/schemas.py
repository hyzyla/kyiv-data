from app.extensions import ma
from app.tickets.models import (
    District, Subject
)


class DistrictStatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = District

    id = ma.Integer()
    name = ma.String()
    tickets_count = ma.Integer()


class SubjectStatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subject

    id = ma.Integer()
    name = ma.String()
    tickets_count = ma.Integer()


class TitleStatSchema(ma.Schema):
    title = ma.String(dump_only=True)
    tickets_count = ma.Integer(dump_only=True)


districts_tickets = DistrictStatSchema(many=True)
subjects_tickets = SubjectStatSchema(many=True)
titles_tickets = TitleStatSchema(many=True)
