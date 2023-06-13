from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.apartment_dto import (CreateApartmentRequest, UpdateApartmentRequest)
from app.models.apartment import ApartmentData
from app.models.room import RoomData
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
            rooms_dict.append(room_dict)
        
        return {
            "apratment": apartment.dict(),
            "rooms": rooms_dict
        }