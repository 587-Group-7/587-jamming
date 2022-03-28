# Database operations
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User, Robot

router = APIRouter(
    prefix="/control",
    tags=["control"],
    responses={404: {"description": "Not found"}}
)

class Control(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID


@router.post("/", status_code=200)
async def create_control(user: User, robot: Robot, db=Depends(database.provide_connection)):
    try:
        await db.execute("INSERT INTO control (userId, robotId) VALUES userId=:userId, robotId=:robotId", values={"userId": user.id, "robotId": robot.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or robot id, or robot already under control.",
        )

@router.delete("/", status_code=200)
async def delete_control(control: Control, db=Depends(database.provide_connection)):
    try:
        await db.execute("DELETE FROM control where id=:id", values={"id": control.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid control id.",
        )

@router.get("/", status_code=200)
async def get_control_by_robot_id(control: Control, db=Depends(database.provide_connection)):
    async with db.transaction():
        return await db.fetch_one("SELECT userId, robotId FROM control WHERE id=:id", values={"id": control.id})

@router.get("/list", status_code=200)
async def list_controls(db=Depends(database.provide_connection)):
    async with db.transaction():
        return await db.fetch_all("SELECT userId, robotId FROM control")
