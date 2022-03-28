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
async def create_user(user: User, db=Depends(database.provide_connection)):
    try:
        await db.execute("INSERT INTO users (username, password) VALUES (:username, crypt(:password, gen_salt('md5')))", values={'username': user.username, 'password': user.password})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.",
        )

@router.get("/", status_code=200)
async def get_user_by_id(user: UserId, db=Depends(database.provide_connection)):
    return await db.fetch_one("SELECT username FROM user WHERE id=:id", values={"id": user.id})

@router.get("/list", status_code=200)
async def list_measurements(request: Request, db=Depends(database.provide_connection)):
    return await db.fetch_all("SELECT username FROM user")

@router.delete("/", status_code=200)
async def delete_measurement_by_id(user: User, db=Depends(database.provide_connection)):
    try:
        await db.execute("DELETE FROM user where id=:id", values={"id": user.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or user does not exist.",
        )