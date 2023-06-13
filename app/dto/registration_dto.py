from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.user import UserType, GenderType
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)

class CreateRegistrationRequest(BaseModel):
    registration_name: str
    start_date: datetime
    end_date: datetime
    start_register: datetime
    end_register: datetime
    paid_date: datetime
    semester: str
    
class UpdateRegistrationRequest(CreateRegistrationRequest):
    id: str