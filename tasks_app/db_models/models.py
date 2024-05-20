"""
Database Models for Users and Tasks

This module defines the SQLAlchemy ORM models for `User` and `Task` entities in the application.
These models represent the database schema and include relationships and utility methods for 
handling user passwords.

Classes:
    - User: Represents a user in the application.
    - Task: Represents a task associated with a user in the application.

Dependencies:
    - datetime: For handling date and time operations.
    - sqlalchemy: For defining database columns and relationships.
    - config.db_settings.Base: For the declarative base class.
    - tasks_app.db_models.hashing: For password hashing utilities.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from config.db_settings import Base
from . import hashing

class User(Base):
    """
    Represents a user in the application.

    Attributes:
        id (int): The primary key of the user.
        name (str): The name of the user.
        email (str): The unique email of the user.
        password (str): The hashed password of the user.
        tasks (list[Task]): The list of tasks associated with the user.

    Methods:
        __init__(name: str, email: str, password: str): Initializes a new user with hashed password.
        check_password(password: str) -> bool: Verifies the given password against the stored hashed password.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    tasks = relationship("Task", back_populates="user_info")

    def __init__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = hashing.get_password_hash(password)

    def check_password(self, password):
        """
        Verifies the given password against the stored hashed password.

        Args:
            password (str): The plain text password to verify.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return hashing.verify_password(password, self.password)

class Task(Base):
    """
    Represents a task associated with a user in the application.

    Attributes:
        id (int): The primary key of the task.
        title (str): The title of the task.
        description (str): The description of the task.
        due_date (datetime): The due date of the task.
        creation_date (datetime): The creation date of the task, defaults to current time.
        completed (bool): Whether the task is completed.
        user_id (int): The foreign key referencing the user the task belongs to.
        user_info (User): The user associated with the task.
    """
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    due_date = Column(DateTime, nullable=True)
    creation_date = Column(DateTime, default=datetime.now)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user_info = relationship("User", back_populates="tasks")
