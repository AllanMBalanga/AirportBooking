from fastapi import APIRouter, status, HTTPException, Depends
from ..body import Airport
from ..response import AirportResponse
from ..updates import AirportPatch, AirportPut
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List
from ..status_codes import validate_airport_exists
from ..queries import get_airport_query

router = APIRouter(
    prefix="/airports",
    tags=["Airports"]
)


@router.get("/", response_model=List[AirportResponse])
def get_all_airports(db: Session = Depends(get_db)):
    airports = db.query(models.Airport).all()
    return airports

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AirportResponse)
def create_airport(airport: Airport, db: Session = Depends(get_db)):
    try:
        created_airport = models.Airport(**airport.dict())

        db.add(created_airport)
        db.commit()
        db.refresh(created_airport)
        return created_airport
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{airport_id}", response_model=AirportResponse)
def get_airport(airport_id: int, db: Session = Depends(get_db)):
    airport = get_airport_query(db, airport_id).first()
    validate_airport_exists(airport, airport_id)

    return airport

@router.delete("/{airport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    try:
        airport_query = get_airport_query(db, airport_id)
        existing_airport = airport_query.first()
        validate_airport_exists(existing_airport, airport_id)

        airport_query.delete(synchronize_session=False)
        db.commit()
        return

    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        db.rollback()
        print(f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/{airport_id}", response_model=AirportResponse)
def put_airport(airport_id: int, airport: AirportPut, db: Session = Depends(get_db)):
    try:
        airport_query = get_airport_query(db, airport_id)
        existing_airport = airport_query.first()
        validate_airport_exists(existing_airport, airport_id)

        airport_query.update(airport.dict(), synchronize_session=False)
        db.commit()

        return airport_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/{airport_id}", response_model=AirportResponse)
def patch_airport(airport_id: int, airport: AirportPatch, db: Session = Depends(get_db)):
    try:
        airport_query = get_airport_query(db, airport_id)
        existing_airport = airport_query.first()
        validate_airport_exists(existing_airport, airport_id)

        airport_query.update(airport.dict(exclude_unset=True), synchronize_session=False)
        db.commit()

        return airport_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
