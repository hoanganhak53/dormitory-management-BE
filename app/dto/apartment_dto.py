from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.user import UserType, GenderType
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)

class CreateApartmentRequest(BaseModel):
    apartment_name: str
    manager_id: str
    
class UpdateApartmentRequest(CreateApartmentRequest):
    id: str
    
    
class GetStudentNoRoom(BaseModel):
    apartment_id: str
    room_type_id: str
    
class AddStudentToRoom(BaseModel):
    user_id: str
    student_room_id: str
    room_id: str
    
class RemoveStudentToRoom(BaseModel):
    user_id: str
    room_id: str
    
class ClusterStudent(BaseModel):
    apartment_id: str
    room_type_name: str
    fuzzy_m: float
    max_loop: int
    epsilon: float