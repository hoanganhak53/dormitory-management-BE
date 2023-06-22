from typing import Optional, Union, List
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.room_dto import (CreateRoomRequest, UpdateRoomRequest)
from app.models.room import RoomData
from app.models.room_type import RoomTypeData
from app.models.user import UserData
from app.models.apartment import ApartmentData
from app.models.student_room import StudentRoomData
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
            students = UserData.find_many({'room_id': str(room.id)})

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
        if room and room.apartment_id == room_input.apartment_id:
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
        if room_check and room_check.id != room.id and room_check.apartment_id == room.apartment_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Phòng đã tồn tại')
        
        await room.update({"$set": {
            "room_name" : room_input.room_name,
            "room_type_id" : room_input.room_type_id,
            "apartment_id" : room_input.apartment_id
        }})
        
        return room.dict()
    
    async def detail(
        self,
        room_id: str
    ):
        students = UserData.find_many({'room_id': room_id})
        students_dict = []
        student_list = await students.to_list()
        for student in student_list:
            students_dict.append(student.dict())
        
        return students_dict
    
    
    async def distribute(
        self,
        rooms: List
    ):
        if len(rooms) == 0:
            return [], ""
        
        #get room type
        room_type = rooms[0].get("room_type")
        apartment_id = rooms[0].get("apartment_id")
        CAPACITY = room_type.get("capacity")
        valid_rooms = []
        #loc cac phong trong va day
        for room in rooms:
            if room.get("student_num") != 0 and room.get("student_num") != CAPACITY:
                #loc cac thong tin thua
                short_room = {
                    "room_name": room.get("room_name"),
                    "id": room.get("id"),
                    "student_num": room.get("student_num")
                }
                valid_rooms.append(short_room)
        
        if len(valid_rooms) == 0:
            return [], ""
        
        #ghep cac phong co tong bang max
        new_valid_rooms = valid_rooms.copy()
        pair_array = []
        
        i = 0
        while i < len(new_valid_rooms) - 1:
            current_dict = new_valid_rooms[i]
            current_num = current_dict["student_num"]
            complement = CAPACITY - current_num

            for j in range(i + 1, len(new_valid_rooms)):
                if new_valid_rooms[j]["student_num"] == complement:
                    # Tìm thấy cặp dict, thêm vào mảng mới và xóa khỏi mảng gốc
                    pair_array.append([current_dict, new_valid_rooms[j]])
                    new_valid_rooms.pop(i)
                    new_valid_rooms.pop(j - 1)
                    break
            else:
                i += 1

        #thuc hien don cac cap phong trong pair_array TO DO
        
        #sắp xếp các phòng còn lại giảm dần
        sorted_room = sorted(new_valid_rooms, key=lambda x: x["student_num"], reverse=True)
        
        groups = []  # Mảng chứa các nhóm
        current_group = []  # Nhóm hiện tại
        total = 0  # Tổng của các phần tử trong nhóm hiện tại
        tail = 0 # Vị trí phần tử lớn nhất còn trong mảng
        head = len(sorted_room) - 1 #Vị trí phần tử nhỏ nhất còn trong mảng
        
        while head > tail:
            if len(current_group) == 0:
                # Nếu current_group rỗng thì luôn thêm vào tail
                student_num_tail = sorted_room[tail]["student_num"]
                current_group.append(sorted_room[tail])
            else:
                # Tổng tất cả phần tử trong current group
                student_num_tail = sum(item["student_num"] for item in current_group)
                
            # Nếu tổng tail và head bằng CAPACITY
            if sorted_room[head]["student_num"] + student_num_tail == CAPACITY:
                current_group.append(sorted_room[head])
                groups.append(current_group)
                current_group = []
                head -= 1
                tail += 1

            elif sorted_room[head]["student_num"] + student_num_tail > CAPACITY:
                append_head = sorted_room[head].copy()
                append_head["student_num"] = CAPACITY - student_num_tail
                current_group.append(append_head)
                groups.append(current_group)
                current_group = []
                tail += 1
                # Cập nhật lại tail
                sorted_room[head]["student_num"] = sorted_room[head]["student_num"] + student_num_tail - CAPACITY
                if(tail >= head):
                    groups.append([sorted_room[head]])
            
            else:
                # Tổng trong current_group chưa đủ CAPACITY
                current_group.append(sorted_room[head])
                if(head - 1 <= tail):
                    groups.append(current_group)
                
                head -= 1

        new_rooms = pair_array + groups
        
        # Thêm thông tin sinh viên vào các group mới
        students = UserData.find_many({"user_type": 1})
        student_list = await students.to_list()
        students_dict = []
        for student in student_list:
            students_dict.append(student.dict())
        
        total_student_count = 0
        for room_group in new_rooms:
            for room in room_group:
                student_in_room = []
                count = 0
                new_students_dict = students_dict.copy()
                for student in students_dict:
                    if student.get("room_id") == room.get("id"):
                        student_in_room.append(student)
                        count += 1
                        new_students_dict.remove(student)
                        if count == room.get("student_num"):
                            break

                room["students"] = student_in_room
                students_dict = new_students_dict.copy()
                total_student_count += len(student_in_room)
            
        return new_rooms, {
            "num_distributed": len(valid_rooms),
            "num_empty": len(valid_rooms) - len(new_rooms),
            "new_rooms": len(new_rooms),
            "total_student": total_student_count
        }
        
        
    async def save_distribute(
        self,
        rooms: List
    ):
        try:
            for room_group in rooms:
                new_room_id = room_group[0].get('id')
                for room in room_group:
                    for student in room.get('students'):
                        student_data = await UserData.find_one({'_id': PydanticObjectId(student.get('id'))})
                        if student_data is None:
                            raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Lưu thông tin thất bại')
                        
                        await student_data.update({"$set": {
                            "room_id" : new_room_id
                        }})
                        
                        student_room_data = await StudentRoomData.find_one({'user_id': student.get('id'), 'status': 3})
                        if student_room_data is not None:
                            await student_room_data.update({"$set": {
                                "room_id" : new_room_id
                            }})
                        
        
        finally:
            pass
        
        return