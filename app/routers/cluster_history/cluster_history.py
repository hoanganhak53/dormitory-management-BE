from fastapi import APIRouter, Query
from app.dto.common import BaseResponse
from app.dto.cluster_history_dto import (ClusterHistoryResponse, ClusterHistoryPaginationData, ClusterHistoryPaginationResponse, ClusterHistoryPutRequest)
from app.services.cluster_history_service import ClusterHistoryService


route = APIRouter(tags=['Cluster History'], prefix="/cluster_history")


@route.get(
    '/list',
    response_model=ClusterHistoryPaginationData
)
async def get_list_cluster_history(
    name: str = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    items, total = await ClusterHistoryService().list(
        name=name,
        page=page,
        limit=limit,
    )

    return ClusterHistoryPaginationResponse(
        message="Get list history successfully",
        data=ClusterHistoryPaginationData(
            items=items,
            total=total,
        )
    )


@route.get(
    '/{cluster_history_id}',
)
async def get_history_by_id(
    cluster_history_id: str,
):
    history_data = await ClusterHistoryService().get(
        cluster_history_id=cluster_history_id,
    )

    return ClusterHistoryResponse(
        message="Get history data successfully",
        data=history_data
    )


@route.put(
    '/{cluster_history_id}',
)
async def update_cluster_history_data(
    cluster_history_id: str,
    update_history_data: ClusterHistoryPutRequest,
):
    updated_data = await ClusterHistoryService().put(
        cluster_history_id=cluster_history_id,
        new_cluster_history=update_history_data,
    )
    return ClusterHistoryResponse(
        message="Updated history data successfully",
        data=updated_data
    )


@route.delete(
    '/{cluster_history_id}',
)
async def delete_cluster_history_by_id(
    cluster_history_id: str,
):
    await ClusterHistoryService().delete(
        cluster_history_id=cluster_history_id,
    )
    return BaseResponse(
        message="Deleted history data successfully"
    )