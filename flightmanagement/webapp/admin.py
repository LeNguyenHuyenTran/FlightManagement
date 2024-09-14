from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from webapp.models import Flight, FlightRoute, UserRole
from webapp import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime


class Authenticated(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


class MyFlightView(Authenticated):
    column_list = ['id', 'name', 'flight_route_id']
    column_searchable_list = ['id', 'name']
    column_editable_list = ['name']


class MyFlightRouteView(Authenticated):
    column_list = ['id', 'name', 'flights']
    column_searchable_list = ['id', 'name']


class MyStatsView(BaseView):
    @expose('/')
    def index(self):
        revenue_by_flight_route = dao.stats_revenue_by_flight_route(kw=request.args.get('kw'))
        revenue_by_flight_route_id = dao.stats_revenue_by_period_by_id(year=request.args.get('year',
                                                                       datetime.now().year),
                                                                       period=request.args.get('period', 'month'),
                                                                       flight_route_id=request.args.get('flight_route_id', None))
        return self.render('admin/stats.html', revenue_by_flight_route=revenue_by_flight_route,
                           revenue_by_flight_route_id=revenue_by_flight_route_id)

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_flights_by_flight_route()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app, name='Flight Manager Website', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(MyFlightRouteView(FlightRoute, db.session))
admin.add_view(MyFlightView(Flight, db.session))
admin.add_view(MyStatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
