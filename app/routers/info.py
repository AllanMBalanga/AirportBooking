from fastapi import APIRouter, status, HTTPException, Depends
from ..body import AccountInfo, TokenData
from ..response import AccountInfoResponse
from ..updates import AccountsInfoPut, AccountsInfoPatch
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models 
from ..oauth2 import get_current_user
from ..status_codes import validate_account_exists, validate_account_ownership, validate_account_info_exists
from ..queries import get_account_query, get_account_info_query

router = APIRouter(
    prefix="/accounts/{account_id}/info",
    tags=["Accounts Information"]
)

@router.get("/", response_model=AccountInfoResponse)
def get_account_info(account_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    validate_account_ownership(account_id, current_user.id)

    account = get_account_query(db, account_id).first()
    validate_account_exists(account, account_id)

    accounts_info = db.query(models.AccountInfo).filter(models.AccountInfo.account_id == account_id).first()
    return accounts_info

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountInfoResponse)
def create_account(account_id: int, account_info: AccountInfo, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)

        account_info_data = account_info.dict()
        account_info_data["account_id"] = account_id

        created_account_info = models.AccountInfo(**account_info_data)
        db.add(created_account_info)
        db.commit()
        db.refresh(created_account_info)
        return created_account_info
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)

        account_info_query = get_account_info_query(db, account_id)
        existing_account_info = account_info_query.first()
        validate_account_info_exists(existing_account_info)
        
        account_info_query.delete(synchronize_session=False)
        db.commit()
        return

    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/", response_model=AccountInfoResponse)
def put_account(account_id: int, account_info: AccountsInfoPut, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)

        account_info_query = get_account_info_query(db, account_id)
        existing_account_info = account_info_query.first()
        validate_account_info_exists(existing_account_info)
        
        account_info_query.update(account_info.dict(), synchronize_session=False)
        db.commit()

        return account_info_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.patch("/", response_model=AccountInfoResponse)
def patch_account(account_id: int, account_info: AccountsInfoPatch, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        validate_account_ownership(account_id, current_user.id)
        
        account = get_account_query(db, account_id).first()
        validate_account_exists(account, account_id)

        account_info_query = get_account_info_query(db, account_id)
        existing_account_info = account_info_query.first()
        validate_account_info_exists(existing_account_info)
        
        account_info_query.update(account_info.dict(exclude_unset=True), synchronize_session=False)
        db.commit()

        return account_info_query.first()
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
