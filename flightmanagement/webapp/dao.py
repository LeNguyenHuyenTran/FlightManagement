import hashlib
from webapp.models import Flight, Ticket, User, Airport, FlightRoute, Bill
from webapp import db, app
from sqlalchemy import func
from datetime import datetime


def count_flights_by_flight_route():
    return db.session.query(FlightRoute.id, FlightRoute.name,
                            func.count(Flight.id)).join(Flight, Flight.flight_route_id.__eq__(FlightRoute.id), isouter=True)\
                     .group_by(FlightRoute.id).all()


def stats_revenue_by_flight_route(kw=None):
    query = (db.session.query(FlightRoute.id, FlightRoute.name, func.sum(Ticket.price))
             .join(Flight, Flight.flight_route_id.__eq__(FlightRoute.id), isouter=True)
             .join(Ticket, Flight.id == Ticket.flight_id)
             .join(Bill, Ticket.bill_id == Bill.id))
    if kw:
        query = query.filter(FlightRoute.name.contains(kw))

    return query.group_by(FlightRoute.id).order_by(FlightRoute.id).all()


def stats_revenue_by_period(year=datetime.now().year, period='month'):
    query = db.session.query(func.extract(period, Bill.created_date),
                             func.sum(Ticket.price))\
                     .join(Ticket, Ticket.bill_id.__eq__(Bill.id))\
                     .filter(func.extract('year', Bill.created_date).__eq__(year))

    return query.group_by(func.extract(period, Bill.created_date)).order_by(func.extract(period, Bill.created_date)).all()


def stats_revenue_by_period_by_id(year=datetime.now().year, period='month', flight_route_id=None):
    query = db.session.query(func.extract(period, Bill.created_date),
                             func.sum(Ticket.price)) \
                     .join(Ticket, Ticket.bill_id.__eq__(Bill.id))\
                     .filter(func.extract('year', Bill.created_date).__eq__(year))

    if flight_route_id:
        query = query.filter(Flight.flight_route_id == flight_route_id)

    return query.group_by(func.extract(period, Bill.created_date)).order_by(func.extract(period, Bill.created_date)).all()


def load_flights():
    return Flight.query.order_by(Flight.id).all()


def load_airports():
    return Airport.query.order_by(Airport.id).all()


def load_start_dates():
    return db.session.query(Flight.start_date).distinct().order_by(Flight.start_date).all()


def load_tickets():
    return Ticket.query.order_by(Ticket.id).all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf_8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(id):
    return User.query.get(id)


def add_user(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name.strip(), username=username.strip(), password=password)
    db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        print(stats_revenue_by_period_by_id(flight_route_id=4))
