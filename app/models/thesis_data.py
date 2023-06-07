from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel


class ThesisStudentData(BaseModel):
    student_name: str
    student_id: str


class ThesisDataInput(BaseModel):
    semester: str
    title: str
    title_vector: Optional[List]
    category: str
    category_vector: Optional[List]
    expected_result: str
    expected_result_vector: Optional[List]
    problem_solve: str
    problem_solve_vector: Optional[List]
    student_data: ThesisStudentData
    

class ThesisData(RootModel, ThesisDataInput):
    class Collection:
        name = "thesis_data"
        indexes = [
            IndexModel(
                [
                    ("semester", ASCENDING),
                ],
                unique=False,
            )
        ]

    need_nlp_extract: bool = True