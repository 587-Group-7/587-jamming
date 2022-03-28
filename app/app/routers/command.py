# Database operations
from ..database import database
import asyncpg


# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User
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
async def execute_command(user: User, command: Command):
    pass
