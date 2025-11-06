from app.database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP, text,ForeignKey,UUID,Text
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String,nullable=False,primary_key=True,default=lambda: str(uuid.uuid4()))
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    is_active = Column(Boolean,default=True,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text("CURRENT_TIMESTAMP"))
    
    class Config:
        orm_mode = True

class Post(Base):
    __tablename__ = "posts"

    id = Column(String,primary_key=True,nullable=False,default=lambda: str(uuid.uuid4()))
    title = Column(String,nullable=False)
    description = Column(String)
    is_published = Column(Boolean,default=True,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text("CURRENT_TIMESTAMP"))
    
    owner_id = Column(String,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
    owner = relationship("User")
    
    class Config:
        orm_mode = True
        
