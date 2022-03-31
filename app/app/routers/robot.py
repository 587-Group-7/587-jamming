# Database operations
from typing import Optional
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status, WebSocket

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
        await db.execute("INSERT INTO robot (alias) VALUES (:alias)", values={"alias": "" if robot.alias == None else robot.alias})
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

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:3000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

# @router.get("/ws-test")
# async def get():
#     return HTMLResponse(html)