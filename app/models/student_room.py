from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum

class StudentRoomStatus(int, RootEnum):
    DA_DANG_KY = 1
    DA_NOP = 2
    DA_SAP_XEP = 3
    DA_HUY = 4
    #neu chuyen thanh da huy thi phai xoa room id cua user neu ko se la tiep tuc gia han dang ky


class StudentRoomDataInput(BaseModel):
    user_id: str
    registration_id: str
    room_id: Optional[str]
    room_type_id: str
    apartment_id: str
    status: StudentRoomStatus = StudentRoomStatus.DA_DANG_KY
    

class StudentRoomData(RootModel, StudentRoomDataInput):
    class Collection:
        name = "student_room"
        indexes = [
            IndexModel(
                [
                    ("registration_id", ASCENDING),
                    ("apartment_id", ASCENDING),
                    ("room_type_id", ASCENDING),
                ],
            )
        ]