from fastapi import FastAPI,Header,Request,Depends,UploadFile
from typing import Annotated
from typing import Optional
from fastapi.staticfiles import StaticFiles
import base64
import shutil
from psycopg2.extras import RealDictCursor
import psycopg2
from pydantic import BaseModel,Field

UPLOAD_DIR = "uploads"

app = FastAPI()


# ------------- DATE : 04/11/2025 --------------------

# Database Connection
DB_NAME = "fastapi_kpi"
DB_USER = "postgres"
DB_PASS = "ztlab141" 
DB_HOST = "localhost"
DB_PORT = "5432"

# Pydantic Post 
class Post(BaseModel):
    title : Annotated[str,Field(...,description="Post's Title")]
    description : Annotated[str,Field(...,description="Post's Description")]
    is_published : Annotated[bool,Field(default=False,description="Post is Published or not.")]

class UPost(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    is_published : Optional[bool] = None

def connect():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,cursor_factory=RealDictCursor)
        
        # create cursor
        curs = conn.cursor()
        yield curs, conn
        print("Database connected successfully")
    except Exception as e:
        print(f"Database not connected successfully : {e}")
    
  
# ------ Using Raw Query --------
  
# @app.get('/posts')
# def get_posts(db = Depends(connect)):
#     """
#     This will fetched all Posts
#     """
#     curs,conn = db
#     curs.execute("""SELECT id,title,description FROM posts""")
#     data = curs.fetchall()
#     return data

# @app.get("/posts/{post_id}")
# def get_post(post_id:int,db = Depends(connect)):
#     """
#     This will Give post with post id
#     """
#     curs,conn = db
#     curs.execute(f"""SELECT id,title,description from posts where id = {post_id}""")
#     data = curs.fetchone()
#     return data

# @app.post("/posts")
# def create_post(post:Post,db = Depends(connect)):
#     curs,conn = db
#     curs.execute(
#         """
#         INSERT INTO posts (title, description, is_published)
#         VALUES (%s, %s, %s)
#         RETURNING id, title, description, is_published
#         """,
#         (post.title, post.description, post.is_published)
#     )
#     new_post = curs.fetchone()
#     conn.commit()
#     return {
#         "msg" : "Post created successfully",
#         "post" : new_post
#     }
    
# @app.delete("/posts/{post_id}")
# def delete_post(post_id:int,db = Depends(connect)):
#     curs,conn = db
#     curs.execute("""DELETE from posts where id = %s""",(post_id,))
#     conn.commit()
#     return {
#         "msg": "Data Deleted Successfully!"
#     }
    
# @app.patch("/posts/{post_id}")
# def update_post(post_id:int,updated_post:UPost,db = Depends(connect)):
#     curs,conn = db
#     if post_id:
#         curs.execute("""SELECT * FROM posts where id = %s""",(post_id,))
#         existing_post = curs.fetchone()

#         new_title = updated_post.title if updated_post.title else existing_post.get('title')
#         new_description = updated_post.description if updated_post.description else existing_post.get('description')
#         new_is_published = updated_post.is_published if updated_post.is_published else existing_post.get('is_published')
        
#         curs.execute("""
#             UPDATE posts SET title = %s, description = %s, is_published = %s where id = %s RETURNING id,title,description          
#         """,(new_title,new_description,new_is_published,post_id))
        
#         data = curs.fetchone()

#         conn.commit()
#         return {
#             "msg" : "Post Updated Successfully!",
#             "data" : data
#         }
#     else:
#         return {
#             "msg" : "Product not found!"
#         }
        
        
# ------------- DATE : 03/11/2025 --------------------


# Access To Public Folder
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# @app.get("/")
# def root():
#     return {
#         "msg" : "Hello World!"
#     }
    
# # Path Parameter
# @app.get("/data/{data_id}")
# def get_data(data_id:int,request:Request,data:str = Header()):        

#     # Get All Headers Value
#     # data = dict(request.headers)
    
#     # Get Specific Header value and also Validate using Header() Function
#     # print(data)
#     return {
#         "msg" : f"Data with id {data_id} Fetched Successfully!",
#     }
    
    
# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}


# CommonsDep = Annotated[dict, Depends(common_parameters)]


# @app.get("/items/")
# async def read_items(commons: CommonsDep):
#     return commons


# @app.get("/users/")
# async def read_users(commons: CommonsDep):
#     return commons

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     # content =  await file.read()
#     file_location = f"{UPLOAD_DIR}/{file.filename}"
    
#     # Save the uploaded file
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {
#         "filename": file.filename,
#         "content" : file_location
#     }
    

    

