# Database operations
from ..database import database
import asyncpg

# Pydantic typing
from pydantic import BaseModel

# Framework imports
from fastapi import APIRouter, Depends, Request, HTTPException, status

# Type imports
from ..shared.definitions import User

# Local definitions


class Measurement(BaseModel):
    lat: float
    lng: float
    intensity: float
    robot_id: asyncpg.pgproto.pgproto.UUID


class MeasurementId(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID


router = APIRouter(
    prefix="/measurement",
    tags=["measurement"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=201)
async def create_measurement(measurement: Measurement, db=Depends(database.provide_connection)):
    try:
        await db.execute("INSERT INTO jaminfo (lat, lng, intensity, robot_id) VALUES lat=:lat, lng=:lng, intensity=:intensity, robot_id=:robot_id", values={"lat": measurement.lat, "lng": measurement.lng, "intensity": measurement.intensity, "robot_id": measurement.robot_id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed measurement.",
        )


@router.get("/", status_code=201)
async def get_measurement_by_id(id: MeasurementId, db=Depends(database.provide_connection)):
    return await db.fetch_one("SELECT lat, lng, intensity, robot_id FROM control WHERE id=:id", values={"id": id.id})

@ router.get("/list", status_code=201)
async def list_measurements(request: Request, db=Depends(database.provide_connection)):
    return await db.fetch_all("SELECT lat, lng, intensity, robot_id FROM control")

@ router.delete("/", status_code=201)
async def delete_measurement_by_id(id: MeasurementId, db=Depends(database.provide_connection)):
    try:
        await db.execute("DELETE FROM control where id=:id", values={"id": id.id})
    except asyncpg.exceptions.DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid control id.",
        )
