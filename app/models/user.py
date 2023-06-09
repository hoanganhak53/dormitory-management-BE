from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum

class UserType(int, RootEnum):
    STUDENT = 1
    MANAGER = 2
    ADMIN = 3
    
class GenderType(int, RootEnum):
    MALE = 1
    FAMALE = 2

class UserDataInput(BaseModel):
    email: str
    full_name: str
    mssv: str
    password: str
    user_type: UserType = UserType.STUDENT
    is_valid: bool = False
    is_more_info: bool = False
    room_id: Optional[str]
    major: Optional[str]
    gender: Optional[GenderType]
    avatar: Optional[str]
    batch: Optional[str]
    phonenumber: Optional[str]
    birth: Optional[datetime]
    answers: Optional[dict]
    

class UserData(RootModel, UserDataInput):
    class Collection:
        name = "user"
        indexes = [
            IndexModel(
                [
                    ("email", ASCENDING),
                ],
                unique=True,
            )
        ]