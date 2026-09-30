from sqlalchemy.orm import mapped_column,DeclarativeBase,Mapped,relationship
from sqlalchemy import ForeignKey
from db import async_engine
class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    age:Mapped[int]
    hashed_password:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    books:Mapped[list["Book"]] = relationship(back_populates='users',secondary='user_books')
    role:Mapped[str] = mapped_column(default='user') 
class Book(Base):
    __tablename__ = 'books'
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str]
    description:Mapped[str]
    read_url:Mapped[str]
    users: Mapped[list["User"]] = relationship(back_populates='books',secondary='user_books')
class UserBooks(Base):
    __tablename__ = 'user_books'
    user_id:Mapped[int] = mapped_column(ForeignKey('user.id'),primary_key=True)
    book_id:Mapped[int] = mapped_column(ForeignKey('books.id'),primary_key=True)
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
