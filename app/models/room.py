from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum


class RoomDataInput(BaseModel):
    room_name: str
    room_type_id: str
    apartment_id: str

class RoomData(RootModel, RoomDataInput):
    class Collection:
        name = "room"
        indexes = [
            IndexModel(
                [
                    ("room_type_id", ASCENDING),
                ],
            )
        ]