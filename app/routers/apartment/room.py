from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.room_dto import (CreateRoomRequest, UpdateRoomRequest)
from app.services.room_service import RoomService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated, List

route = APIRouter(tags=['Room'], prefix="/room")

@route.post('')
async def create_room(room_input: CreateRoomRequest, user_id: str = Depends(require_user)):
    room = await RoomService().post(room_input)
    
    return {
        "message": "Tạo phòng thành công",
        "data": room
    }
    
@route.put('')
async def update_room(room_input: UpdateRoomRequest, user_id: str = Depends(require_user)):
    room = await RoomService().put(room_input)
    
    return {
        "message": "Cập nhật phòng thành công",
        "data": room
    }
    

@route.get('/list')
async def get_list_room_data(user_id: str = Depends(require_user)):
    items, total = await RoomService().list()
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }
    
@route.get('/detail/{room_id}')
async def get_room_detail(room_id: str, user_id: str = Depends(require_user)):
    items = await RoomService().detail(room_id)
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items
    }
    
    
@route.post('/distribute')
async def distribute_room(rooms: List, user_id: str = Depends(require_user)):
    items, statistic = await RoomService().distribute(rooms)
    
    return {
        "message": "Phân chia thành công",
        "data": items,
        "statistic": statistic
    }

@route.put('/distribute')
async def save_distribute_room(rooms: List, user_id: str = Depends(require_user)):
    await RoomService().save_distribute(rooms)
    
    return {
        "message": "Dồn phòng thành công",
    }
    