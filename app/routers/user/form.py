from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.form_dto import (CreateFormRequest, UpdateFormRequest)
from app.services.form_service import FormService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.form import FormData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Form'], prefix="/form")

@route.get('/list')
async def get_list_form_data(user_id: str = Depends(require_user)):
    items, total = await FormService().list()
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }

@route.post('')
async def create_form(form_input: CreateFormRequest, user_id: str = Depends(require_user)):
    form = await FormService().post(form_input)
    return {
        "message": "Tạo bài câu hỏi thành công",
        "data": form
    }


@route.put('')
async def update_form(form_input: UpdateFormRequest, user_id: str = Depends(require_user)):
    form = await FormService().put(form_input)
    return {
        "message": "Cập nhật câu hỏi thành công",
        "data": form
    }

@route.delete('/{form_id}')
async def remove_form(form_id: str, user_id: str = Depends(require_user)):
    await FormService().delete(form_id)
    return {
        "message": "Xóa câu hỏi thành công",
    }
