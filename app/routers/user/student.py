from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (ChangePasswordRequest, ChangeProfileRequest, ChangeAnswerRequest, ChangeAvatarRequest)
from app.dto.apartment_dto import (GetStudentNoRoom, AddStudentToRoom, RemoveStudentToRoom)
from app.services.student_service import StudentService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Student'], prefix="/student")

@route.put("/toggle/valid/{student_id}")
async def change(student_id: str, user_id: str = Depends(require_user)):
    user_data = await StudentService().toggleValid(student_id)
 
    return {
        "message": "Cập nhật trạng thái sinh viên thành công",
        "data": user_data
    }
    
    
@route.get("/registration_list")
async def registration_list(user_id: str = Depends(require_user)):
    registration_data = await StudentService().registration_list(user_id)
 
    return {
        "message": "Danh sách đăng ký các kỳ",
        "data": registration_data
    }
    
    
@route.post("/no_room")
async def student_no_room(no_room_input: GetStudentNoRoom, user_id: str = Depends(require_user)):
    students = await StudentService().no_room(no_room_input)
 
    return {
        "message": "Danh sách sinh viên chưa được xếp phòng",
        "data": students
    }


@route.post("/add_to_room")
async def add_student_to_room(add_student_input: AddStudentToRoom, user_id: str = Depends(require_user)):
    student = await StudentService().add_to_room(add_student_input)
 
    return {
        "message": "Thêm sinh viên vào phòng",
        "data": student
    }


@route.post("/remove_to_room")
async def remove_student_to_room(remove_student_input: RemoveStudentToRoom, user_id: str = Depends(require_user)):
    student = await StudentService().remove_to_room(remove_student_input)
 
    return {
        "message": "Xóa sinh viên vào phòng khỏi",
        "data": student
    }
    