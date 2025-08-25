from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# PostgreSQL 資料庫連線
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
# 建立 Session 類別，用來與資料庫互動
TestingSessionlocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)