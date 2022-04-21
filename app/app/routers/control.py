# Database operations
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User, Robot, Control, RobotID

# Auth utils
from ..utils.auth import get_current_user

from ..utils.manager import manager

router = APIRouter(
    prefix="/control",
    tags=["control"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=200)
async def create_control(robot: RobotID, user = Depends(get_current_user)):
    result = await manager.pair_client(user['id'], robot.id)
    if (result[0]):
        return result[1]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Malformed request: {result[1]}",
        )

@router.delete("/", status_code=200)
async def delete_control(user = Depends(get_current_user)):
    await manager.client_release_connection(user['id'])

@router.get("/", status_code=200)
async def get_control_by_user_id(user = Depends(get_current_user), db = Depends(database.provide_connection)):
    result = manager.get_connection_by_client_id(user['id'])
    if (result is not None):
        return await db.fetch_one("SELECT alias, id FROM robot WHERE id=:id", values={"id": result})
    else:
        return None

@router.get("/list", status_code=200)
async def list_controls():
    return manager.get_available_active_connections()


# *** Control used to be based on database records. This  is deprecated, but kept for possible future improvement. A new stateful implementation is designed above. ***
# @router.post("/", status_code=200)
# async def create_control(robot: RobotID, user = Depends(get_current_user), db = Depends(database.provide_connection)):
#     try:
#         return await db.fetch_one("INSERT INTO control (userId, robotId) VALUES (:userId, :robotId) RETURNING id", values={"userId": user["id"], "robotId": robot.id})
#     except asyncpg.exceptions.DataError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid user or robot id, or robot already under control.",
#         )

# @router.delete("/", status_code=200)
# async def delete_control(control: Control, db=Depends(database.provide_connection)):
#     try:
#         await db.execute("DELETE FROM control where id=:id", values={"id": control.id})
#     except asyncpg.exceptions.DataError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid control id.",
#         )

# @router.get("/", status_code=200)
# async def get_control_by_robot_id(control: Control, db=Depends(database.provide_connection)):
#     async with db.transaction():
#         return await db.fetch_one("SELECT userId, robotId FROM control WHERE id=:id", values={"id": control.id})

# @router.get("/user", status_code=200)
# async def get_control_by_user_id(user = Depends(get_current_user), db=Depends(database.provide_connection)):
#     async with db.transaction():
#         return await db.fetch_all("SELECT robotId FROM control WHERE userId=:userId", values={"userId": user["id"]})

# @router.get("/list", status_code=200)
# async def list_controls(db=Depends(database.provide_connection)):
#     async with db.transaction():
#         return await db.fetch_all("SELECT userId, robotId FROM control")
