from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.student_room_dto import (CreateStudentRoomRequest, UpdateStudentRoomRequest)
from app.services.student_room_service import StudentRoomService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['StudentRoom'], prefix="/student_room")

@route.post('')
async def register_room(student_room_input: CreateStudentRoomRequest, user_id: str = Depends(require_user)):
    student_room = await StudentRoomService().post(student_room_input, user_id)
    
    return {
        "message": "Đăng ký phòng thành công",
        "data": student_room
    }
    
#only change status
@route.put('')
async def update_student_room(student_room_input: UpdateStudentRoomRequest, user_id: str = Depends(require_user)):
    student_room = await StudentRoomService().put(student_room_input)
    
    return {
        "message": "Cập nhật đăng ký thành công",
        "data": student_room
    }
    

@route.get('/list')
async def get_list_student_room_data(user_id: str = Depends(require_user)):
    items, total = await StudentRoomService().list()
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }


@route.get('/current')
async def get_current_room_data(user_id: str = Depends(require_user)):
    roommates, room_current = await StudentRoomService().current(user_id)
    
    return {
        "message": "Lấy danh sách thành công",
        "data": roommates,
        "current": room_current
    }
