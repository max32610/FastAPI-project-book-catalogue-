from db import async_session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException
from security import jwt,JWTError,SECRET_KEY,ALGORITHM
from crud import get_user
async def get_session():
    session = async_session()
    yield session
oauth2 = OAuth2PasswordBearer(tokenUrl='/login')

async def get_current_user(token:str = Depends(oauth2),session = Depends(get_session)):
    try:
         data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401,detail='Invalid token')
    user_id = data['user_id']
    user = await get_user(user_id,session)
    if not user:
        raise HTTPException(status_code=401,detail='User does not exist')
    return user
async def get_current_admin(user = Depends(get_current_user)):
    if user.role == 'admin':
        return user
    raise HTTPException(status_code=403,detail='403 Forbidden')
    

