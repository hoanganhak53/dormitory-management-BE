from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.user import UserType, GenderType
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)


class UserRegisterRequest(BaseModel):
    email: str
    full_name: str
    mssv: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str

class ChangePasswordRequest(BaseModel):
    password: str
    old_password: str

class ChangeProfileRequest(BaseModel):
    full_name: str
    mssv: str
    batch: str
    phonenumber: str
    birth: str
    major: str
    gender: GenderType

class ChangeAvatarRequest(BaseModel):
    avatar: str
    
class ChangeAnswerRequest(BaseModel):
    answers: dict
    
class ShortUserData(BeanieDocumentWithId):
    email: str
    full_name: str
    mssv: str
    user_type: UserType = UserType.STUDENT
    avatar: Optional[str]


class FullUserData(ShortUserData):
    is_valid: bool = False
    is_more_info: bool = False
    room_id: Optional[str]
    major: Optional[str]
    gender: Optional[GenderType]
    batch: Optional[str]
    phonenumber: Optional[str]
    birth: Optional[str]
    answers: Optional[dict]


class UserDataResponse(BaseResponseData):
    data: FullUserData

