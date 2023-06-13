from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime
from .user import GenderType

from app.models.base import RootModel, RootEnum


class RoomTypeDataInput(BaseModel):
    room_type_name: str
    room_price: str
    capacity: int
    gender: GenderType
    

class RoomTypeData(RootModel, RoomTypeDataInput):
    class Collection:
        name = "room_type"
        indexes = [
            IndexModel(
                [
                    ("capacity", ASCENDING),
                ],
            )
        ]