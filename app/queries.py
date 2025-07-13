from . import models
from sqlalchemy.orm import Session

def get_account_query(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id)

def get_account_info_query(db: Session, account_id: int):
    return db.query(models.AccountInfo).filter(models.AccountInfo.account_id == account_id)

def get_airport_query(db: Session, airport_id: int):
    return db.query(models.Airport).filter(models.Airport.id == airport_id)

def get_class_type_query(db: Session, class_id: int):
    return db.query(models.ClassType).filter(models.ClassType.id == class_id)


#SELECT * FROM bookings
#JOIN accounts_info ON accounts_info.id = bookings.account_info_id
#WHERE accounts_info.account_id = account_id
#AND bookings.id = booking_id
def get_booking_for_account(db: Session, account_id: int, booking_id: int = None):
    if booking_id:
        return db.query(models.Booking).join(
            models.AccountInfo, models.AccountInfo.id == models.Booking.account_info_id
        ).filter(
            models.AccountInfo.account_id == account_id, 
            models.Booking.id == booking_id
        )
    else:
        return db.query(models.Booking).join(
            models.AccountInfo, models.AccountInfo.id == models.Booking.account_info_id
        ).filter(
            models.AccountInfo.account_id == account_id
        )


#SELECT * FROM flights 
#JOIN accounts_info ON accounts_info.account_id = flights.account_info
#WHERE accounts_info.account_id = account_id
#AND flights.booking_id = booking_id
#AND flights.id = flight_id
def get_flight_for_booking(db: Session, account_id: int, booking_id: int, flight_id: int = None):
    if flight_id:
        return db.query(models.Flight).join(
            models.AccountInfo, models.AccountInfo.id == models.Flight.account_info_id
        ).filter(
            models.AccountInfo.account_id == account_id,
            models.Flight.booking_id == booking_id,
            models.Flight.id == flight_id
        )
    
    else:
        return db.query(models.Flight).join(
            models.AccountInfo, models.AccountInfo.id == models.Flight.account_info_id
        ).filter(
            models.AccountInfo.account_id == account_id,
            models.Flight.booking_id == booking_id
        )

#db.query(models.AccountInfo).filter(models.AccountInfo.id == info_id, models.AccountInfo.account_id == account_id) - 2 info.py