"""
Authentication Routes for FastAPI Application

This module defines the authentication routes for a FastAPI application, specifically for user login.
It handles user verification and JWT token generation.

Routes:
    - POST /login: Authenticates a user and returns a JWT token if credentials are valid.

Dependencies:
    - datetime.timedelta: For handling time intervals.
    - fastapi.APIRouter: For creating a FastAPI router instance.
    - fastapi.Depends: For declaring dependencies in FastAPI route handlers.
    - fastapi.HTTPException: For raising HTTP exceptions in FastAPI.
    - fastapi.status: For accessing HTTP status codes.
    - fastapi.security.OAuth2PasswordRequestForm: For handling OAuth2 password request forms.
    - sqlalchemy.orm.Session: For database session handling.
    - config.db_settings: For database configuration settings.
    - tasks_app.db_models.hashing: For password hashing utilities.
    - tasks_app.db_models.models.User: For the User model.
    - .jwt.create_access_token: For creating JWT tokens.

"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import db_settings
from tasks_app.db_models import hashing
from tasks_app.db_models.models import User
from .jwt import create_access_token

# Create a router instance for authentication routes
router = APIRouter(
    tags=['auth']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db_settings.get_db)):
    """
    Authenticates a user and returns a JWT token if credentials are valid.

    Args:
        request (OAuth2PasswordRequestForm): The login form data, including username and password.
        database (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the user is not found or the password is invalid.
    """
    user = database.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password')

    # Generate a JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
