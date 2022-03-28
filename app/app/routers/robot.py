# Database operations
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User

router = APIRouter(
    prefix="/robot",
    tags=["robot"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=200)
async def create_control(user: User):
    pass

@router.delete("/", status_code=200)
async def delete_control(user: User):
    pass

@router.get("/", status_code=200)
async def get_control_by_robot_id(user: User):
    pass

@router.get("/list", status_code=200)
async def list_controls(user: User):
    pass