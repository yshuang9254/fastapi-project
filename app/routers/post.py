from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import case,or_,and_,func
from typing import List,Optional
from .. import models,schemas,oauth2

router = APIRouter(prefix = "/posts",tags = ["posts"])

"""取得所有貼文"""
@router.get("/",response_model = List[schemas.PostOut]) 
def get_posts(db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user),
              limit:int = 100,skip:int = 0,search:Optional[str] = ""):
    
    query = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    
    title_match = models.Post.title.contains(search)
    content_match = models.Post.content.contains(search)
    votes = func.count(models.Vote.post_id).desc()
    if search:
        contains =  or_(title_match, content_match)
        sort = case((and_(title_match, content_match), 1),(title_match, 2),(content_match, 3),else_=4)
        query = query.filter(contains).order_by(sort,votes,models.Post.created_at.desc())
    else:
        query = query.order_by(votes,models.Post.created_at.desc())
    posts = query.limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="找不到相關關鍵字")
    return posts

"""新增貼文"""
@router.post("/",status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):  
    new_post = models.Post(owner_id = current_user.id,**post.model_dump()) 
    db.add(new_post) 
    db.commit() 
    db.refresh(new_post) 
    return new_post 

"""取得最新一則貼文"""
@router.get("/latest",response_model = schemas.PostOut) 
def get_latest_post(db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id
            ).order_by(models.Post.created_at.desc()).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "沒有最新貼文") 
    return post

"""根據ID取得貼文"""
@router.get("/{id}",response_model = schemas.PostOut)
def get_post(id: int,db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)): 
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id
            ).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"id為{id}的貼文不存在。") 
    return post

"""刪除指定ID的貼文"""
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int,db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"id為{id}的貼文不存在。")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action.")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

"""更新指定ID的貼文"""
@router.put("/{id}",response_model = schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"id為{id}的貼文不存在。")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action.")
    post_query.update(post.model_dump(),synchronize_session = False) 
    db.commit()
    return post_query.first()