from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.models.user import UserData
from app.models.room import RoomData
from app.models.room_type import RoomTypeData
from app.models.student_room import StudentRoomData
from app.models.apartment import ApartmentData
from app.models.registration import RegistrationData
from fastapi import HTTPException, status
from app.dto.student_room_dto import (CreateStudentRoomRequest, UpdateStudentRoomRequest)

class StudentRoomService:
    async def list(self):
        query_task = StudentRoomData.find_all()
        total = await query_task.count()
        student_room_list = await query_task.to_list()
        student_rooms_dict = []
        for student_room in student_room_list:
            student_room_dict = student_room.dict()
            student_rooms_dict.append(student_room_dict)
            
        return student_rooms_dict, total


    async def post(
        self,
        student_room_input: CreateStudentRoomRequest,
        user_id: str
    ):
        student_room_input.user_id = user_id
        
        student_room_check = await StudentRoomData.find_one({'user_id': user_id, 'registration_id': student_room_input.registration_id})
        if student_room_check:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Bạn chỉ được đăng ký 1 lần duy nhất')
        
        registration = await RegistrationData.find_one({'_id': PydanticObjectId(student_room_input.registration_id)})
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Đợt đăng ký không tồn tại')
            
        if registration.start_register >= datetime.now() or registration.end_register <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Đợt đăng ký đã kết thúc')
            
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(student_room_input.apartment_id)})
        if not apartment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Toà nhà không tồn tại')
        
        room_type = await RoomTypeData.find_one({'_id': PydanticObjectId(student_room_input.room_type_id)})
        if not room_type:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Loại phòng không tồn tại')
        
        #check capacity register
        
        #danh sach cac dang ky cung toa nha cung loai phong, dot dang ky
        student_room_list = StudentRoomData.find_many({
            'apartment_id': student_room_input.apartment_id,
            'registration_id': student_room_input.registration_id,
            'room_type_id': student_room_input.room_type_id
        })
        
        #danh sach cac phong cung toa nha, cùng loai phong
        room_list = RoomData.find_many({
            'apartment_id': student_room_input.apartment_id,
            'room_type_id': student_room_input.room_type_id
        })
        #tim cac phong trong
        count_room_empty = 0
        rooms = await room_list.to_list()
        
        for room in rooms:
            #tim xem co sv nao dang o phong nay khon. neu co thi ko trong
            student = await UserData.find_one({'room_id': str(room.id)})
            if student is not None:
                continue
            
            count_room_empty += 1
        
        #neu so sinh vien dang ky loai phong do da lon hon so phong trong thi đầy
        if await student_room_list.count() >= room_type.capacity * count_room_empty:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Loại phòng này đã bị đăng ký hết')
        
        student_room_dict = student_room_input.dict()
        model = StudentRoomData(**student_room_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        student_room_input: UpdateStudentRoomRequest
    ):        
        student_room = await StudentRoomData.find_one({'_id': PydanticObjectId(student_room_input.id)})
        if not student_room:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Đăng ký không tồn tại')
        
        await student_room.update({"$set": {
            "status" : student_room_input.status
        }})
        
        return student_room.dict()


    async def current(
        self,
        user_id: str
    ):
        user = await UserData.find_one({'_id': PydanticObjectId(user_id)})
        if user.room_id is None:
            return [], {
                "room_name": "NA",
                "apartment_name": "NA"
            }

        room = await RoomData.find_one({'_id': PydanticObjectId(user.room_id)})
        room_dict = room.dict()
        apartment = await ApartmentData.find_one({'_id': PydanticObjectId(room.apartment_id)})
        room_dict['apartment_name'] = apartment.apartment_name
        
        roommates = UserData.find_many({'room_id': user.room_id})
        roommates_list = await roommates.to_list()
        roommates_dict = []
        for roommate in roommates_list:
            roommate_dict = roommate.dict()
            roommates_dict.append(roommate_dict)
        
        return roommates_dict, room_dict
