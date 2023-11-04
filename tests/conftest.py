# conftest.py ทุกอย่างที่ประกาศในนี้จะเห็นใน test ไม่ต้อง import แต่จะใช้ได้เฉพาะ folder/sub folder ที่ไม่ได้มี file conftest.py ในนั้นเอง

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import setting
from app.database import get_db
from app.database import Base
from alembic import command
from app.oauth2 import create_access_token
from app import models

# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:egcoming@localhost/fastapi_test'


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}/{setting.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# Base = declarative_base()


client = TestClient(app)

# Fixture scopes
# Fixtures are created when first requested by a test, and are destroyed based on their scope:
# function: the default scope, the fixture is destroyed at the end of the test.
# class: the fixture is destroyed during teardown of the last test in the class.
# module: the fixture is destroyed during teardown of the last test in the module.
# package: the fixture is destroyed during teardown of the last test in the package.
# session: the fixture is destroyed at the end of the test session.
# default จะเป็น function


@pytest.fixture()
def session():
    # drop all table
    Base.metadata.drop_all(bind=engine)
    # เอาไว้ generate table โดยไม่มี alembic 
    # create all table
    Base.metadata.create_all(bind=engine)

    # หรือจะใช้งาน alembic แทน
    # command.upgrade("head")
    # command.downgrade("base")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    # run our code before we run our testClient
    yield TestClient(app)
    # run our code after our test finishes

@pytest.fixture
def test_user(client):
     user_data = {"email": "user1@example.com", "password": "string"}
     res = client.post("/users/", json=user_data)

     assert res.status_code == 201
    #  print(res.json())
     new_user = res.json()
     new_user['password'] = user_data['password']
     return new_user

@pytest.fixture
def test_user2(client):
     user_data = {"email": "user2@example.com", "password": "string"}
     res = client.post("/users/", json=user_data)

     assert res.status_code == 201
    #  print(res.json())
     new_user = res.json()
     new_user['password'] = user_data['password']
     return new_user


@pytest.fixture
def token(test_user):
    # print(f"token-test_user: {test_user['id']}")
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    # print(f"authorized_client-bearer: {token}")
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
