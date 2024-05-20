from typing import List, Optional

from fastapi import HTTPException, status

from tasks_app.db_models import models


async def new_user_register(request, database) -> models.User:
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user

async def get_user_by_id(user_id, database) -> Optional[models.User]:
    user_info = database.query(models.User).get(user_id)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return user_info
