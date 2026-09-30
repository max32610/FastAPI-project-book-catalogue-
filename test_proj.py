import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from models import Base,User,Book
from schemas import UserRegistrationDTO,LoginUserDTO,AddBookDTO
from crud import register_user,login_user,add_book,add_book_for_user
from exceptions import UserAlreadyExists,IncorrectPassword
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)

@pytest_asyncio.fixture
async def session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
@pytest.mark.asyncio
async def test_register_user(session):
    user_data = UserRegistrationDTO(name='Alex',age=18,email='user@example.com',password='string')
    user = await register_user(user_data,session)
    assert user.name == 'Alex'
    assert user.age == 18
    assert user.email == 'user@example.com'
    assert user.hashed_password != 'string'
    assert user.id is not None
@pytest.mark.asyncio
async def test_regitset_duplicate_email(session):
    user_data = UserRegistrationDTO(name='Max',age=18,email='user@example.com',password = 'string')
    await register_user(user_data,session)
    duplicate_user_data = UserRegistrationDTO(name='Max',age=18,email='user@example.com',password = 'string')
    with pytest.raises(UserAlreadyExists):
        await register_user(duplicate_user_data,session)
@pytest.mark.asyncio
async def test_login_user(session):
    user_data = UserRegistrationDTO(name='Max',age=18,email='user@example.com',password = 'string')
    await register_user(user_data,session)
    user_login_data = LoginUserDTO(email='user@example.com',password = 'string')
    result = await login_user(user_login_data,session)
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None
    assert result["token_type"] == "bearer"
@pytest.mark.asyncio
async def test_login_wrong_password(session):
    user_data = UserRegistrationDTO(name='Max',age=18,email='user1@example.com',password = 'string')
    await register_user(user_data,session)
    user_login_data = LoginUserDTO(email='user1@example.com',password = 'wrong')
    with pytest.raises(IncorrectPassword):
        await login_user(user_login_data,session)
@pytest.mark.asyncio
async def test_add_book(session):
    admin = User(
        name="Admin",age=30,email="admin@example.com",hashed_password="hashed_password",role="admin")

    session.add(admin)
    await session.commit()

    book_data = AddBookDTO(
        title="Change",
        description="your life",
        read_url="https://dsajdwqdsa.ru"
    )

    result = await add_book(session, book_data, admin)

    assert result is not None
    assert result.title == 'Change'
    assert result.description == 'your life'
    assert result.id is not None
@pytest.mark.asyncio
async def test_add_book_for_user(session):
    user = User(name='burmalda',age=15,email = 'email@example.com',hashed_password="hashed_password")
    book = Book(title='book',description = 'books',read_url = 'url:?/dsaq')
    session.add(book)
    await session.commit()
    await session.refresh(book)
    result = await add_book_for_user(user,book.id,session)
    assert result.title == 'book'
    assert result.id is not None
    assert result.description == 'books'
    assert result.read_url == 'url:?/dsaq'

    
        




