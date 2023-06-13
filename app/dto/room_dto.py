from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.user import UserType, GenderType
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)

class CreateRoomRequest(BaseModel):
    room_name: str
    room_type_id: str
    apartment_id: str
    
class UpdateRoomRequest(CreateRoomRequest):
    id: str