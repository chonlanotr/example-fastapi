from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from .config import setting



# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/<hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:egcoming@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}/{setting.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Reference
# while True:
#     try:
#         conninfo = "host='localhost' port='5432' dbname='fastapi' user='postgres' password='egcoming'"
#         conn = psycopg.connect( conninfo=conninfo, row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break 
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error:", error)
#         time.sleep(2)