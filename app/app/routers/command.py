# Database operations and utils
from ..database import database
from ..utils.manager import manager, Message
from ..utils.auth import get_current_user

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import Control, User, Robot, RobotID
from typing import Optional

# Pydantic typing
from pydantic import BaseModel


router = APIRouter(
    prefix="/command",
    tags=["command"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=200)
async def execute_command(message: Message, user = Depends(get_current_user), db=Depends(database.provide_connection)):
    manager.request_send_message(message)