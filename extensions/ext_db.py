from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
print(f'Connecting to postgresql://{os.getenv("USER_DB_USERNAME")}:{os.getenv("USER_DB_PASSWORD")}@{os.getenv("USER_DB_HOST")}:{os.getenv("USER_DB_PORT")}/{os.getenv("USER_DB_DATABASE")}')
engine = create_engine(f'postgresql://{os.getenv("USER_DB_USERNAME")}:{os.getenv("USER_DB_PASSWORD")}@{os.getenv("USER_DB_HOST")}:{os.getenv("USER_DB_PORT")}/{os.getenv("USER_DB_DATABASE")}')
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

