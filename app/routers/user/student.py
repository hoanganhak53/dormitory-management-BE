from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (ChangePasswordRequest, ChangeProfileRequest, ChangeAnswerRequest, ChangeAvatarRequest)
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
    