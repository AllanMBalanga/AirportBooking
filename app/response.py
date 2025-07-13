from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import ClassEnum, FlightStatus


# NESTED RESPONSES

class AirportResponse(BaseModel):
    id: int
    name: str
    country: str
    city: str

    class Config:
        orm_mode = True


class ClassTypeResponse(BaseModel):
    id: int
    type: ClassEnum

    class Config:
        orm_mode = True


class FlightNested(BaseModel):
    id: int
    flight_number: str
    seat_number: str
    status: FlightStatus
    created_at: datetime

    class Config:
        orm_mode = True


class BookingNested(BaseModel):
    id: int
    departure_date: datetime
    return_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True


# MAIN RESPONSES

class FlightResponse(BaseModel):
    id: int
    flight_number: str
    seat_number: str
    status: FlightStatus
    created_at: datetime

    # Relationships
    account_info_id: int
    booking: BookingNested

    class Config:
        orm_mode = True


class BookingResponse(BaseModel):
    id: int
    departure_date: datetime
    return_date: Optional[datetime] = None
    created_at: datetime

    # Foreign key fields
    account_info_id: int
    class_id: int
    from_id: int
    to_id: int

    # Relationships
    class_type: Optional[ClassTypeResponse]
    from_airport: Optional[AirportResponse]
    to_airport: Optional[AirportResponse]
    flights: List[FlightNested] = []

    class Config:
        orm_mode = True


class AccountInfoResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    created_at: datetime

    # Relationships
    bookings: List[BookingResponse] = []
    flights: List[FlightNested] = []

    class Config:
        orm_mode = True


class AccountResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # Relationship
    account_info: Optional[AccountInfoResponse]

    class Config:
        orm_mode = True