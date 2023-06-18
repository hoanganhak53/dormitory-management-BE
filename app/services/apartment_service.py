from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.apartment_dto import (CreateApartmentRequest, UpdateApartmentRequest)
from app.models.apartment import ApartmentData
from app.models.room import RoomData
from app.models.user import UserData
from app.models.student_room import StudentRoomData
from app.models.room_type import RoomTypeData
from app.models.registration import RegistrationData
from fastapi import HTTPException, status

class ApartmentService:
    async def list(self):
        query_task = ApartmentData.find_all()
        total = await query_task.count()
        apartment_list = await query_task.to_list()
        apartments_dict = []
        for apartment in apartment_list:
            apartment_dict = apartment.dict()
            apartments_dict.append(apartment_dict)
        
        return apartments_dict, total


    async def post(
        self,
        apartment_input: CreateApartmentRequest
    ):
        apartment = await ApartmentData.find_one({'apartment_name': apartment_input.apartment_name})
        if apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tên tòa nhà đã tồn tại')
        
        apartment = await ApartmentData.find_one({'manager_id': apartment_input.manager_id})
        if apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Quản lý đang quản lý tòa nhà khác')
        
        apartment_dict = apartment_input.dict()
        model = ApartmentData(**apartment_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        apartment_input: UpdateApartmentRequest
    ):
        #thiếu cập nhật apartment thì phải cập nhật room
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(apartment_input.id)})
        if not apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tòa nhà không tồn tại')
        
        apartment_check = await ApartmentData.find_one({'apartment_name': apartment_input.apartment_name})
        if apartment_check and apartment_check.id != apartment.id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tên tòa nhà đã tồn tại')
        
        apartment_check = await ApartmentData.find_one({'manager_id': apartment_input.manager_id})
        if apartment_check and apartment_check.id != apartment.id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Quản lý đang quản lý tòa nhà khác')
        
        
        await apartment.update({"$set": {
            "apartment_name" : apartment_input.apartment_name,
            "manager_id" : apartment_input.manager_id
        }})
        
        return apartment.dict()
    

    async def detail(
        self,
        apartment_id: str
    ):
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(apartment_id)})
        if not apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tòa nhà không tổn tại')
        
        rooms = RoomData.find_many({'apartment_id': apartment_id})
        
        room_list = await rooms.to_list()
        rooms_dict = []
        for room in room_list:
            room_dict = room.dict()
            
            student_in_room = UserData.find_many({'room_id': str(room.id)})
            room_type = await RoomTypeData.find_one({'_id': PydanticObjectId(room.room_type_id)})

            room_dict['student_num'] = await student_in_room.count()
            room_dict['room_type'] = room_type.dict()
            rooms_dict.append(room_dict)
        
        return apartment.dict(), rooms_dict
    
    
    async def registration_by_apartment(
        self,
        apartment_id: str
    ):
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(apartment_id)})
        if not apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tòa nhà không tổn tại')
        
        registrations = StudentRoomData.find_many({'apartment_id': apartment_id})
        registrations_list = await registrations.to_list()
        registrations_dict = []
        
        for registration in registrations_list:
            registration_dict = registration.dict()
            room = await RoomData.find_one({'_id': PydanticObjectId(registration.room_id)})
            if room is not None:
                registration_dict['room_name'] = room.room_name
                
            user = await UserData.find_one({'_id': PydanticObjectId(registration.user_id)})
            registra = await RegistrationData.find_one({'_id': PydanticObjectId(registration.registration_id)})
            
            registration_dict['full_name'] = user.full_name
            registration_dict['mssv'] = user.mssv
            registration_dict['gender'] = user.gender
            registration_dict['batch'] = user.batch
            registration_dict['major'] = user.major
            registration_dict['registration_name'] = registra.registration_name
            
            registrations_dict.append(registration_dict)
        
        return registrations_dict, apartment.dict()