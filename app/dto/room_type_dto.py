from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.user import UserType, GenderType
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)

class CreateRoomTypeRequest(BaseModel):
    room_type_name: str
    room_price: str
    capacity: int
    gender: GenderType
    
class UpdateRoomTypeRequest(CreateRoomTypeRequest):
    id: str