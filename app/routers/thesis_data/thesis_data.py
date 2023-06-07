from fastapi import APIRouter, Query
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.thesis_data_dto import (ThesisDataResponse, ThesisDataPaginationResponse, ThesisDataPaginationData, ThesisDataCreateRequest)
from app.services.thesis_data_service import ThesisDataService

route = APIRouter(tags=['Thesis Data'], prefix="/thesis_data")


@route.get(
    '/list',
    response_model=ThesisDataPaginationResponse,
)
async def get_list_thesis_data(
    title: str = Query(None),
    semester: str = Query(None),
    created_at: str = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    items, total = await ThesisDataService().list(
        title=title,
        semester=semester,
        created_at=created_at,
        page=page,
        limit=limit,
    )

    return ThesisDataPaginationResponse(
        message="Get list thesis successfully",
        data=ThesisDataPaginationData(
            items=items,
            total=total,
        )
    )


@route.get(
    '/{thesis_id}',
    response_model=ThesisDataResponse
)
async def get_thesis_data_by_id(
    thesis_id: str,
):
    thesis_data = await ThesisDataService().get(
        thesis_id=thesis_id,
    )

    return ThesisDataResponse(
        message="Get thesis successfully",
        data=thesis_data
    )


@route.post(
    '/create',
    response_model=BaseResponseData,
)
async def create_thesis_data(
    thesis_input: ThesisDataCreateRequest,
):
    created_thesis_id = await ThesisDataService().create(
        thesis_input=thesis_input,
    )
    return BaseResponseData(
        message="Created thesis successfully",
        data=created_thesis_id
    )


@route.delete(
    '/{thesis_id}',
    response_model=BaseResponse
)
async def delete_thesis_by_id(
    thesis_id: str
):
    await ThesisDataService().delete(
        thesis_id=thesis_id
    )

    return BaseResponse(
        message="Deleted thesis successfully"
    )