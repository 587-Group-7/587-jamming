# Database operations
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User

# Local definitions
class UserId(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=201)
async def create_measurement(user: User):
    pass

@router.get("/", status_code=201)
async def get_measurement_by_id(id: UserId):
    pass

@router.get("/list", status_code=201)
async def list_measurements(request: Request):
    pass

@router.delete("/", status_code=201)
async def delete_measurement_by_id(user: User):
    pass