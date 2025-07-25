from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..body import Token
from .. import models, oauth2
from ..utils import verify

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/", response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        #gets the row of the user that matches the email
        user = db.query(models.Account).filter(models.Account.email == credentials.username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid credentials.")
        
        #verifies password of the email/user
        if not verify(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid credentials.")

        #create a token from oauth2 using user id
        access_token = oauth2.create_token(data = {"user_id": user.id})

        #return token and account_id
        return {"access_token": access_token, "token_type": "bearer", "account_id": user.id}
    
    except HTTPException as http_error:
        raise http_error
    