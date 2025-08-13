from pydantic import BaseModel,EmailStr, field_validator
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True # 預設貼文為已發布

class PostCreate(PostBase):
    pass # 建立貼文，繼承 PostBase 的欄位


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True

class Post(PostBase):
    id:int
    created_at:datetime # 繼承 PostBase 的欄位，新增貼文建立時間
    owner_id:int
    owner:UserOut
    class Config:
        from_attributes = True # 讓 Pydantic 能從 ORM 模型中讀取資料

class UserCreate(BaseModel):
    email:EmailStr # EmailStr 自動驗證格式是不是email
    password:str
    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower()


class UserLogin(BaseModel):
    email:EmailStr 
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None