from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.models.user import UserData
from app.models.room import RoomData
from app.models.student_room import StudentRoomData
from app.models.registration import RegistrationData
from app.models.apartment import ApartmentData
from app.models.room_type import RoomTypeData
from fastapi import HTTPException, status

class StudentService:

    async def toggleValid(
        self,
        student_id: str
    ):
        user = await UserData.get(PydanticObjectId(str(student_id)))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tài khoản không tổn tại')
        
        user.is_valid =  False if user.is_valid else True
        await user.update(
            { "$set":
                {
                    "is_valid": user.is_valid,
                }
            }
        )

        return user.dict()

    async def registration_list(
        self,
        user_id: str
    ):
        user = await UserData.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tài khoản không tổn tại')
        
        registrations = StudentRoomData.find_many({'user_id': str(user.id)})
        registration_list = await registrations.to_list()
        registrations_dict = []
        for registration in registration_list:
            registration_dict = registration.dict()
            room = await RoomData.get(PydanticObjectId(registration.room_id))
            regis = await RegistrationData.get(PydanticObjectId(registration.registration_id))
            apartment = await ApartmentData.get(PydanticObjectId(registration.apartment_id))
            room_type = await RoomTypeData.get(PydanticObjectId(registration.room_type_id))
            
            registration_dict['semester'] = regis.semester
            registration_dict['registration_name'] = regis.registration_name
            registration_dict['apartment_name'] = apartment.apartment_name
            registration_dict['room_type_name'] = room_type.room_type_name
            registration_dict['room_price'] = room_type.room_price
            if room is not None:
                registration_dict['room_name'] = room.room_name
            else:
                registration_dict['room_name'] = "NA"
                
            registrations_dict.append(registration_dict)
            
        return registrations_dict
