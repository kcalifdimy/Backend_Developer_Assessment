"""
Pydantic Models for Authentication

This module defines the Pydantic models used for authentication purposes in a FastAPI application.
These models ensure data validation and serialization for authentication-related data structures.

Classes:
    - Login: Represents the login request data.
    - Token: Represents the JWT token response data.
    - TokenData: Represents the data extracted from a JWT token.
"""

from typing import Optional
from pydantic import BaseModel

class Login(BaseModel):
    """
    Represents the login request data.

    Attributes:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.
    """
    username: str
    password: str

class Token(BaseModel):
    """
    Represents the JWT token response data.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (e.g., "bearer").
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Represents the data extracted from a JWT token.

    Attributes:
        email (Optional[str]): The email of the user associated with the token, if available.
    """
    email: Optional[str] = None
