from fastapi import FastAPI, Request
from .database import database
from .routers import robot, user, command, control, measurement
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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
@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Templated HTML examples
@app.get("/control", response_class=HTMLResponse)
async def control(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": 1234})