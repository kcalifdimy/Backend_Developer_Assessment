"""
Password Hashing Utilities

This module provides utilities for hashing and verifying passwords using the Argon2 algorithm.
It utilizes the Passlib library to handle password hashing securely.

Functions:
    - verify_password(plain_password: str, hashed_password: str) -> bool:
        Verifies a plain password against a hashed password.

    - get_password_hash(password: str) -> str:
        Hashes a plain password using the Argon2 algorithm.

Dependencies:
    - passlib.context.CryptContext: For managing hashing schemes and contexts.
"""

from passlib.context import CryptContext

# Create a CryptContext object with the Argon2 algorithm for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password using the Argon2 algorithm.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)
