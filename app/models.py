from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Enum, Float, CheckConstraint, UniqueConstraint, null
from sqlalchemy.sql.expression import text
import enum
from sqlalchemy.orm import relationship

#CREATE TABLE

#signup or login
#accounts/{account_id}/info
#airports
#classes
#accounts/{account_id}/bookings
#accounts_info/{account_info_id}/bookings/{booking_id}/flights

#accounts/{account_id}/info/bookings
#select * from bookings JOIN accounts_info ON accounts_info.id = bookings.account_info_id JOIN accounts ON accounts.id = accounts_info.account_id WHERE accounts.id == account_id
class ClassEnum(enum.Enum):
    economy = "economy"
    premium = "premium"
    business = "business"
    first = "first"

class FlightStatus(enum.Enum):
    pending = "pending"
    boarding = "boarding"
    on_time = "on_time"
    delayed = "delayed"
    cancelled = "cancelled"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    account_info = relationship("AccountInfo", back_populates="account", uselist=False, cascade="all, delete")

class AccountInfo(Base):
    __tablename__ = "accounts_info"

    id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    account = relationship("Account", back_populates="account_info")
    bookings = relationship("Booking", back_populates="account_info", cascade="all, delete")
    flights = relationship("Flight", back_populates="account_info", cascade="all, delete")

class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), nullable=False)
    country = Column(String(32), nullable=False)
    city = Column(String(32), nullable=False)

    departures = relationship("Booking", back_populates="from_airport", foreign_keys="Booking.from_id")
    arrivals = relationship("Booking", back_populates="to_airport", foreign_keys="Booking.to_id")


class ClassType(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum(ClassEnum, name="type_name", create_constraint=True), nullable=False, unique=True)

    bookings = relationship("Booking", back_populates="class_type")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, nullable=False)
    account_info_id = Column(ForeignKey("accounts_info.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    class_id = Column(ForeignKey("classes.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    from_id = Column(ForeignKey("airports.id"), nullable=False)
    to_id = Column(ForeignKey("airports.id"), nullable=False)
    departure_date = Column(TIMESTAMP(timezone=True), nullable=False)
    return_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    __table_args__ = (
        CheckConstraint('from_id <> to_id', name='different_locations'),
    )

    account_info = relationship("AccountInfo", back_populates="bookings")
    class_type = relationship("ClassType", back_populates="bookings")
    from_airport = relationship("Airport", foreign_keys=[from_id], back_populates="departures")
    to_airport = relationship("Airport", foreign_keys=[to_id], back_populates="arrivals")
    flights = relationship("Flight", back_populates="booking", cascade="all, delete")

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, nullable=False)
    booking_id = Column(ForeignKey("bookings.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    account_info_id = Column(ForeignKey("accounts_info.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    flight_number = Column(String(32), nullable=False)
    seat_number = Column(String(32), nullable=False)
    status = Column(Enum(FlightStatus, name="flight_status", create_constraint=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    booking = relationship("Booking", back_populates="flights")
    account_info = relationship("AccountInfo", back_populates="flights")
