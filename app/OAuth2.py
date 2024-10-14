from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
import secrets
from datetime import datetime,timedelta, timezone
from fastapi import HTTPException,status,Depends
from .schemas import TokenResponseData
from .models import User
from sqlalchemy.orm import Session
from .config import settings



#You need three things to create a token

SECRET_KEY=secrets.token_hex(32)
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes


def create_access_token(data):
    to_encode=data.copy()
    expires=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id :str =payload.get("user_id")
        if not id:
            raise credential_exception
        token_data=TokenResponseData(id=id)
        return token_data
    except JWTError:
        raise credential_exception

from .database import get_db
db_dependency=Annotated[Session, Depends(get_db)]
oaut2_bearer=OAuth2PasswordBearer(tokenUrl='/login')
def get_current_user(token:str =Depends(oaut2_bearer),db:Session =Depends(get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not valid credentials",headers={"WWW-Authenticate":"Bearer"})
    token_obj=verify_access_token(token,credential_exception)
    user=db.query(User).filter(token_obj.id==User.id).first()
    return user


    
