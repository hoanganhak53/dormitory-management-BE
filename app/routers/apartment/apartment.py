from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.apartment_dto import (CreateApartmentRequest, UpdateApartmentRequest)
from app.services.apartment_service import ApartmentService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Apartment'], prefix="/apartment")

@route.post('')
async def create_apartment(apartment_input: CreateApartmentRequest, user_id: str = Depends(require_user)):
    apartment = await ApartmentService().post(apartment_input)
    
    return {
        "message": "Tạo tòa nhà thành công",
        "data": apartment
    }
    
@route.put('')
async def update_apartment(apartment_input: UpdateApartmentRequest, user_id: str = Depends(require_user)):
    apartment = await ApartmentService().put(apartment_input)
    
    return {
        "message": "Cập nhật tòa nhà thành công",
        "data": apartment
    }
    

@route.get('/list')
async def get_list_apartment_data(user_id: str = Depends(require_user)):
    items, total = await ApartmentService().list()
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }
    
@route.get('/{apartment_id}')
async def get_apartment_by_id_data(apartment_id: str, user_id: str = Depends(require_user)):
    apartment, rooms = await ApartmentService().detail(apartment_id)
    
    return {
        "message": "Lấy danh sách thành công",
        "data": apartment,
        "rooms": rooms
    }

@route.get('/registration/{apartment_id}')
async def get_registration_by_apartment(apartment_id: str, user_id: str = Depends(require_user)):
    items, apartment = await ApartmentService().registration_by_apartment(apartment_id)
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "apartment": apartment
    }