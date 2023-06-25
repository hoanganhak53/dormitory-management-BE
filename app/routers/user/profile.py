from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (ChangePasswordRequest, ChangeProfileRequest, ChangeAnswerRequest, ChangeAvatarRequest, AdminChangeRequest)
from app.services.user_service import UserService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.user import UserData
from app.models.room import RoomData
from app.models.apartment import ApartmentData
from app.models.student_room import StudentRoomData
from app.models.registration import RegistrationData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Profile'], prefix="/profile")

@route.get('/{target_id}')
async def get_me(target_id: str, user_id: str = Depends(require_user)):
    if target_id == 'me':
        user = await UserData.get(PydanticObjectId(str(user_id)))
    else:
        user = await UserData.get(PydanticObjectId(str(target_id)))
    
    user_dict = user.dict()
    if user.room_id is not None:
        room = await RoomData.find_one({'_id': PydanticObjectId(user.room_id)})
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(room.apartment_id)})
        if room is not None:
            user_dict['room_name'] = room.room_name
            student_room = await StudentRoomData.find_one({'room_id': str(room.id), 'user_id': str(user.id)})
            if student_room is not None:
                user_dict['apartment_name'] = apartment.apartment_name
                registration = await RegistrationData.find_one({'_id': PydanticObjectId(student_room.registration_id)})
                if registration is not None:
                    user_dict['registration'] = registration.dict()
    
    return {
        "message": "get user",
        "data": user_dict
    }


@route.put("/change/password")
async def change_password(passward_input: ChangePasswordRequest, user_id: str = Depends(require_user)):
    user_data = await UserService().changePassword(passward_input, user_id)
    return {
        "message": "Đổi mật khẩu thành công",
    }


@route.put("/change")
async def change(profile_input: Union[ChangeProfileRequest, ChangeAvatarRequest, ChangeAnswerRequest, AdminChangeRequest], user_id: str = Depends(require_user)):
    user_data = await UserService().change(profile_input, user_id)
 
    return {
        "message": "Cập nhật thông tin thành công",
        "data": user_data
    }