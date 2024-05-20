from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from tasks_app.auth.jwt import get_current_user
from config import db_settings
from . import schema
from . import validator
from . import services

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_registration(
    request: schema.User,
    database: Session = Depends(db_settings.get_db)
):
    user = await validator.verify_email_exist(request.email, database)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
    )

    new_user = await services.new_user_register(request, database)
    return new_user


@router.get('/{user_id}', response_model=schema.DisplayUser)
async def get_user_by_id(
    user_id: int,
    database: Session = Depends(db_settings.get_db),
):
    return await services.get_user_by_id(user_id, database)

