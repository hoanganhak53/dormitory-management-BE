from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum

class StudentRoomStatus(int, RootEnum):
    DA_DANG_KY = 1
    DA_NOP = 2
    DA_SAP_XEP = 3


class StudentRoomDataInput(BaseModel):
    user_id: str
    registration_id: str
    room_id: str
    apartment_id: str
    room_type_id: str
    status: StudentRoomStatus = StudentRoomStatus.DA_DANG_KY
    created_date: datetime
    

class StudentRoomData(RootModel, StudentRoomDataInput):
    class Collection:
        name = "student_room"
        indexes = [
            IndexModel(
                [
                    ("registration_id", ASCENDING),
                    ("apartment_id", ASCENDING),
                ],
            )
        ]