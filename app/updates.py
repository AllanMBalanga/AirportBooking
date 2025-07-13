from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import ClassEnum, FlightStatus

#accounts
class AccountPut(BaseModel):
    email: EmailStr
    password: str

class AccountPatch(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


#accounts info
class AccountsInfoPut(BaseModel):
    first_name: str
    last_name: str

class AccountsInfoPatch(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


#airports
class AirportPut(BaseModel):
    name: str
    country: str
    city: str

class AirportPatch(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


#class types
class ClassTypePut(BaseModel):
    type: ClassEnum

class ClassTypePatch(BaseModel):
    type: Optional[ClassEnum] = None


#bookings
class BookingPut(BaseModel):
    class_id: int
    from_id: int
    to_id: int
    departure_date: datetime
    return_date: Optional[datetime] = None

class BookingPatch(BaseModel):
    class_id: Optional[int] = None
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    departure_date: Optional[datetime] = None
    return_date: Optional[datetime] = None


#flights
class FlightPut(BaseModel):
    flight_number: str
    seat_number: str
    status: FlightStatus

class FlightPatch(BaseModel):
    flight_number: Optional[str] = None
    seat_number: Optional[str] = None
    status: Optional[FlightStatus] = None
