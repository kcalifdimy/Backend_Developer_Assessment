"""
Authentication and Authorization Utilities

This module provides functions and utilities for handling JWT-based authentication and authorization
in a FastAPI application. It includes functions for creating and verifying JWT tokens and a dependency
for retrieving the current user based on the provided token.

Functions:
    create_access_token(data: dict) -> str:
        Creates a JWT access token with an expiration time.

    verify_token(token: str, credentials_exception) -> schema.TokenData:
        Verifies a JWT token and extracts the token data.

    get_current_user(data: str = Depends(oauth2_scheme)) -> schema.TokenData:
        Retrieves the current user based on the provided OAuth2 token.

Dependencies:
    - os: For interacting with the operating system and reading environment variables.
    - datetime: For handling date and time operations.
    - fastapi.Depends: For declaring dependencies in FastAPI route handlers.
    - fastapi.HTTPException: For raising HTTP exceptions in FastAPI.
    - fastapi.status: For accessing HTTP status codes.
    - fastapi.security.OAuth2PasswordBearer: For handling OAuth2 password flow.
    - jose.JWTError, jose.jwt: For encoding and decoding JWT tokens.
    - dotenv.load_dotenv: To load environment variables from a .env file.
    - tasks_app.auth.schema: For defining the data structure of token data.

Environment Variables:
    - SECRET_KEY: Secret key used for encoding and decoding JWT tokens.
    - ALGORITHM: Algorithm used for encoding the JWT tokens.
    - ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes.
"""

import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from dotenv import load_dotenv

from tasks_app.auth import schema

# Load environment variables from a .env file
load_dotenv()

# Retrieve secret key, algorithm, and token expiration time from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict) -> str:
    """
    Creates a JWT access token with an expiration time.

    Args:
        data (dict): Data to include in the JWT token payload.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """
    Verifies a JWT token and extracts the token data.

    Args:
        token (str): JWT token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.

    Returns:
        schema.TokenData: Extracted token data.

    Raises:
        HTTPException: If the token is invalid or verification fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception

# OAuth2 password flow scheme for obtaining tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided OAuth2 token.

    Args:
        data (str): Encoded JWT token provided by the OAuth2 scheme.

    Returns:
        schema.TokenData: Extracted token data of the current user.

    Raises:
        HTTPException: If the token is invalid or verification fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)
