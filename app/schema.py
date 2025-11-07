from pydantic import BaseModel,EmailStr
from typing import Optional

class User(BaseModel):
    email : EmailStr
    password : str
    is_active : Optional[bool] = True
    
class LoginUser(BaseModel):
    email : EmailStr
    password : str
    
class Post(BaseModel):
    title : str
    description : str
    is_published : Optional[bool] = True
    owner_id : Optional[int]  = None

    class Config:
        orm_mode = True
        
        
class QueryParameter(BaseModel):
    # This will restrict user from entering extra query params

    model_config = {"extra": "forbid"}
    
    limit : int = 10
    skip : int = 0
    search : str = None
    
    
# Test Classes

class Data(BaseModel):
    name: str
    age : int
    
class Data2(BaseModel):
    sex : str
    adult : bool

