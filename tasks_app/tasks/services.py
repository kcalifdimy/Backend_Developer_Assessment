# """
# Provides functions for CRUD (Create, Read, Update, Delete) operations on tasks in a task management system.

# Imports:
#     - List, Optional, Set: Type hinting for lists, optionals, and sets.
#     - WebSocket, WebSocketDisconnect, APIRouter: FastAPI components for handling WebSocket connections and building API routes.
#     - HTTPException, status: FastAPI components for handling HTTP exceptions and status codes.
#     - Session: SQLAlchemy session for database interactions.
#     - User, Task: SQLAlchemy models representing users and tasks in the database.
#     - TaskCreate, TaskUpdate: Pydantic models for creating and updating tasks.

# Variables:
#     - active_connections: A set to keep track of active WebSocket connections.

# Functions:
#     - create_new_task: Creates a new task with the provided data and associates it with the current user.
#     - get_task_by_id: Retrieves a task by its ID from the database.
#     - get_all_tasks: Retrieves a paginated list of all tasks from the database.
#     - update_task_by_id: Updates an existing task by its ID with the provided update data.
#     - delete_task_by_id: Deletes a task by its ID from the database.

# Dependencies:
#     - None

# Returns:
#     - Depending on the function, returns a task instance, list of tasks, or raises an HTTPException if the operation fails.
# """
# from typing import List, Optional, Set

# from fastapi import WebSocket, WebSocketDisconnect, APIRouter
# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session

# from tasks_app.db_models.models import User, Task
# from tasks_app.tasks.schema import TaskCreate, TaskUpdate

# active_connections: Set[WebSocket] = set()

# async def create_new_task(task: TaskCreate, current_user: User, database: Session) -> Task:
#     # Fetch the user info from the database
#     user_info = database.query(User).filter(User.email == current_user.email).first()
    
#     if not user_info:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
    
#     new_task = Task(**task.dict(), user_id=user_info.id)
#     database.add(new_task)
#     database.commit()
#     database.refresh(new_task)
#     for connection in active_connections:
#         connection.send_text(f"New task created: {new_task.title}")
#     return new_task

# async def get_task_by_id(task_id:int, database:Session) -> Optional[Task]:
#     task = database.query(Task).get(task_id)
#     if not task:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
#     return task

# async def get_all_tasks(database:Session, skip: int = 0, limit : int = 10,) -> List[Task]:
#     tasks = database.query(Task).offset(skip).limit(limit).all()
#     return tasks

# async def update_task_by_id(task_id: int, task_update: TaskUpdate, database: Session):
#     database_task = database.query(Task).filter(Task.id == task_id).first()
#     if database_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     for key, value in task_update.dict().items():
#         setattr(database_task, key, value)
#     database.commit()
#     database.refresh(database_task)
#     for connection in active_connections:
#         connection.send_text(f"Task {database_task.id} updated")
#     return database_task

# async def delete_task_by_id(task_id: int, database: Session):
#     task = database.query(Task).filter(Task.id == task_id).first()
#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     database.delete(task)
#     database.commit()
#     for connection in active_connections:
#         connection.send_text(f"Task {task.id} deleted")
#     return task
