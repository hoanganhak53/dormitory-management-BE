from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.post import PostStatus
from app.dto.common import (
    BaseResponseData, BeanieDocumentWithId
)

class CreatePostRequest(BaseModel):
    image: str
    title: str
    content: str
    status: PostStatus = PostStatus.ACTIVE
    
class UpdatePostRequest(CreatePostRequest):
    id: str