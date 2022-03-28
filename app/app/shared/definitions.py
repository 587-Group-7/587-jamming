import asyncpg
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID

class Robot(BaseModel):
    id: asyncpg.pgproto.pgproto.UUID
    alias: Optional[str] = None