from typing import Optional, List
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel
from datetime import datetime

from app.models.base import RootModel, RootEnum

class PostStatus(int, RootEnum):
    ACTIVE = 1
    DEACTIVE = 2


class PostDataInput(BaseModel):
    user_id: str
    image: str
    title: str
    content: str
    created_date: datetime
    status: PostStatus = PostStatus.ACTIVE
    

class PostData(RootModel, PostDataInput):
    class Collection:
        name = "post"
        indexes = [
            IndexModel(
                [
                    ("created_date", ASCENDING),
                ],
            )
        ]