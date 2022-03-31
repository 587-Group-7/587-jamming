from fastapi import FastAPI, Request, Depends
from .shared import template
from .database import database
from .routers import robot, user, command, control, measurement
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
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

# map requests
# the whole map
@app.get("/map", response_class=HTMLResponse)
async def create_account(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, "nav": template.NAVIGATION})

@app.get("/map2", response_class=HTMLResponse)
async def create_account(request: Request):
    return templates.TemplateResponse("map2.html", {"request": request, "nav": template.NAVIGATION})

#map hotpoints
@app.get("/mapped")
async def mapped(robot: Optional[str] = "", oldest: Optional[str]="", newest: Optional[str]="", db=Depends(database.provide_connection)):
    # TODO: not dealing with date ranges yet (oldest to newest)
    if (robot == ""):
        result = await db.fetch_all(
            "SELECT lat, lng, intensity FROM jaminfo")
    else:
        d = {'robot': robot}
        result = await db.fetch_all(
            """SELECT lat, lng, intensity FROM jaminfo JOIN robot on jaminfo.robotId = robot.id 
            WHERE robot.alias=:robot""",d)
    return result


@app.get("/view_robots", response_class=HTMLResponse)
async def create_account(request: Request, db=Depends(database.provide_connection)):
    robots = await db.fetch_all("SELECT * FROM robot")
    return templates.TemplateResponse("robot.html", {"request": request, "nav": template.NAVIGATION, "robots": [(dict(robot)['id'], dict(robot)['alias'])for robot in robots]})
    
@app.get("/robot-control/id/{id}/alias/{robot_alias}", response_class=HTMLResponse)
async def create_account(request: Request, robot_alias):
    return templates.TemplateResponse("control.html", {"request": request, "nav": template.NAVIGATION, "robot": robot_alias})

@app.get("/create-test-robot", response_class=HTMLResponse)
async def create_robot_test(request: Request):
    return templates.TemplateResponse("create-robot-test.html", {"request": request, "nav": template.NAVIGATION})