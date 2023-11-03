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

# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:egcoming@localhost/fastapi_test'


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}/{setting.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# Base = declarative_base()


client = TestClient(app)

@pytest.fixture
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


@pytest.fixture
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


