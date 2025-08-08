from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from random import randrange
import psycopg2 # greSQL 資料庫驅動程式
from psycopg2.extras import RealDictCursor # 查詢結果會變成字典（dict），而不是Tuple
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db
from typing import List



# 建立資料庫表格（若表格不存在）
models.Base.metadata.create_all(bind = engine) 


app = FastAPI()

# 資料庫連線重試機制
for i in range(5):
    try:
        conn = psycopg2.connect(host = "localhost",database = "fastapi",user = "postgres"
                                ,password = "712140",cursor_factory = RealDictCursor) # conn（連線物件）只代表跟資料庫的連線，但它不能直接執行查詢
        cursor = conn.cursor() # cursor（游標）是執行 SQL 查詢的工具
        print("資料庫連接成功!")
        break
    except Exception as error:
        print("資料庫連接失敗!\n","Error:",error)
        time.sleep(3) # 暫停三秒，之後會繼續迴圈重試連接。


@app.get("/")
def root(): 
    return {"message":"Hello world!"}


"""取得所有貼文"""
@app.get("/posts",response_model = List[schemas.Post]) 
def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all() 
    return posts

"""新增貼文"""
@app.post("/createposts",status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db)):  
    new_post = models.Post(**post.model_dump()) 
    db.add(new_post) 
    db.commit() 
    db.refresh(new_post) 
    return new_post 

"""取得最新一則貼文"""
@app.get("/posts/latest",response_model = schemas.Post) 
def get_latest_post(db:Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "沒有最新貼文") 
    return post

"""根據ID取得貼文"""
@app.get("/posts/{id}",response_model = schemas.Post)
def get_post(id: int,db:Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was not found.") 
    return post

"""刪除指定ID的貼文"""
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} is  not exist.")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

"""更新指定ID的貼文"""
@app.put("/posts/{id}",response_model = schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} is  not exist.")
    post_query.update(post.model_dump(),synchronize_session = False) 
    db.commit()
    return post_query.first()

"""新增使用者"""
@app.post("/createuser",status_code = status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
