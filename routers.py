from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from crud import register_user,login_user,get_books,get_user,add_book,search_book,get_user_book,add_book_for_user,remove_book_for_user,get_user_books
from schemas import UserRegistrationDTO,LoginUserDTO,ReadBooknDescDTO,ReadUserAdminDTO,ReadUserMeDTO,ReadUserDTO,ReadBookDTO,AddBookDTO
from dependency import get_session,get_current_user,get_current_admin
from models import User
from crud import AsyncSession
from exceptions import BookAlrExists,BookNotFoundErr,UserNotFoundErr,IncorrectToken,UserAlreadyExists
from security import refresh
router = APIRouter()
@router.post('/registration',response_model=ReadUserMeDTO)
async def registration(user_data:UserRegistrationDTO,session: AsyncSession = Depends(get_session)):
    try:
        return await register_user(user_data,session)
    except UserAlreadyExists:
        raise HTTPException(status_code=409,detail='User with that email already exists')
@router.post('/login')
async def login(user_data:OAuth2PasswordRequestForm = Depends(),session: AsyncSession = Depends(get_session)):
    data = LoginUserDTO(email = user_data.username,password = user_data.password)
    return await login_user(data,session)
@router.get('/books',response_model=list[ReadBookDTO])
async def getbooks(user: User = Depends(get_current_user), session: AsyncSession=Depends(get_session)):
    return await get_books(session)
@router.get('/user/{user_id}',response_model=ReadUserDTO)
async def getuser(user_id:int,session: AsyncSession=Depends(get_session),user: User = Depends(get_current_user)):
    return await get_user(user_id,session)
@router.get('/user/{user_id}/details',response_model=ReadUserAdminDTO)
async def getdetaileduser(user_id:int,session: AsyncSession=Depends(get_session),user: User = Depends(get_current_admin)):
    return await get_user(user_id,session)
@router.get('/me',response_model=ReadUserMeDTO)
async def getme(user: User = Depends(get_current_user)):
    return user
@router.post('/books',response_model=ReadBooknDescDTO)
async def addbook(book:AddBookDTO,user:User = Depends(get_current_admin),session:AsyncSession = Depends(get_session)):
    return await add_book(session,book,user)
@router.get('/book/title',response_model=list[ReadBookDTO])
async def searchbook(title:str,session = Depends(get_session)):
    return await search_book(session,title)
@router.get('/book/{book_id}',response_model=ReadBooknDescDTO)
async def getuserbook(book_id:int, session = Depends(get_session),user:User = Depends(get_current_user)):
    try:
        return await get_user_book(user,book_id,session)
    except BookNotFoundErr:
        raise HTTPException(status_code=404,detail='Book was not found!')
@router.post('/me/books/{book_id}',response_model=ReadBookDTO)
async def addbookforuser(book_id:int, user:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    try:
        return await add_book_for_user(user,book_id,session)
    except BookNotFoundErr:
        raise HTTPException(status_code=404,detail="Book was not found")
    except BookAlrExists:
        raise HTTPException(status_code=409,detail="User already has this book")
@router.delete('/me/books/{book_id}')
async def delbook(book_id:int,user:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    try:
        return await remove_book_for_user(user,session,book_id)
    except BookNotFoundErr:
        raise HTTPException(status_code=404,detail='Book was not found!')
@router.get('/me/books')
async def getuserbooks(user:User = Depends(get_current_user),session = Depends(get_session)):
    return await get_user_books(user,session)
@router.post('/refresh')
def refreshacctoken(refresh_token:str):
    try:
        return refresh(refresh_token)
    except IncorrectToken:
        raise HTTPException(status_code=401,detail='Invalid or expired refresh token')





