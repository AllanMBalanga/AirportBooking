from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from .body import TokenData
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_minutes

def create_token(data: dict):
    #create a copy of data
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #user_id from login.py access toekn
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        
    except JWTError as e:
        raise credentials_exception
    
    return TokenData(id=id)

def get_current_user(token = Depends(oauth2_scheme)):
    credentias_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})

    return verify_token(token, credentias_exception)