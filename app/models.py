from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key = True,nullable = False) # 主鍵欄位，自動遞增序列
    title = Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default = "True",nullable = False) # 資料庫自帶預設值 True
    created_at = Column(TIMESTAMP(timezone = True),nullable = False,server_default = text("now()")) # text()會建立TextClause 物件，讓SQLAlchemy知道這是 SQL 語句，不是純字串。

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True,nullable = False) # 主鍵欄位，自動遞增序列
    email = Column(String,nullable = False,unique = True) # 信箱不可重複
    password = Column(String,nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),nullable = False,server_default = text("now()")) # 資料庫自帶預設值建立時間
    