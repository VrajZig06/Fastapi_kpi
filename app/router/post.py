import sys
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session,joinedload
from app.utils import get_curent_user

# Add shared_utils to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import models,schema
from app.database import get_db

post_router = APIRouter(
    prefix="/posts"
)

"""********* With Query Parameter *********"""

# @post_router.get("/")
# def get_posts(db : Session = Depends(get_db),current_user = Depends(get_curent_user),limit: int = 10, skip: int = 0,search:str = None):
#     data = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.is_published == "true").limit(limit).offset(skip).all()

#     if search:
#         data = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.title.ilike(f"%{search}%")).all()

#     return {
#         "msg" : "Hello world!",
#         "data" : data
#     }

"""********* With Query Object + Query Pydantic Model *********"""    
@post_router.get("/")
def get_posts(db : Session = Depends(get_db),current_user = Depends(get_curent_user),query_parameter: schema.QueryParameter = Query()):
    
    data = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.is_published == "true").limit(query_parameter.limit).offset(query_parameter.skip).all()

    if query_parameter.search:
        data = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.title.ilike(f"%{query_parameter.search}%")).all()

    return {
        "msg" : "Hello world!",
        "data" : data
    }
    
@post_router.get("/me")
def get_my_posts(current_user:int = Depends(get_curent_user),db:Session = Depends(get_db)):
    try:
        db_query = db.query(models.Post).filter(models.Post.owner_id == current_user)
        all_posts = db_query.all()

        return {
            "msg" : "All Posts fetched Successfully for Current user.",
            "data" : all_posts
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error : {e}")

    
@post_router.get("/{id}")
def get_post(id:str, db : Session = Depends(get_db),current_user = Depends(get_curent_user)):
    data = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.id == id).first()
    
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found with Given ID.")
    
    return {
        "msg" : "Post Fetched Successfully!",
        "data" : data
    }
    
@post_router.post("/")
def create_post(post:schema.Post, db:Session = Depends(get_db),current_user = Depends(get_curent_user)):
    post.owner_id = current_user
    new_post = models.Post(**post.model_dump())
    print(new_post.is_published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "msg" : "New Post Created Successfully",
        "data" : new_post
    }
    
@post_router.delete("/{id}")
def delete_post(id:str,db:Session = Depends(get_db),current_user:str = Depends(get_curent_user)):
    is_existing_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = is_existing_post.first()

    if not is_existing_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found!")
    
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized to perform this action")
    
    is_existing_post.delete()
    db.commit()
    return {
        "msg" : "Post Deleted Successfully!",
    }



@post_router.patch("/{id}")
def update_post(id:str,post_data:schema.Post,db:Session = Depends(get_db),current_user:str = Depends(get_curent_user)):

    query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query.first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found with Given ID.")

    if existing_post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform this action")

    post_data.owner_id = current_user
    query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()

    return {"msg": "Post Updated Successfully!"}


@post_router.post('/test')
def test_router(data1 : schema.Data, data2 : schema.Data2):
    return {
        "data" : data1.model_dump(),
        "data2" : data2.model_dump()
    }


