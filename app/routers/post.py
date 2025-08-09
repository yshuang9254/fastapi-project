from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import models,schemas

router = APIRouter()

"""取得所有貼文"""
@router.get("/posts",response_model = List[schemas.Post]) 
def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all() 
    return posts

"""新增貼文"""
@router.post("/createposts",status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db)):  
    new_post = models.Post(**post.model_dump()) 
    db.add(new_post) 
    db.commit() 
    db.refresh(new_post) 
    return new_post 

"""取得最新一則貼文"""
@router.get("/posts/latest",response_model = schemas.Post) 
def get_latest_post(db:Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "沒有最新貼文") 
    return post

"""根據ID取得貼文"""
@router.get("/posts/{id}",response_model = schemas.Post)
def get_post(id: int,db:Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was not found.") 
    return post

"""刪除指定ID的貼文"""
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} is  not exist.")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

"""更新指定ID的貼文"""
@router.put("/posts/{id}",response_model = schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} is  not exist.")
    post_query.update(post.model_dump(),synchronize_session = False) 
    db.commit()
    return post_query.first()