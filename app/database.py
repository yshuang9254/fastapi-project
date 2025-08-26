from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings


# PostgreSQL 資料庫連線
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}?sslmode=require"
engine = create_engine(SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"}) 
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

"""
# 資料庫連線重試機制：純 psycopg2 → 需要自己手動連線、重試、管理 cursor
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
"""