# Database operations
from ..database import database
import asyncpg


# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import Control, User, Robot, RobotID
from typing import Optional

# Pydantic typing
from pydantic import BaseModel

# Class definitions
class Movement(BaseModel):
    duration: int
    speed: int

class Rotation(BaseModel):
    duration: int
    angle: int

class Command(BaseModel):
    rotation: Optional[Rotation] = None
    movement: Optional[Movement] = None


router = APIRouter(
    prefix="/command",
    tags=["command"],
    responses={404: {"description": "Not found"}}
)

# TODO: Robotic movements would be implemented here. Web Sockets may be ideal for communicating information.
@router.post("/", status_code=200)
async def execute_command(control: Control, user: User, robot: RobotID, command: Command, db=Depends(database.provide_connection)):
    control = await db.fetch_one("SELECT userId, robotId FROM control WHERE id=:id", values={"id": control.id})
    if (control is not None and control.userId == user.id and control.robotId == robot.id):
        pass
        # TODO: This is where robot control requests would be made.
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or robot id, or invalid control id",
        )