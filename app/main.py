from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import psycopg2 # greSQL 資料庫驅動程式
from psycopg2.extras import RealDictCursor # 查詢結果會變成字典（dict），而不是Tuple
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth



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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root(): 
    return {"message":"Hello world!"}







