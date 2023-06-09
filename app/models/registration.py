from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum

class RegistrationDataInput(BaseModel):
    registration_name: str
    start_date: datetime
    end_date: datetime
    start_register: datetime
    end_register: datetime
    paid_date: datetime
    semester: str
    

class RegistrationData(RootModel, RegistrationDataInput):
    class Collection:
        name = "registration"
        indexes = [
            IndexModel(
                [
                    ("paid_date", ASCENDING),
                ],
            )
        ]