from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# PostgreSQL 資料庫連線
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:712140@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
# 建立 Session 類別，用來與資料庫互動
Sessionlocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)
# 建立 Base 為所有 ORM 類別的父類別，宣告資料表結構用
Base = declarative_base() 

"""產生資料庫 Session 物件，並確保最後關閉"""
def get_db():
    db = Sessionlocal()
    try:
        yield db 
    finally: 
        db.close()