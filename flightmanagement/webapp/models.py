from webapp import db, app
from sqlalchemy import Column, String, ForeignKey, Float, Enum, DateTime, Integer, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import enum


class UserRole(enum.Enum):
    CUSTOMER = "Khách hàng"
    EMPLOYEE = "Nhân viên bán vé"
    ADMIN = "Quản trị viên"


class GenderEnum(enum.Enum):
    MALE = 'Nam'
    FEMALE = 'Nữ'
    OTHER = 'Khác'


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Airport(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(100), nullable=False, unique=True)
    stop_by_airports = relationship('StopByAirport', backref='airport', lazy=True)
    start_flight_routes = relationship('FlightRoute',
                                       backref='startairport', lazy=True, foreign_keys='FlightRoute.start_airport_id')
    end_flight_routes = relationship('FlightRoute',
                                     backref='endairport', lazy=True, foreign_keys='FlightRoute.end_airport_id')

    def __str__(self):
        return self.name


class Plane(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    flights = relationship('Flight', backref='plane', lazy=True)

    def __str__(self):
        return self.name


class FlightRoute(BaseModel):
    name = Column(String(100), nullable=False)
    start_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    end_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    flights = relationship('Flight', backref='flightroute', lazy=True)

    def __str__(self):
        return self.startairport.name + '-' + self.endairport.name


class Flight(BaseModel):
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(Float)
    is_active = Column(Boolean, default=False)
    image = Column(String(100))
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
    tickets = relationship('Ticket', backref='flight', lazy=True)
    stop_by_airports = relationship('StopByAirport', backref='flight', lazy=True)
    seats = relationship('Seat', backref='Flight', lazy=True)

    def __str__(self):
        return self.name


class StopByAirport(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True, nullable=False)
    airport_id = Column(Integer, ForeignKey(Airport.id), primary_key=True, nullable=False)
    time_stop = Column(Integer)
    note = Column(String(100))


class ClassTicket(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    benefit = Column(String(500))
    tickets = relationship('Ticket', backref='classticket', lazy=True)
    seats = relationship('Seat', backref='classTichket', lazy=True)

    def __str__(self):
        return self.name


class Seat(BaseModel):
    quantity = Column(Integer)
    class_ticket_id = Column(Integer, ForeignKey(ClassTicket.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)

    def __str__(self):
        return self.name


class Human(BaseModel):
    name = Column(String(50), nullable=False)
    phone = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    birth_day = Column(DateTime)
    gender = Column(Enum(GenderEnum), default=GenderEnum.MALE)


class User(Human, UserMixin):
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    bills = relationship('Bill', backref='employee', lazy=True, foreign_keys='Bill.payer_id')
    tickets = relationship('Ticket', backref='customer', lazy=True, foreign_keys='Ticket.user_id')


class Bill(BaseModel):
    payer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    total_bill = Column(Float, default=0)
    is_paid = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now())
    tickets = relationship('Ticket', backref='Bill', lazy=False)


class Ticket(BaseModel):
    booked_date = Column(DateTime, default=datetime.now())
    price = Column(Float, nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)
    class_ticket_id = Column(Integer, ForeignKey(ClassTicket.id), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)


class Regulations(BaseModel):
    content = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        # sb1 = Airport(name="Sân bay Quốc tế Tân Sơn Nhất", address="TP. Hồ Chí Minh")
        # sb2 = Airport(name="Sân bay Rạch Giá", address="Rạch Giá, Kiên Giang")
        # sb3 = Airport(name="Sân bay Điện Biên Phủ", address="Điện Biên")
        # sb4 = Airport(name="Sân bay Quốc tế Nội Bài", address="Hà Nội")
        # sb5 = Airport(name="Sân bay Quốc tế Cần Thơ", address="Cần Thơ")
        # sb6 = Airport(name="Sân bay Quốc tế Cam Ranh", address="Khánh Hòa")
        # sb7 = Airport(name="Sân bay Quốc tế Cát Bi", address="Hải Phòng")
        # sb8 = Airport(name="Sân bay Cà Mau", address="Cà Mau")
        # sb9 = Airport(name="Sân bay Quốc tế Phú Quốc", address="Phú Quốc, Kiên Giang")
        # sb10 = Airport(name="Sân bay Buôn Mê Thuột", address="Đắk Lắk")
        # db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10])
        # db.session.commit()

        # tb1 = FlightRoute(name="TP. Hồ Chí Minh - Hà Nội", start_airport_id=1, end_airport_id=4)
        # tb2 = FlightRoute(name="TP. Hồ Chí Minh - Cà Mau", start_airport_id=1, end_airport_id=8)
        # tb3 = FlightRoute(name="Hải Phòng - Hà Nội", start_airport_id=7, end_airport_id=4)
        # tb4 = FlightRoute(name="Khánh Hòa - Rạch Giá, Việt Nam", start_airport_id=6, end_airport_id=9)
        # tb5 = FlightRoute(name="Cần Thơ - Đắk Lắk", start_airport_id=5, end_airport_id=10)
        # tb6 = FlightRoute(name="Hải Phòng - TP. Hồ Chí Minh", start_airport_id=6, end_airport_id=1)
        # tb7 = FlightRoute(name="Phú Quốc, Kiên Giang - Điện Biên", start_airport_id=2, end_airport_id=3)
        # tb8 = FlightRoute(name="Hà Nội - Đắk Lắk", start_airport_id=4, end_airport_id=10)
        # db.session.add_all([tb1, tb2, tb3, tb4, tb5, tb6, tb7, tb8])
        # db.session.commit()
        #
        # mb1 = Plane(name="Máy bay 1")
        # mb2 = Plane(name="Máy bay 2")
        # mb3 = Plane(name="Máy bay 3")
        # mb4 = Plane(name="Máy bay 4")
        # mb5 = Plane(name="Máy bay 5")
        # mb6 = Plane(name="Máy bay 6")
        # mb7 = Plane(name="Máy bay 7")
        # mb8 = Plane(name="Máy bay 8")
        # mb9 = Plane(name="Máy bay 9")
        # mb10 = Plane(name="Máy bay 10")
        # db.session.add_all([mb1, mb2, mb3, mb4, mb5, mb6, mb7, mb8, mb9, mb10])
        # db.session.commit()
        #
        # cb1 = Flight(name='TP. Hồ Chí Minh - Cà Mau', start_date=datetime(2024, 5, 20, 8, 0),
        #              end_date=datetime(2024, 5, 20, 10, 0), price=1000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806191/Hue.jpg',
        #              plane_id=3, flight_route_id=2)
        # cb2 = Flight(name='TP. Hồ Chí Minh - Hà Nội', start_date=datetime(2024, 5, 20, 8, 0),
        #              end_date=datetime(2024, 5, 21, 5, 0), price=3000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806193/HaNoi.jpg',
        #              plane_id=1, flight_route_id=1)
        # cb3 = Flight(name='Kiên Giang - Điện Biên', start_date=datetime(2024, 6, 20, 7, 0),
        #              end_date=datetime(2024, 6, 20, 10, 0), price=2000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806193/HaNoi.jpg',
        #              plane_id=5, flight_route_id=7)
        # cb4 = Flight(name='Hải Phòng - Hà Nội', start_date=datetime(2024, 6, 21, 15, 30),
        #              end_date=datetime(2024, 6, 21, 20, 0), price=3000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806191/Hue.jpg',
        #              plane_id=4, flight_route_id=3)
        # cb5 = Flight(name='Khánh Hòa - Kiên Giang', start_date=datetime(2024, 10, 21, 18, 0),
        #              end_date=datetime(2024, 10, 21, 20, 0), price=1800000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806158/thanhphoHoChiMinh.jpg',
        #              plane_id=6, flight_route_id=4)
        # cb6 = Flight(name='Cần Thơ - Đắk Lắk', start_date=datetime(2024, 1, 22, 8, 0),
        #              end_date=datetime(2024, 1, 22, 15, 0), price=3000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806193/HaNoi.jpg',
        #              plane_id=2, flight_route_id=5)
        # cb7 = Flight(name='Hà Nội - Đắk Lắk', start_date=datetime(2024, 2, 20, 8, 0),
        #              end_date=datetime(2024, 2, 21, 1, 0), price=3000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806158/thanhphoHoChiMinh.jpg',
        #              plane_id=8, flight_route_id=8)
        # cb8 = Flight(name='Hải Phòng - TP. Hồ Chí Minh', start_date=datetime(2024, 5, 21, 8, 0),
        #              end_date=datetime(2024, 5, 21, 17, 0), price=3000000,
        #              image='https://res.cloudinary.com/dpnkep1km/image/upload/v1714806158/thanhphoHoChiMinh.jpg',
        #              plane_id=7, flight_route_id=6)
        # db.session.add_all([cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8])
        # db.session.commit()
        #
        # hv1 = ClassTicket(name="Hạng 1", price=2000000, benefit="Ngồi hàng ghế VIP và được phục vụ thức ăn, thức uống miễn phí")
        # hv2 = ClassTicket(name="Hạng 2", price=1000000, benefit="Miễn phí thức uống")
        # db.session.add_all([hv1, hv2])
        # db.session.commit()
        #
        # g1 = Seat(flight_id=1, class_ticket_id=1,quantity=25)
        # g2 = Seat(flight_id=1, class_ticket_id=2,quantity=75)
        # g3 = Seat(flight_id=2, class_ticket_id=1,quantity=25)
        # g4 = Seat(flight_id=2, class_ticket_id=2,quantity=75)
        # g5 = Seat(flight_id=3, class_ticket_id=1,quantity=25)
        # g6 = Seat(flight_id=3, class_ticket_id=2,quantity=75)
        # g7 = Seat(flight_id=4, class_ticket_id=1,quantity=25)
        # g8 = Seat(flight_id=4, class_ticket_id=2,quantity=75)
        # g9 = Seat(flight_id=5, class_ticket_id=1,quantity=25)
        # g10 = Seat(flight_id=5, class_ticket_id=2,quantity=75)
        # g11 = Seat(flight_id=6, class_ticket_id=1,quantity=25)
        # g12 = Seat(flight_id=6, class_ticket_id=2,quantity=75)
        # g13 = Seat(flight_id=7, class_ticket_id=1,quantity=25)
        # g14 = Seat(flight_id=7, class_ticket_id=2,quantity=75)
        # g15 = Seat(flight_id=8, class_ticket_id=1,quantity=25)
        # g16 = Seat(flight_id=8, class_ticket_id=2,quantity=75)
        # db.session.add_all([g1, g2, g3, g4, g5, g6, g7, g8,
        # g9, g10, g11, g12, g13, g14, g15, g16])
        # db.session.commit()
        #
        # import hashlib
        # u = User(name="admin", username="admin",
        # password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()), role=UserRole.ADMIN)
        # u1 = User(name="huyentran", username="huyentran",
        #           password=str(hashlib.md5("12345".encode('utf-8')).hexdigest()))
        # u2 = User(name="thuyngan", username="thuyngan",
        #           password=str(hashlib.md5("1234".encode('utf-8')).hexdigest()), role=UserRole.EMPLOYEE)
        # u3 = User(name="hy", username="hy",
        #           password=str(hashlib.md5("12345".encode('utf-8')).hexdigest()))
        # u4 = User(name="nhi", username="mannhi",
        #           password=str(hashlib.md5("12345".encode('utf-8')).hexdigest()))
        # u5 = User(name="mynhan", username="mynhan",
        #           password=str(hashlib.md5("12345".encode('utf-8')).hexdigest()))
        # u6 = User(name="baoan", username="baoan",
        #           password=str(hashlib.md5("12345".encode('utf-8')).hexdigest()))
        # u7 = User(name="luan", username="luan",
        #           password=str(hashlib.md5("12345".encode('utf-8')).hexdigest()))
        # u8 = User(name="nhaphuong", username="phuong",
        #           password=str(hashlib.md5("1234".encode('utf-8')).hexdigest()), role=UserRole.EMPLOYEE)
        # u9 = User(name="my", username="my",
        #           password=str(hashlib.md5("1234".encode('utf-8')).hexdigest()), role=UserRole.EMPLOYEE)
        # db.session.add_all([u, u1, u2, u3, u4, u5, u6, u7, u8, u9])
        # db.session.commit()
        #
        # s1 = StopByAirport(flight_id=1, airport_id=7, time_stop=30)
        # s2 = StopByAirport(flight_id=4, airport_id=3, time_stop=25)
        # s3 = StopByAirport(flight_id=2, airport_id=5, time_stop=30)
        # s4 = StopByAirport(flight_id=3, airport_id=1, time_stop=25)
        # s5 = StopByAirport(flight_id=4, airport_id=2, time_stop=20)
        # s6 = StopByAirport(flight_id=5, airport_id=2, time_stop=30)
        # s7 = StopByAirport(flight_id=6, airport_id=4, time_stop=20)
        # db.session.add_all([s1, s2, s3, s4, s5, s6, s7])
        # db.session.commit()
        #
        # b1 = Bill(payer_id=2, total_bill=8000000, is_paid=True)
        # b2 = Bill(payer_id=2, total_bill=11000000, is_paid=True)
        # b3 = Bill(payer_id=8, total_bill=6800000, is_paid=True)
        # b4 = Bill(payer_id=9, total_bill=12800000, is_paid=True)
        # db.session.add_all([b1, b2, b3, b4])
        # db.session.commit()
        #
        # v1 = Ticket(flight_id=1, class_ticket_id=1, user_id=1, bill_id=1, price=3000000)
        # v2 = Ticket(flight_id=1, class_ticket_id=2, user_id=1, bill_id=1, price=2000000)
        # v3 = Ticket(flight_id=1, class_ticket_id=1, user_id=1, bill_id=1, price=3000000)
        # v4 = Ticket(flight_id=3, class_ticket_id=2, user_id=5, bill_id=2, price=3000000)
        # v5 = Ticket(flight_id=2, class_ticket_id=2, user_id=5, bill_id=2, price=4000000)
        # v6 = Ticket(flight_id=4, class_ticket_id=2, user_id=5, bill_id=2, price=4000000)
        # v7 = Ticket(flight_id=5, class_ticket_id=2, user_id=4, bill_id=3, price=2800000)
        # v8 = Ticket(flight_id=6, class_ticket_id=2, user_id=4, bill_id=3, price=4000000)
        # v9 = Ticket(flight_id=5, class_ticket_id=1, user_id=6, bill_id=4, price=3800000)
        # v10 = Ticket(flight_id=7, class_ticket_id=2, user_id=6, bill_id=4, price=4000000)
        # v11 = Ticket(flight_id=8, class_ticket_id=1, user_id=6, bill_id=4, price=5000000)
        # db.session.add_all([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11])
        # db.session.commit()



