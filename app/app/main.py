from fastapi import FastAPI, Request, Depends, WebSocket
from .shared import template
from .database import database
from .routers import robot, user, command, control, measurement
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

ROOTDIR = os.environ.get('ROOTDIR')
STATICDIR = "static" if ROOTDIR is None else ROOTDIR+"static"
app.mount("/static", StaticFiles(directory=STATICDIR), name="static")

TEMPLATEDIR = "templates" if ROOTDIR is None else ROOTDIR+"templates"
templates = Jinja2Templates(directory=TEMPLATEDIR)

app.include_router(robot.router)
app.include_router(user.router)
app.include_router(command.router)
app.include_router(control.router)
app.include_router(measurement.router)

@app.on_event("startup")
async def start():
    await database.startup()

@app.on_event("shutdown")
async def stop():
    await database.shutdown()

# Simple HTML example
# @app.get("/", response_class=HTMLResponse)
# async def read_items():
#     html_content = f"""
#     <html>
#         <head>
#             <title>Some HTML in here</title>
#         </head>
#         <body>
#             <h1>Look! HTML!</h1>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content, status_code=200)

# Templated HTML examples
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db=Depends(database.provide_connection)):
    users = await db.fetch_all("SELECT username FROM users")
    robots = await db.fetch_all("SELECT * FROM robot")
    return templates.TemplateResponse("index.html", {"request": request, "users": [dict(user)['username'] for user in users], "robots": [(dict(robot)['id'], dict(robot)['alias'])for robot in robots], "nav": template.NAVIGATION})

@app.get("/account", response_class=HTMLResponse)
async def create_account(request: Request):
    return templates.TemplateResponse("account.html", {"request": request, "nav": template.NAVIGATION})

@app.get("/login", response_class=HTMLResponse)
async def create_account(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "nav": template.NAVIGATION})

@app.get("/map", response_class=HTMLResponse)
async def create_account(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, "nav": template.NAVIGATION})

@app.get("/view_robots", response_class=HTMLResponse)
async def create_account(request: Request):
    return templates.TemplateResponse("robot.html", {"request": request, "nav": template.NAVIGATION, "robots": ["Red Robot", "Blue Robot"]})
    
@app.get("/robot_control/{robot_alias}", response_class=HTMLResponse)
async def create_account(request: Request, robot_alias):
    return templates.TemplateResponse("control.html", {"request": request, "nav": template.NAVIGATION, "robot": robot_alias})

@app.websocket("/ws")
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

@app.get("/ws-test")
async def get():
    return HTMLResponse(html)