from enum import Enum
from fastapi import FastAPI, Request, HTTPException, Depends, status
from .database import database
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncpg

import http

class Measurement(BaseModel):
    lat: float
    lng: float
    intensity: float
    robot_id: asyncpg.pgproto.pgproto.UUID

class MeasurementId(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID

class Movement(BaseModel):
    duration: int
    speed: int

class Rotation(BaseModel):
    angle: int

class User(BaseModel):
    user_id: asyncpg.pgproto.pgproto.UUID

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# @app.on_event("startup")
# async def start():
#     await database.startup()

# @app.on_event("shutdown")
# async def stop():
#     await database.shutdown()

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

# Templated HTML
@app.get("/leaflet", response_class=HTMLResponse)
async def control(request: Request):
    return templates.TemplateResponse("leaflet.html", {"request": request})

@app.post("/control", status_code=200)
async def create_control(user: User):
    pass

@app.post("/movement", status_code=200)
async def movement(movement: Movement):
    # Robot runner code here. Translate the forward movement to actual robot movement
    pass

@app.post("/rotation", status_code=200)
async def rotation(rotation: Rotation):
    # Robot rotation here
    pass

# Simple json example
@app.get("/json", status_code=200)
async def root(request: Request):
    return {"Hello": "World"}

@app.post("/measurement", status_code=201)
async def create_measurement(measurement: Measurement):
    pass

@app.get("/measurement", status_code=201)
async def get_measurement_by_id(id: MeasurementId):
    pass

@app.get("/measurements", status_code=201)
async def get_measurements(request: Request):
    pass

@app.delete("/measurement", status_code=201)
async def delete_measurement_by_id(id: MeasurementId):
    pass