import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fastapi import FastAPI
from app import models
from app.database import engine
from .router.user import user_router
from .router.post import post_router
from .router.auth import auth_router

app = FastAPI()

# Create Tables if Not Exists
models.Base.metadata.create_all(bind=engine)

# Add Routers
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)


