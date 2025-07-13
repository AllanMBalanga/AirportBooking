from fastapi import APIRouter, status, HTTPException, Depends
from ..body import ClassType
from ..response import ClassTypeResponse
from ..updates import ClassTypePatch, ClassTypePut
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List
from ..status_codes import validate_class_exists
from ..queries import get_class_type_query

router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)


@router.get("/", response_model=List[ClassTypeResponse])
def get_all_airports(db: Session = Depends(get_db)):
    classes = db.query(models.ClassType).all()
    return classes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClassTypeResponse)
def create_airport(classes: ClassType, db: Session = Depends(get_db)):
    try:
        created_class = models.ClassType(**classes.dict())

        db.add(created_class)
        db.commit()
        db.refresh(created_class)
        return created_class
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{class_id}", response_model=ClassTypeResponse)
def get_airport(class_id: int, db: Session = Depends(get_db)):
    class_type = get_class_type_query(db, class_id).first()
    validate_class_exists(class_type, class_id)

    return class_type

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airport(class_id: int, db: Session = Depends(get_db)):
    try:
        class_query = get_class_type_query(db, class_id)
        existing_class = class_query.first()
        validate_class_exists(existing_class, class_id)

        class_query.delete(synchronize_session=False)
        db.commit()
        return

    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/{class_id}", response_model=ClassTypeResponse)
def put_airport(class_id: int, classes: ClassTypePut, db: Session = Depends(get_db)):
    try:
        class_query = get_class_type_query(db, class_id)
        existing_class = class_query.first()
        validate_class_exists(existing_class, class_id)

        class_query.update(classes.dict(), synchronize_session=False)
        db.commit()

        return class_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/{class_id}", response_model=ClassTypeResponse)
def patch_airport(class_id: int, classes: ClassTypePatch, db: Session = Depends(get_db)):
    try:
        class_query = get_class_type_query(db, class_id)
        existing_class = class_query.first()
        validate_class_exists(existing_class, class_id)

        class_query.update(classes.dict(exclude_unset=True), synchronize_session=False)
        db.commit()

        return class_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
