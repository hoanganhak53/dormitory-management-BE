from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum


class ApartmentDataInput(BaseModel):
    apartment_name: str
    total_student: int = 0
    total_room: int = 0
    manager_id: str
    

class ApartmentData(RootModel, ApartmentDataInput):
    class Collection:
        name = "apartment"
        indexes = [
            IndexModel(
                [
                    ("apartment_name", ASCENDING),
                ],
                unique=True,
            )
        ]