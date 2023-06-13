from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.room_dto import (CreateRoomRequest, UpdateRoomRequest)
from app.models.room import RoomData
from app.models.room_type import RoomTypeData
from app.models.user import UserData
from app.models.apartment import ApartmentData
from fastapi import HTTPException, status

class RoomService:
    async def list(self):
        query_task = RoomData.find_all()
        total = await query_task.count()
        room_list = await query_task.to_list()
        rooms_dict = []
        for room in room_list:
            room_dict = room.dict()
            room_type = await RoomTypeData.find_one({'_id': PydanticObjectId(room.room_type_id)})
            apartment = await ApartmentData.find_one({'_id': PydanticObjectId(room.apartment_id)})
            students = ApartmentData.find_many({'room_id': room_dict['id']})

            room_dict["room_type_name"] = room_type.room_type_name
            room_dict["room_price"] = room_type.room_price
            room_dict["capacity"] = room_type.capacity
            room_dict["gender"] = room_type.gender
            room_dict["apartment_name"] = apartment.apartment_name
            room_dict["student_num"] = await students.count()
        
            rooms_dict.append(room_dict)

        return rooms_dict, total


    async def post(
        self,
        room_input: CreateRoomRequest
    ):
        room = await RoomData.find_one({'room_name': room_input.room_name})
        if room:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Phòng đã tồn tại')
        
        room_dict = room_input.dict()
        
        room_type = await RoomTypeData.find_one({'_id': PydanticObjectId(room_input.room_type_id)})
        if not room_type:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Loại phòng không tồn tại')
        room_dict['room_type'] = room_type.dict()
        
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(room_input.apartment_id)})
        if not apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tòa nhà không tồn tại')
        room_dict['apartment_name'] = apartment.apartment_name
        
        model = RoomData(**room_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        room_input: UpdateRoomRequest
    ):
        room = await RoomData.find_one({'_id': PydanticObjectId(room_input.id)})
        if not room:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Phòng không tồn tại')
        
        room_check = await RoomData.find_one({'room_name': room_input.room_name})
        if room_check and room_check.id != room.id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Phòng đã tồn tại')
        
        await room.update({"$set": {
            "room_name" : room_input.room_name,
            "room_type_id" : room_input.room_type_id,
            "apartment_id" : room_input.apartment_id
        }})
        
        return room.dict()