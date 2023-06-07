from app.dto.common import BaseResponseData
from fastapi import APIRouter


router = APIRouter(tags=['Ping'])


@router.get(
    '/ping',
    response_model=BaseResponseData
)
async def check_health():
    return BaseResponseData(
        message='Server is working',
        data={'a': 1, 'b': 2})