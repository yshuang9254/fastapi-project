from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models,schemas,utils

router = APIRouter(prefix = "/users",tags = ["users"])

"""新增使用者，對密碼加密"""
@router.post("/",status_code = status.HTTP_201_CREATED,response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail="此信箱已被註冊過，請使用其他信箱。")
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

"""取得指定id使用者資料"""
@router.get("/{id}",response_model = schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"id為{id}的使用者不存在。")
    return user