"""
This module defines the API endpoints for task management in a FastAPI application. It includes
endpoints for creating, retrieving, updating, and deleting tasks, as well as a WebSocket endpoint 
for real-time task updates.

Imports:
    - List, Set: Type hinting for lists and sets.
    - APIRouter, Depends, status, Response, HTTPException: FastAPI components for building API routes.
    - WebSocket, WebSocketDisconnect: FastAPI components for handling WebSocket connections.
    - Session: SQLAlchemy session for database interactions.
    - get_current_user: Dependency for retrieving the current authenticated user.
    - db_settings: Configuration settings for the database.
    - schema: Module containing Pydantic models for request and response bodies.
    - services: Module containing business logic for task management.
    - User: SQLAlchemy model representing a user in the database.

Router:
    - APIRouter: Prefixes all routes with '/task' and tags them as 'Tasks'.

Variables:
    - active_connections: A set to keep track of active WebSocket connections.

Endpoints:
    - websocket_endpoint: WebSocket endpoint at '/ws/tasks/{client_id}'. 
      Manages real-time communication with clients.
    - create_task: POST endpoint at '/tasks/'. 
      Creates a new task with the provided data and returns the created task.
    - get_user_by_id: GET endpoint at '/{task_id}'. 
      Retrieves a task by its ID and returns the task data.
    - get_all_tasks: GET endpoint at '/'. 
      Retrieves a paginated list of all tasks with optional skip and limit query parameters.
    - update_task_by_id: PUT endpoint at '/tasks/{task_id}'. 
      Updates a task by its ID with the provided update data and returns the updated task.
    - delete_task: DELETE endpoint at '/{task_id}'. 
      Deletes a task by its ID and returns the deleted task data.

Dependencies:
    - get_current_user: Dependency to get the current authenticated user from JWT.
    - db_settings.get_db: Dependency to get the database session.

Schemas:
    - schema.TaskDisplay: Pydantic model for displaying task data in responses.
    - schema.TaskCreate: Pydantic model for creating a new task.
    - schema.TaskUpdate: Pydantic model for updating an existing task.
"""
from typing import List, Set

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from tasks_app.auth.jwt import get_current_user
from config import db_settings
from . import schema
from . import services
from tasks_app.db_models.models import User

router = APIRouter(
    tags=['Tasks'],
    prefix='/task'
)

active_connections: Set[WebSocket] = set()

@router.websocket("/ws/tasks/{client_id}")
async def websocket_endpoint(client_id: int, websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"Client with {client_id} wrote {message}!")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@router.post("/tasks/", status_code=status.HTTP_201_CREATED, response_model=schema.TaskDisplay)
async def create_task(
    task: schema.TaskCreate,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(db_settings.get_db)
):
    return await services.create_new_task(task, current_user, database)

@router.get('/{task_id}', response_model=schema.TaskDisplay)
async def get_user_by_id(
    task_id: int,
    database: Session = Depends(db_settings.get_db),
):
    return await services.get_task_by_id(task_id, database)

@router.get('/', response_model=List[schema.TaskDisplay])
async def get_all_tasks(
    database: Session = Depends(db_settings.get_db),
    skip: int = 0,
    limit: int = 10,
):
    return await services.get_all_tasks(database, skip, limit)

@router.put("/tasks/{task_id}", response_model=schema.TaskUpdate)
async def update_task_by_id(
    task_id: int, 
    task_update: schema.TaskUpdate, 
    database: Session = Depends(db_settings.get_db)
):
    return await services.update_task_by_id(task_id, task_update, database)

@router.delete("/{task_id}", response_model=schema.TaskDisplay)
async def delete_task(
    task_id: int,
    database: Session = Depends(db_settings.get_db)
):
    return await services.delete_task_by_id(task_id, database)
