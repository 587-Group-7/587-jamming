import asyncpg
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID

class Robot(BaseModel):
    alias: Optional[str] = None

class RobotID(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID

class Control(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID