from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum


class FormType(int, RootEnum):
    CHECKBOX = 1
    RADIO = 2


class FormDataInput(BaseModel):
    question: str
    answers: List
    weight: str
    form_type: FormType = FormType.RADIO
    matrix: dict
    

class FormData(RootModel, FormDataInput):
    class Collection:
        name = "form"
        indexes = [
            IndexModel(
                [
                    ("question", ASCENDING),
                ],
                unique=True
            )
        ]