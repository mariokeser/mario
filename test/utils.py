from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
import pytest
from models import Base, Todos, Users
from fastapi.testclient import TestClient
from main import app
from routers.users import bcrypt_context



URL = "sqlite:///./testdb.db"
engine = create_engine(URL, connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "mariocodingtest", "id": 1, "user_role": "admin"}

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn FastAPI",
        description =  "It is nice",
        priority = 5,
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username= "mariocoding",
        email= "mariocoding@email.com",
        first_name= "Mario",
        last_name= "Keser",
        hashed_password= bcrypt_context.hash("testpassword"),
        role= "admin",
        phone_number= "(11)-111-1111"
    )
    db= TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
