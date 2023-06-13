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