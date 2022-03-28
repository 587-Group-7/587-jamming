# Database operations
from typing import Optional
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User, Robot

router = APIRouter(
    prefix="/robot",
    tags=["robot"],
    responses={404: {"description": "Not found"}}
)

class RobotAlias(BaseModel):
    alias: Optional[str] = None


@router.post("/", status_code=200)
async def create_control(robot: RobotAlias, db=Depends(database.provide_connection)):
    try:
        await db.execute("INSERT INTO robot (alias) VALUES (:alias)", values={"alias": "" if robot.alias == None else robot.alias})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.",
        )

@router.delete("/", status_code=200)
async def delete_control(robot: Robot, db=Depends(database.provide_connection)):
    try:
        await db.execute("DELETE FROM robot where id=:id", values={"id": robot.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id or resource doesn't exist.",
        )

@router.get("/", status_code=200)
async def get_control_by_robot_id(robot: Robot, db=Depends(database.provide_connection)):
    return await db.fetch_one("SELECT alias FROM robot WHERE id=:id", values={"id": robot.id})

@router.get("/list", status_code=200)
async def list_controls(request: Request, db=Depends(database.provide_connection)):
    return await db.fetch_all("SELECT * FROM control")