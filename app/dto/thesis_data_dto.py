from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.dto.common import (
    BasePaginationResponseData, BaseResponseData, BeanieDocumentWithId
)


class ThesisStudentData(BaseModel):
    student_name: str
    student_id: str


# DTO for list response (Inherit BeanieDocumentWithId so the response include databaseID)
class ShortThesisData(BeanieDocumentWithId):
    semester: str
    title: str
    student_data: ThesisStudentData


# DTO for detail response
class FullThesisData(ShortThesisData):
    category: str
    expected_result: str
    problem_solve: str
    created_at: datetime


class ThesisDataResponse(BaseResponseData):
    data: Optional[FullThesisData]


class ThesisDataPaginationData(BasePaginationResponseData):
    items: List[ShortThesisData]


class ThesisDataPaginationResponse(BaseResponseData):
    data: ThesisDataPaginationData


# Body format for post request
class ThesisDataCreateRequest(BaseModel):
    semester: str
    title: str
    category: str
    expected_result: str
    problem_solve: str
    student_data: ThesisStudentData