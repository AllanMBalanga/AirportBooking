from fastapi import APIRouter, status, HTTPException, Depends
from ..body import Flight, TokenData
from ..response import FlightResponse
from ..updates import FlightPut, FlightPatch
from ..database import get_db
from .. import models
from typing import List
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from ..status_codes import validate_account_exists, validate_account_ownership, validate_flight_exists, validate_booking_exists, validate_account_info_exists
from ..queries import get_account_query, get_booking_for_account, get_flight_for_booking

router = APIRouter(
    prefix="/accounts/{account_id}/bookings/{booking_id}/flights",
    tags=["Flights"]
)

@router.get("/", response_model=List[FlightResponse])
def get_flights(account_id: int, booking_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    validate_account_ownership(account_id, current_user.id)
    
    account = get_account_query(db, account_id).first()
    validate_account_exists(account, account_id)
    
    booking = get_booking_for_account(db, account_id, booking_id).first()
    validate_booking_exists(booking, booking_id)
    
    flights = get_flight_for_booking(db, account_id, booking_id).all()

    return flights

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FlightResponse)
def create_flight(account_id: int, booking_id: int, flight: Flight, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        account_info = db.query(models.AccountInfo.id).filter(models.AccountInfo.account_id == account_id).scalar()
        validate_account_info_exists(account_info)

        booking = get_booking_for_account(db, account_id, booking_id).first()
        validate_booking_exists(booking, booking_id)
        
        flight_data = flight.dict()
        flight_data["booking_id"] = booking_id
        flight_data["account_info_id"] = account_info

        created_flight = models.Flight(**flight_data)
        db.add(created_flight)
        db.commit()
        db.refresh(created_flight)

        return created_flight

    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight_by_id(account_id: int, booking_id: int, flight_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    validate_account_ownership(account_id, current_user.id)
        
    account = get_account_query(db, account_id).first()
    validate_account_exists(account, account_id)
    
    booking = get_booking_for_account(db, account_id, booking_id).first()
    validate_booking_exists(booking, booking_id)

    #SELECT * FROM flights
    #JOIN accounts_info ON accounts_info.account_info = models.Flight.account_info_id
    #WHERE accounts_info.account_id = account_id
    #AND flights.booking_id = booking_id
    #AND flights.id = flight_id
    flight = get_flight_for_booking(db, account_id, booking_id, flight_id).first()
    validate_flight_exists(flight, flight_id)
    
    return flight

@router.delete("/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight(account_id: int, booking_id: int, flight_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        booking = get_booking_for_account(db, account_id, booking_id).first()
        validate_booking_exists(booking, booking_id)
        
        flight = get_flight_for_booking(db, account_id, booking_id, flight_id).first()
        validate_flight_exists(flight, flight_id)
        
        db.delete(flight)
        db.commit()
        return

    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/{flight_id}", response_model=FlightResponse)
def put_flight(account_id: int, booking_id: int, flight_id: int, flight: FlightPut, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        booking = get_booking_for_account(db, account_id, booking_id).first()
        validate_booking_exists(booking, booking_id)
        
        existing_flight = get_flight_for_booking(db, account_id, booking_id, flight_id).first()
        validate_flight_exists(existing_flight, flight_id)
        
        # Update fields manually
        for key, value in flight.dict().items():
            setattr(existing_flight, key, value)

        db.commit()
        db.refresh(existing_flight)
        return existing_flight
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.patch("/{flight_id}", response_model=FlightResponse)
def put_flight(account_id: int, booking_id: int, flight_id: int, flight: FlightPatch, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        booking = get_booking_for_account(db, account_id, booking_id).first()
        validate_booking_exists(booking, booking_id)
        
        existing_flight = get_flight_for_booking(db, account_id, booking_id, flight_id).first()
        validate_flight_exists(existing_flight, flight_id)
        
        # Update fields manually
        for key, value in flight.dict(exclude_unset=True).items():
            setattr(existing_flight, key, value)

        db.commit()
        db.refresh(existing_flight)
        return existing_flight
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        