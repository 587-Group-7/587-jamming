# Database operations
from typing import Optional
from ..database import database
import asyncpg
from ..utils.manager import manager

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status, WebSocket, WebSocketDisconnect

# Type imports
from ..shared.definitions import User, Robot, RobotID

router = APIRouter(
    prefix="/robot",
    tags=["robot"],
    responses={404: {"description": "Not found"}}
)

class RobotAlias(BaseModel):
    alias: Optional[str] = None


@router.post("/", status_code=200)
async def create_robot(robot: RobotAlias, db=Depends(database.provide_connection)):
    try:
        return await db.execute("INSERT INTO robot (alias) VALUES (:alias) RETURNING id", values={"alias": "" if robot.alias == None else robot.alias})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.",
        )

@router.delete("/", status_code=200)
async def delete_robot(robot: RobotID, db=Depends(database.provide_connection)):
    try:
        await db.execute("DELETE FROM robot where id=:id", values={"id": robot.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id or resource doesn't exist.",
        )

@router.get("/", status_code=200)
async def get_robot_by_id(robot: RobotID, db=Depends(database.provide_connection)):
    return await db.fetch_one("SELECT alias FROM robot WHERE id=:id", values={"id": robot.id})

@router.get("/list", status_code=200)
async def list_robots(request: Request, db=Depends(database.provide_connection)):
    return await db.fetch_all("SELECT * FROM robot")

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db=Depends(database.provide_connection)):
    client = await db.fetch_one("SELECT alias FROM robot WHERE id=:id", values={"id": client_id})
    if (client is not None):
        try:
            await manager.connect(websocket, client_id)
            while True:
                incoming_message = await websocket.receive_json()
        except WebSocketDisconnect:
            manager.disconnect(websocket, client_id)
    return