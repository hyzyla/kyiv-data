from flask_admin.contrib.sqla import ModelView

from app.main import admin, db
from app.models import Ticket, District, Subject, City


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


admin.add_view(TicketView(Ticket, db.session))
admin.add_view(DistrictView(District, db.session))
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(CityView(City, db.session))
