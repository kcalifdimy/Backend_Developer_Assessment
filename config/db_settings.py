"""
Database Configuration and Connection Setup

This module is responsible for setting up and managing the connection to a PostgreSQL database using SQLAlchemy.
It utilizes environment variables for configuration, enabling secure and flexible database access.

Functions:
    get_db(): Provides a database session for use within a context.

Dependencies:
    - os: For interacting with the operating system and reading environment variables.
    - dotenv.load_dotenv: To load environment variables from a .env file.
    - sqlalchemy.create_engine: To create a new SQLAlchemy engine instance.
    - sqlalchemy.ext.declarative.declarative_base: To return a new base class for all mapped classes.
    - sqlalchemy.orm.sessionmaker: To create a configurable session factory for database operations.

Environment Variables:
    - POSTGRES_USER: Username for the PostgreSQL database.
    - POSTGRES_PASSWORD: Password for the PostgreSQL database.
    - POSTGRES_SERVER: Host address of the PostgreSQL server.
    - POSTGRES_DB: Name of the PostgreSQL database.
    - POSTGRES_PORT: Port number on which the PostgreSQL server is running.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from a .env file
load_dotenv()

# Retrieve database connection details from environment variables
DATABASE_USERNAME = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_SERVER")
DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_PORT = os.getenv("POSTGRES_PORT")

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

def get_db():
    """
    Provides a database session for use within a context.

    Yields:
        db (Session): A SQLAlchemy session object.

    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
