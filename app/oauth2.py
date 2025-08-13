from jose import JWTError, jwt
from datetime import datetime,timedelta,timezone
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")

SECRET_KEY = "Q2lXV2pHV2J4Y0FJcFSDFFD456561Gd3Y1FVaXkfdsjNwM3VLYkU"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

"""建立並回傳包含過期時間的 JWT 存取權杖"""
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)
    return encoded_jwt

"""驗證 JWT 並回傳 Token 資料"""
def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
        return token_data
    except JWTError:
        raise credentials_exception
    

"""取得當前用戶並驗證權限"""
def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                            detail="Could not validate credentials",
                                            headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user