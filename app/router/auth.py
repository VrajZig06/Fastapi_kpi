import sys
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import hash_user_password,verify_user_password,generate_token

# Add shared_utils to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import models,schema
from app.database import get_db

auth_router = APIRouter(
    prefix="/auth"
)

@auth_router.post("/login")
def login_user(user_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    # Check that user exists or not
    is_user_exists = db.query(models.User).filter(models.User.email == user_data.username).first()
    
    if not is_user_exists:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not Exists")

    is_password_correct = verify_user_password(user_data.password,is_user_exists.password)

    if not is_password_correct:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wrong User Password!")
    
    payload = {
        "id" : str(is_user_exists.id),
        "email" : is_user_exists.email
    }
    
    access_token = generate_token(payload)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }