"""
Defines Pydantic models for representing tasks in a task management system.

Imports:
    - datetime: For working with date and time.
    - BaseModel: Base class for creating Pydantic models.

Classes:
    - TaskCreate: Pydantic model for creating a new task. Includes fields for title, description, 
      due date, and creation date.
    - TaskUpdate: Pydantic model for updating an existing task. Includes fields for title, description, 
      due date, and creation date.
    - TaskDisplay: Pydantic model for displaying task data. Includes fields for task ID, title, 
      description, completion status, due date, and creation date.
"""
from datetime import datetime
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    creation_date: datetime

class TaskUpdate(BaseModel):
    title: str
    description: str
    due_date: datetime
    creation_date: datetime

class TaskDisplay(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    due_date: datetime
    creation_date: datetime
