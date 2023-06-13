from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.room_type_dto import (CreateRoomTypeRequest, UpdateRoomTypeRequest)
from app.services.room_type_service import RoomTypeService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['RoomType'], prefix="/room_type")

@route.post('')
async def create_room_type(room_type_input: CreateRoomTypeRequest, user_id: str = Depends(require_user)):
    room_type = await RoomTypeService().post(room_type_input)
    
    return {
        "message": "Tạo tòa loại phòng thành công",
        "data": room_type
    }
    
@route.put('')
async def update_room_type(room_type_input: UpdateRoomTypeRequest, user_id: str = Depends(require_user)):
    room_type = await RoomTypeService().put(room_type_input)
    
    return {
        "message": "Cập nhật loại phòng thành công",
        "data": room_type
    }
    

@route.get('/list')
async def get_list_room_type_data(user_id: str = Depends(require_user)):
    items, total = await RoomTypeService().list()
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }