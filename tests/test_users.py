from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas
from app.main import app
from app.config import setting
from app.database import get_db
from app.database import Base

# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:egcoming@localhost/fastapi_test'


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}/{setting.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# เอาไว้ generate table โดยไม่มี alembic 
Base.metadata.create_all(bind=engine)

Base = declarative_base()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db



client = TestClient(app)

# def test_root():
#     res = client.get("/")
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200

# def test_create_user(client):
#     res = client.post(
#         "/users/", json={"email": "hello123@gmail.com", "password": "password123"})

#     new_user = schemas.UserOut(**res.json())
#     assert new_user.email == "hello123@gmail.com"
#     assert res.status_code == 201



def test_create_user():
    res = client.post("/users/", json={"email": "user5@example.com", "password": "string"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "user5@example.com"
    assert res.status_code == 201