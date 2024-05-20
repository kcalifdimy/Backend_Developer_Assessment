import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.db_settings import Base, get_db

load_dotenv()

from main import app





DATABASE_USERNAME = os.getenv("TEST_POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("TEST_POSTGRES_HOST")
DATABASE_NAME = os.getenv("TEST_POSTGRES_DB")


SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db