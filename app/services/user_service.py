from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.user_dto import (UserRegisterRequest , UserLoginRequest, FullUserData, ShortUserData, 
    ChangePasswordRequest, ChangeProfileRequest, ChangeAvatarRequest, ChangeAnswerRequest)
from app.models.user import UserData
from app.models.room import RoomData
from app.models.apartment import ApartmentData
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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Email hoặc mật khẩu không chính xác')
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
        
        user.password = password_input.password
        await user.update({"$set": {"password" : password_input.password}})

        return user.dict()


    async def change(
        self,
        profile_input: Union[ChangeProfileRequest, ChangeAvatarRequest, ChangeAnswerRequest],
        user_id: str
    ):
        user = await UserData.get(PydanticObjectId(str(user_id)))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tài khoản không tổn tại')
        
        common_keys = set(user.dict().keys()).intersection(profile_input.dict().keys())

        for key in common_keys:
            setattr(user, key, getattr(profile_input, key))
        
        if profile_input.dict().get('answers') is not None:
            user.is_more_info = True
        
        await user.update(
            { "$set":
                {
                    "email": user.email,
                    "full_name": user.full_name,
                    "mssv": user.mssv,
                    "user_type": user.user_type,
                    "is_valid": user.is_valid,
                    "is_more_info": user.is_more_info,
                    "room_id": user.room_id,
                    "major": user.major,
                    "gender": user.gender,
                    "avatar": user.avatar,
                    "batch": user.batch,
                    "phonenumber": user.phonenumber,
                    "birth": user.birth,
                    "answers": user.answers,
                }
            }
        )

        return user.dict()


    async def getUserListByType(
        self,
        user_type: int
    ):
        query_task = UserData.find_many({"user_type": user_type})
        total = await query_task.count()
        user_list = await query_task.to_list()
        
        users_dict = []
        for user in user_list:
            user_dict = user.dict()
            users_dict.append(user_dict)
            
        return users_dict
    
    async def getStudentListByApartment(
        self,
        apartment_id: str
    ):
        query_task = UserData.find_many({"user_type": 1})
        total = await query_task.count()
        user_list = await query_task.to_list()
        
        users_dict = []
        for user in user_list:
            if user.room_id is None:
                if(apartment_id == "all"):
                    user_dict = user.dict()
                    users_dict.append(user_dict)
                
            else:
                room = await RoomData.find_one({'_id': PydanticObjectId(user.room_id)})
                apartment = await ApartmentData.find_one({'_id': PydanticObjectId(room.apartment_id)})
                
                user_dict = user.dict()
                user_dict['room_name'] = room.room_name
                user_dict['apartment_name'] = apartment.apartment_name
                
                if(apartment_id == "all"):
                    users_dict.append(user_dict)
                else:
                    if(room.apartment_id == apartment_id):
                        users_dict.append(user_dict)
                
        return users_dict