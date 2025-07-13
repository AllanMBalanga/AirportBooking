from fastapi import APIRouter, status, HTTPException, Depends
from ..body import Account, TokenData
from ..response import AccountResponse
from ..updates import AccountPatch, AccountPut
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..utils import hash
from typing import List
from ..oauth2 import get_current_user
from ..status_codes import validate_account_exists, validate_account_ownership
from ..queries import get_account_query

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.get("/", response_model=List[AccountResponse])
def get_all_accounts(db: Session = Depends(get_db)):
    accounts = db.query(models.Account).all()
    return accounts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountResponse)
def create_account(account: Account, db: Session = Depends(get_db)):
    try:
        account.password = hash(account.password)

        created_account = models.Account(**account.dict())
        db.add(created_account)
        db.commit()
        db.refresh(created_account)
        return created_account
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    validate_account_ownership(account_id, current_user.id)

    account = get_account_query(db, account_id).first()
    validate_account_exists(account, account_id)
    
    return account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account_query = get_account_query(db, account_id)
        existing_account = account_query.first()
        validate_account_exists(existing_account, account_id)

        account_query.delete(synchronize_session=False)
        db.commit()
        return

    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/{account_id}", response_model=AccountResponse)
def put_account(account_id: int, account: AccountPut, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account_query = get_account_query(db, account_id)
        existing_account = account_query.first()
        validate_account_exists(existing_account, account_id)

        account.password = hash(account.password)

        account_query.update(account.dict(), synchronize_session=False)
        db.commit()

        return account_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/{account_id}", response_model=AccountResponse)
def patch_account(account_id: int, account: AccountPatch, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account_query = get_account_query(db, account_id)
        existing_account = account_query.first()
        validate_account_exists(existing_account, account_id)

        if account.password:
            account.password = hash(account.password)
            
        account_query.update(account.dict(exclude_unset=True), synchronize_session=False)
        db.commit()

        return account_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
