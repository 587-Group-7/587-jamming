# Database operations
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User

# Auth utils
from ..utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, Login, auth
from datetime import datetime, timedelta

# Local definitions
class UserId(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class Create(BaseModel):
    username: str
    password: str

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=201)
async def create_user(user: Create, db=Depends(database.provide_connection)):
    try:
        await db.execute("INSERT INTO users (username, password) VALUES (:username, crypt(:password, gen_salt('md5')))", values={'username': user.username, 'password': user.password})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.",
        )

@router.get("/", status_code=200)
async def get_user_by_id(user: UserId, db=Depends(database.provide_connection)):
    return await db.fetch_one("SELECT username FROM users WHERE id=:id", values={"id": user.id})

@router.get("/list", status_code=200)
async def list_measurements(request: Request, db=Depends(database.provide_connection)):
    return await db.fetch_all("SELECT username FROM users")

@router.delete("/", status_code=200)
async def delete_measurement_by_id(user: User, db=Depends(database.provide_connection)):
    try:
        await db.execute("DELETE FROM users where id=:id", values={"id": user.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or user does not exist.",
        )

@router.post("/login", response_model=Token)
async def login(auth_id: str = Depends(authenticate_user)):
    if not auth_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"id": auth_id}, expiry=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(user = Depends(get_current_user)):
    if (user):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
            data={"id": str(dict(user)['id'])}, expiry=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}