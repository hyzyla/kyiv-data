from flask_admin.contrib.sqla import ModelView

from app.extensions import admin, db
from app.tickets.models import Ticket, District, Subject


class ReadOnlyView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    can_set_page_size = True
    can_view_details = True


class TicketView(ReadOnlyView):
    column_list = ('external_id', 'title', 'work_taken_by')
    column_filters = ('external_id', 'title', 'work_taken_by')


class DistrictView(ReadOnlyView):
    column_list = ('id', 'name')


class SubjectView(ReadOnlyView):
    column_list = ('id', 'name')


class CityView(ReadOnlyView):
    column_list = ('id', 'name')


ticket_view = TicketView(Ticket, db.session)
district_view = DistrictView(District, db.session)
subject_view = SubjectView(Subject, db.session)
