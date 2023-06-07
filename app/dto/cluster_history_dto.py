from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.dto.common import (
    BasePaginationResponseData, BaseResponseData, BeanieDocumentWithId
)
from app.models.cluster_history import ClusterGroupData


# DTO for list response (Inherit BeanieDocumentWithId so the response include databaseID)
class ShortClusterHistory(BeanieDocumentWithId):
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


# DTO for detail response
class FullClusterHistory(ShortClusterHistory):
    children: List[ClusterGroupData]


class ClusterHistoryResponse(BaseResponseData):
    data: Optional[FullClusterHistory]


class ClusterHistoryPaginationData(BasePaginationResponseData):
    items: List[ShortClusterHistory]


class ClusterHistoryPaginationResponse(BaseResponseData):
    data: ClusterHistoryPaginationData


#DTO for update request
class ClusterHistoryPutRequest(BaseModel):
    name: str
    description: Optional[str]
    children: List[ClusterGroupData]