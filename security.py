from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta
from exceptions import IncorrectToken
from pydantic_settings import BaseSettings

context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"


settings = Settings()
def hash_password(password: str):
    print(repr(password))
    print(type(password))
    print(len(password.encode("utf-8")))

    return context.hash(password)
def verify_password(password:str,hashed_password:str):
    return context.verify(password,hashed_password)
def create_access_token(data:dict):
    to_encode = data.copy()
    to_encode['exp'] = datetime.utcnow()+timedelta(minutes=15)
    to_encode['type'] = 'access'
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def create_refresh_token(data:dict):
    to_encode = data.copy()
    to_encode['exp'] = datetime.utcnow()+timedelta(days=7)
    to_encode['type'] = 'refresh'
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def refresh(refresh_token:str):
    try:
        payload = payload = jwt.decode(refresh_token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        if payload.get('type') != 'refresh':
            raise IncorrectToken()
        user_id = payload.get('user_id')
        if user_id is None:
            raise IncorrectToken()
        new_access_token = create_access_token(data={'user_id':user_id})
        return {'access_token':new_access_token,'token_type':'bearer'}
    except JWTError:
        raise IncorrectToken()
       



