from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True # 預設貼文為已發布

class PostCreate(PostBase):
    pass # 建立貼文，繼承 PostBase 的欄位

class Post(PostBase):
    created_at:datetime # 繼承 PostBase 的欄位，新增貼文建立時間
    class Config:
        from_attributes = True # 讓 Pydantic 能從 ORM 模型中讀取資料

class UserCreate(BaseModel):
    email:EmailStr # EmailStr 自動驗證格式是不是email
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True