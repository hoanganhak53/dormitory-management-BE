from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)
from app.models.form import FormType

class CreateFormRequest(BaseModel):
    question: str
    answers: List
    weight: str
    form_type: FormType = FormType.RADIO
    matrix: dict
    
class UpdateFormRequest(CreateFormRequest):
    id: str