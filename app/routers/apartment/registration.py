from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.registration_dto import (CreateRegistrationRequest, UpdateRegistrationRequest)
from app.services.registration_service import RegistrationService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Registration'], prefix="/registration")

@route.post('')
async def create_registration(registration_input: CreateRegistrationRequest, user_id: str = Depends(require_user)):
    registration = await RegistrationService().post(registration_input)
    
    return {
        "message": "Tạo đợt đăng ký thành công",
        "data": registration
    }
    
@route.put('')
async def update_registration(registration_input: UpdateRegistrationRequest, user_id: str = Depends(require_user)):
    registration = await RegistrationService().put(registration_input)
    
    return {
        "message": "Cập nhật đợt đăng ký thành công",
        "data": registration
    }
    

@route.get('/list')
async def get_list_registration_data(user_id: str = Depends(require_user)):
    items, total = await RegistrationService().list()
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }
    
@route.get('/current')
async def get_current_registration_data(user_id: str = Depends(require_user)):
    rooms, current = await RegistrationService().current(user_id)
    
    return {
        "message": "Lấy đợt đăng ký hiện tại thành công",
        "data": rooms,
        "registration": current
    }