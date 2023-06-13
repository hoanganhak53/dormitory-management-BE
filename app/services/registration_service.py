from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.registration_dto import (CreateRegistrationRequest, UpdateRegistrationRequest)
from app.models.registration import RegistrationData
from app.models.user import UserData
from app.models.room import RoomData
from app.models.apartment import ApartmentData
from app.models.room_type import RoomTypeData
from app.models.student_room import StudentRoomData
from fastapi import HTTPException, status

class RegistrationService:
    async def list(self):
        query_task = RegistrationData.find_all()
        total = await query_task.count()
        registration_list = await query_task.to_list()
        registrations_dict = []
        for registration in registration_list:
            registration_dict = registration.dict()
            registrations_dict.append(registration_dict)

        return registrations_dict, total


    async def post(
        self,
        registration_input: CreateRegistrationRequest
    ):
        registration_dict = registration_input.dict()
        model = RegistrationData(**registration_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        registration_input: UpdateRegistrationRequest
    ):  
        registration = await RegistrationData.find_one({'_id': PydanticObjectId(registration_input.id)})

        await registration.update({"$set": {
            "registration_name" : registration_input.registration_name,
            "start_date" : registration_input.start_date,
            "end_date" : registration_input.end_date,
            "start_register" : registration_input.start_register,
            "end_register" : registration_input.end_register,
            "paid_date" : registration_input.paid_date,
            "semester" : registration_input.semester
        }})
        
        return registration.dict()
    
    async def current(
        self,
        user_id: str
    ):          
        registration_all = RegistrationData.find_all()
        current_registration = None
        registration_all_list = await registration_all.to_list()
        for registration in registration_all_list:
            if  registration.start_register <= datetime.now() and registration.end_register >= datetime.now():
                current_registration = registration
                pass
        
        if current_registration is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Hiện không trong đợt đăng ký nào')
        
        user = await UserData.find_one({'_id': PydanticObjectId(user_id)})
        if not user.is_valid or not user.is_more_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tài khoản chưa sẵn sàng để đăng ký')
             
        room_types = RoomTypeData.find_many({'gender': user.gender})
        room_type_list = await room_types.to_list()
        
        can_register = []
        for room_type in room_type_list:
            room_type_dict = room_type.dict()
            can_register.append(room_type_dict)

        return can_register, current_registration.dict()