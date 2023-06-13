from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.room_type_dto import (CreateRoomTypeRequest, UpdateRoomTypeRequest)
from app.models.room_type import RoomTypeData
from fastapi import HTTPException, status

class RoomTypeService:
    async def list(self):
        query_task = RoomTypeData.find_all()
        total = await query_task.count()
        room_type_list = await query_task.to_list()
        room_types_dict = []
        for room_type in room_type_list:
            room_type_dict = room_type.dict()
            room_types_dict.append(room_type_dict)
            
        return room_types_dict, total


    async def post(
        self,
        room_type_input: CreateRoomTypeRequest
    ):
        room_type = await RoomTypeData.find_one({'room_type_name': room_type_input.room_type_name})
        if room_type:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Loại phòng đã tồn tại')
        
        room_type_dict = room_type_input.dict()
        model = RoomTypeData(**room_type_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        room_type_input: UpdateRoomTypeRequest
    ):
        #thiếu cập nhật room_type thì phải cập nhật room
        
        room_type = await RoomTypeData.find_one({'_id': PydanticObjectId(room_type_input.id)})
        if not room_type:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Loại phòng không tồn tại')
        
        room_type_check = await RoomTypeData.find_one({'room_type_name': room_type_input.room_type_name})
        if room_type_check and room_type_check.id != room_type.id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Tên loại phòng đã tồn tại')
        
        await room_type.update({"$set": {
            "room_type_name" : room_type_input.room_type_name,
            "room_price" : room_type_input.room_price,
            "capacity" : room_type_input.capacity,
            "gender" : room_type_input.gender
        }})
        
        return room_type.dict()