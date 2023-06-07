from typing import Union, Optional, List
from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class BaseResponse(BaseModel):
    error_code: int = 0
    message: str = ''


class BaseResponseData(BaseResponse):
    data: Union[dict, str, int, None]


class BasePaginationRequest(BaseModel):
    limit: Optional[int] = 25
    page: Optional[int] = 1


class BasePaginationResponseData(BaseModel):
    total: int
    items: List


class BeanieDocumentWithId(BaseModel):
    id: PydanticObjectId = Field(alias='_id')