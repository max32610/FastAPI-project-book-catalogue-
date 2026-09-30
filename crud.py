from db import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import User,Book
from schemas import UserRegistrationDTO,LoginUserDTO,AddBookDTO
from security import hash_password,create_access_token,create_refresh_token,verify_password
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from exceptions import UserNotFoundErr,BookNotFoundErr,BookAlrExists,UserAlreadyExists,IncorrectPassword
from sqlalchemy.exc import IntegrityError
async def get_user(user_id:int,session:AsyncSession):
    stmt = select(User).options(selectinload(User.books)).where(User.id == user_id)
    if stmt is None:
        raise UserNotFoundErr()
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user
async def get_books(session:AsyncSession):
    stmt = select(Book)
    if stmt is None:
        raise BookNotFoundErr()
    result = await session.execute(stmt)
    return result.scalars().all()
async def register_user(user_data:UserRegistrationDTO,session :AsyncSession):
    data = user_data.model_dump()
    password = data.pop('password')
    hashed_password = hash_password(password)
    data['hashed_password'] = hashed_password
    user = User(**data)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExists()
    await session.refresh(user)
    return user
async def login_user(user_data:LoginUserDTO,session:AsyncSession):
    data = user_data.model_dump()
    stmt = select(User).where(User.email == data['email'])
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise UserNotFoundErr()
    if not verify_password(data['password'],user.hashed_password):
        raise IncorrectPassword()
    access_token = create_access_token(data = {'user_id':user.id})
    refresh_token = create_refresh_token(data = {'user_id':user.id})
    return {"access_token": access_token,"refresh_token": refresh_token,"token_type": "bearer"}
async def add_book(session:AsyncSession,book: AddBookDTO, user:User):
    new_data = book.model_dump()
    new_book = Book(**new_data)
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book
async def search_book(session:AsyncSession,title:str):
    nbook = select(Book).where(Book.title.ilike(f"%{title}%"))
    if nbook is None:
        raise BookNotFoundErr()
    result = await session.execute(nbook)
    book = result.scalars().all()
    return book
async def get_user_book(user:User,book_id:int, session:AsyncSession):
    stmt = select(Book).join(Book.users).where(Book.id == book_id,User.id == user.id)
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()
    if book is None:
        raise BookNotFoundErr()
    return book
async def add_book_for_user(user:User,book_id:int,session: AsyncSession):
    book = await session.get(Book,book_id)
    if book is None:
        raise BookNotFoundErr()
    if book in user.books:
        return BookAlrExists()
    user.books.append(book)
    await session.commit()
    return book
async def remove_book_for_user(user:User,session:AsyncSession,book_id:int):
    book = await session.get(Book,book_id)
    if book is None:
        raise  BookNotFoundErr()
    user.books.remove(book)
    await session.commit()
    return book
async def get_user_books(user:User,session:AsyncSession):
    stmt = select(Book).join(Book.users).where(User.id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()



    


