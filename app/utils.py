from pwdlib import PasswordHash
from datetime import datetime,timezone,timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_user_password(password:str):
    hash_password = PasswordHash.recommended()
    return hash_password.hash(password)

def verify_user_password(plain_password:str,hash_user_password:str):
    hash_password = PasswordHash.recommended()

    return hash_password.verify(plain_password,hash_user_password)
    
def generate_token(payload:dict,expires_delta: timedelta | None = None):
    to_encode = payload.copy()

    if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        decoded_payload = jwt.decode(token,key=SECRET_KEY,algorithms=ALGORITHM)
    
        id = decoded_payload.get('id')

        if not id:
            raise credentials_exception
        
        return id   
    except InvalidTokenError:
        raise credentials_exception
        
        
def get_curent_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Credentials are not authenticated!")

    return verify_token(token,credential_exception)

    
