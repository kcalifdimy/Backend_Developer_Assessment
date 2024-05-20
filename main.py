from fastapi import FastAPI
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import JSONResponse

from tasks_app.middleware.fle_logs import logging_middleware, logger


from tasks_app.auth.jwt import get_current_user

from tasks_app.user import router as user_router
from tasks_app.auth import router as auth_router
from tasks_app.tasks import router as tasks_router




app = FastAPI(
    title="TaskApp",
    version="0.0.1"
    
)

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(tasks_router.router, dependencies=[Depends(get_current_user)])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Alarm! Global exception!")
    return JSONResponse(
        status_code=500,
        content={"error": "O-o-o-ps! Internal server error"}
    )
