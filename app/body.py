from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime
from .models import ClassEnum, FlightStatus

class Account(BaseModel):
    email: EmailStr
    password: str

class AccountInfo(BaseModel):
    first_name: str
    last_name: str

class Airport(BaseModel):
    name: str
    country: str
    city: str

class ClassType(BaseModel):
    type: ClassEnum

class Booking(BaseModel):
    class_id: int
    from_id: int
    to_id: int
    departure_date: datetime
    return_date: Optional[datetime] = None

class Flight(BaseModel):
    flight_number: str
    seat_number: str
    status: FlightStatus

#Token
class Token(BaseModel):
    access_token: str
    token_type: str
    account_id: int
   
class TokenData(BaseModel):
    id: Optional[int] = None