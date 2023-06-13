from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (ChangePasswordRequest, ChangeProfileRequest, ChangeAnswerRequest, ChangeAvatarRequest)
from app.services.user_service import UserService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['UserType'], prefix="/user_type")

@route.get('/{user_type}')
async def get_list_data_by_type(user_type: int, user_id: str = Depends(require_user)):
    users = await UserService().getUserListByType(user_type)
    return {
        "message": "get user type",
        "data": users
    }

@route.post('/students/{apartment_id}')
async def get_list_students_by_apartment(apartment_id: str, user_id: str = Depends(require_user)):
    users = await UserService().getStudentListByApartment(apartment_id)
    return {
        "message": "get list students",
        "data": users
    }
