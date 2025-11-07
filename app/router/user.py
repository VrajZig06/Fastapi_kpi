import sys
import os
from fastapi import APIRouter, Depends, HTTPException, status,UploadFile,Form
from sqlalchemy.orm import Session
from app.utils import hash_user_password,verify_user_password
import shutil

# Add shared_utils to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import models,schema
from app.database import get_db

user_router = APIRouter(
    prefix="/users"
)

UPLOAD_DIR = "uploads"

@user_router.post("/")
def create_user(user_data:schema.User,db:Session = Depends(get_db)):

    user_data.email = user_data.email.lower()
    # Check if user already exists with current email
    is_user_exist = db.query(models.User).filter(models.User.email == user_data.email).first()

    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists!")
    
    user_data.password = hash_user_password(user_data.password)

    new_user = models.User(**user_data.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "msg" : "User Created Successfully!",
        "data" : new_user
    }
    
def parse_user_data(
    name: str = Form(...),
    age: int = Form(...)
):
    return schema.Data(name=name, age=age)
    
@user_router.post("/profile")
def add_profile(user_data:schema.Data = Depends(parse_user_data),file:UploadFile = Form(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        "content" : file_location,
        "user_data" : user_data.model_dump()
    }
    
    
