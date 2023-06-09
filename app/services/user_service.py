from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.user_dto import (UserRegisterRequest , UserLoginRequest, FullUserData, ShortUserData, 
    ChangePasswordRequest, ChangeProfileRequest, ChangeAvatarRequest, ChangeAnswerRequest)
from app.models.user import UserData
from fastapi import HTTPException, status

class UserService:

    async def register(
        self,
        register_input: UserRegisterRequest
    ):
        user_data = await UserData.find_one({'email': register_input.email}).project(FullUserData)
        if user_data:
            raise Exception("Trùng địa chỉ email")
        user_dict = register_input.dict()
        model = UserData(**user_dict)
        await model.save()
        return str(model.id)


    async def login(
        self,
        login_input: UserLoginRequest
    ):
        user_data = await UserData.find_one({'email': login_input.email, 'password': login_input.password}).project(ShortUserData)
        if not user_data:
            raise Exception("Email hoặc mật khẩu không chính xác")
        return user_data


    async def changePassword(
        self,
        password_input: ChangePasswordRequest,
        user_id: str
    ):
        user = await UserData.get(PydanticObjectId(str(user_id)))
        if not user.password == password_input.old_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Mật khẩu cũ không chính xác')
        
        await user.update(**password_input)

        return user


    async def change(
        self,
        profile_input: Union[ChangeProfileRequest, ChangeAvatarRequest, ChangeAnswerRequest],
        user_id: str
    ):
        user = await UserData.get(PydanticObjectId(str(user_id)))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tài khoản không tổn tại')
        
        await user.update(**profile_input)

        return user
