from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..body import Booking, TokenData
from .. import models
from ..response import BookingResponse
from ..updates import BookingPatch, BookingPut
from typing import List
from ..oauth2 import get_current_user
from ..status_codes import validate_account_exists, validate_account_ownership, validate_account_info_exists, validate_booking_exists
from ..queries import get_account_query, get_booking_for_account

router = APIRouter(
    prefix="/accounts/{account_id}/bookings",
    tags=["Bookings"]
)

@router.get("/", response_model=List[BookingResponse])
def get_bookings(account_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    validate_account_ownership(account_id, current_user.id)
    
    account = get_account_query(db, account_id).first()
    validate_account_exists(account, account_id)
    
    #select * from bookings 
    #JOIN accounts_info ON accounts_info.id = bookings.account_info_id 
    #JOIN accounts ON accounts.id = accounts_info.account_id 
    #WHERE accounts.id == account_id
    bookings = get_booking_for_account(db, account_id).all()

    return bookings

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookingResponse)
def create_booking(account_id: int, booking: Booking, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)

        #scalar - returns the first column on the first row
        #select id from accounts_info WHERE accounts_info.account_id = account_id
        account_info = db.query(models.AccountInfo.id).filter(models.AccountInfo.account_id == account_id).scalar()
        validate_account_info_exists(account_info)
        
        booking_data = booking.dict()
        booking_data["account_info_id"] = account_info

        created_booking = models.Booking(**booking_data)
        db.add(created_booking)
        db.commit()
        db.refresh(created_booking)

        return created_booking

    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{booking_id}", response_model=BookingResponse)
def get_one_booking(account_id: int, booking_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    validate_account_ownership(account_id, current_user.id)
    
    account = get_account_query(db, account_id).first()
    validate_account_exists(account, account_id)
    
    booking = get_booking_for_account(db, account_id, booking_id).first()
    validate_booking_exists(booking, booking_id)

    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(account_id: int, booking_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        booking = get_booking_for_account(db, account_id, booking_id).first()
        validate_booking_exists(booking, booking_id)
        
        db.delete(booking)
        db.commit()
        return
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{booking_id}", response_model=BookingResponse)
def put_booking(account_id: int, booking_id: int, booking: BookingPut, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        booking_query = get_booking_for_account(db, account_id, booking_id)
        existing_booking = booking_query.first()
        validate_booking_exists(existing_booking, booking_id)

        # Update fields manually
        for key, value in booking.dict().items():
            setattr(existing_booking, key, value)

        db.commit()
        db.refresh(existing_booking)  # refresh from DB to return updated version
        return existing_booking
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{booking_id}", response_model=BookingResponse)
def put_booking(account_id: int, booking_id: int, booking: BookingPatch, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)
        
        booking_query = get_booking_for_account(db, account_id, booking_id)
        existing_booking = booking_query.first()
        validate_booking_exists(existing_booking, booking_id)

        # Update fields manually
        for key, value in booking.dict(exclude_unset=True).items():
            setattr(existing_booking, key, value)

        db.commit()
        db.refresh(existing_booking)  # refresh from DB to return updated version
        return existing_booking
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    




        