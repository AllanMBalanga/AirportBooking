from fastapi import status, HTTPException

def exception(e):
    print(f"Request error {e}")
    raise HTTPException(status_code=500, detail=f"Something went wrong")

#check if account.id is the one that created the account before posting/deleting/updating
def validate_account_ownership(account_id: int, current_user_id: int):
    if account_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform this action"
        )

#check if account exists in database
def validate_account_exists(account, account_id: int = None):
    if not account:
        if account_id:
            detail = f"Account with id {account_id} was not found"
        else:
            detail = "Account was not found"
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )

def validate_account_info_exists(account_info, account_info_id: int = None):
    if not account_info:
        if account_info_id:
            detail = f"Account info with id {account_info_id} was not found"
        else:
            detail = "Account info was not found"
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )

#check if airport.id is in database
def validate_airport_exists(airprot, airport_id: int = None):
    if not airprot:
        if airport_id:
            detail = f"Airport with id {airport_id} was not found" 
        else:
            detail = "Airport was not found"

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )


#check if class exists in database
def validate_class_exists(class_type, class_id: int = None):
    if not class_type:
        if class_id:
            detail = f"Flight class with id {class_id} was not found"
        else:
            detail = "Flight class was not found"
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )

#check if booking exists in database
def validate_booking_exists(booking, booking_id: int = None):
    if not booking:
        if booking_id:
            detail = f"Booking with id {booking_id} was not found"
        else:
            detail = "Booking was not found"
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )

#check if flight exists in database
def validate_flight_exists(flight, flight_id: int = None):
    if not flight:
        if flight_id:
            detail = f"Flight with id {flight_id} was not found"
        else:
            detail = "Flight was not found"
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )


