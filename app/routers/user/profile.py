from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (ChangePasswordRequest, ChangeProfileRequest, ChangeAnswerRequest, ChangeAvatarRequest)
from app.services.user_service import UserService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Profile'], prefix="/profile")

@route.get('/{target_id}')
async def get_me(target_id: str, user_id: str = Depends(require_user)):
    if target_id == 'me':
        user = await UserData.get(PydanticObjectId(str(user_id)))
    else:
        user = await UserData.get(PydanticObjectId(str(target_id)))
        
    return {
        "message": "get user",
        "data": user
    }


@route.put("/change/password")
async def change_password(passward_input: ChangePasswordRequest, user_id: str = Depends(require_user)):
    user_data = await UserService().changePassword(passward_input, user_id)
    return {
        "message": "Đổi mật khẩu thành công",
    }


@route.put("/change")
async def change(profile_input: Union[ChangeProfileRequest, ChangeAvatarRequest, ChangeAnswerRequest], user_id: str = Depends(require_user)):
    user_data = await UserService().change(profile_input, user_id)
 
    return {
        "message": "Cập nhật thông tin thành công",
        "data": user_data
    }
    