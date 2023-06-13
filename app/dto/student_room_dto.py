from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.student_room import StudentRoomStatus
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)

class CreateStudentRoomRequest(BaseModel):
    user_id: Optional[str]
    registration_id: str
    room_type_id: str
    apartment_id: str
    status: StudentRoomStatus = StudentRoomStatus.DA_DANG_KY
    
class UpdateStudentRoomRequest(BaseModel):
    id: str
    status: StudentRoomStatus
