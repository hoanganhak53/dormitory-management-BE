from typing import Optional, Union, List
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.apartment_dto import (CreateApartmentRequest, UpdateApartmentRequest, ClusterStudent)
from app.models.apartment import ApartmentData
from app.models.room import RoomData
from app.models.user import UserData
from app.models.student_room import StudentRoomData
from app.models.room_type import RoomTypeData
from app.models.registration import RegistrationData
from app.models.form import FormData
from app.models.cluster_object import ClusterObject, ClusterObjectInput
from app.services.clustering_service import SSMC_FCM
from fastapi import HTTPException, status
import math
import time

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
                
            room_type = await RoomTypeData.find_one({'_id': PydanticObjectId(registration.room_type_id)})
            if room_type is not None:
                registration_dict['room_type_name'] = room_type.room_type_name
                
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
    

    async def clustering(
        self,
        clusterStudent: ClusterStudent
    ):
        start_time = time.time()
        room_type = await RoomTypeData.find_one({'room_type_name': clusterStudent.room_type_name})
        room_list = RoomData.find_many({
            'apartment_id': clusterStudent.apartment_id,
            'room_type_id': str(room_type.id)
        })
        #tim cac phong trong
        count_room_empty = 0
        rooms = await room_list.to_list()
        
        empty_rooms = []
        for room in rooms:
            #tim xem co sv nao dang o phong nay khon. neu co thi ko trong
            student = await UserData.find_one({'room_id': str(room.id)})
            if student is not None:
                continue
            count_room_empty += 1
            empty_rooms.append(room)
        student_limit = room_type.capacity * count_room_empty
        
        if student_limit == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Không còn phòng nào trống')
        # danh sách đăng ký 
        student_room = await StudentRoomData.find_many({'room_type_id': str(room_type.id), 'apartment_id': clusterStudent.apartment_id, 'status': 2}).limit(student_limit).to_list()
        all_student = UserData.find_all()
        all_student_list = await all_student.to_list()
        all_student_registered = []
        for student in all_student_list:
            found = False
            for obj in student_room:
                if obj.user_id == str(student.id):
                    found = True
                    break
            if found:
                all_student_registered.append(student)
        
        dataset, questions_weight = await self.data_preprocessing(all_student_registered)
        dataset_obj = []
        for data in dataset:
            dataset_obj.append(ClusterObject(**data))

        cluster = SSMC_FCM(dataset_obj, questions_weight, round(len(dataset) / room_type.capacity), 2, 0.6, 0.001, 50, False)
        cluster_element = cluster.clustering()
        
        rs = []
        for i in range(len(cluster_element)):
            rs.append(cluster_element[i])
            print(cluster_element[i])
        
        rs = await self.response_data_processing(rs, dataset, room_type.capacity, empty_rooms)
        
        return rs, {
            "room_num": len(cluster_element),
            "student_num": len(dataset),
            "time": round(time.time() - start_time, 3) ,
            "room_type_name": clusterStudent.room_type_name
        }
        
    #todo
    async def save_cluster(self, rooms: List):
        for room in rooms:
            for student in room["students"]:
                student["room_id"] = room["id"]
                # update student room
                # student_room = await StudentRoomData.find_one({'user_id': student["user_id"], 'status': 2})
                # if not student_room:
                #     raise HTTPException(
                #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Sắp xếp lỗi')
                # await student_room.update({"$set": {
                #     "status" : 3
                # }})
        
        return rooms

    async def data_preprocessing(self, students: List):
        # form preprocessing
        form = await FormData.find_all().to_list()
        questions = []
        sum_weight = 0
        questions_weight = []
        for question in form:
            weight = []
            sum_questions = 0
            sum_weight += float(question.weight)
            questions_weight.append(float(question.weight))
            for i in range(0, len(question.matrix.keys())):
                product = 1
                for j in range(0, len(question.matrix.keys())):
                    product = product * question.matrix[f'{i}'][j]
                sum_questions += math.pow(product, 1 / len(question.matrix.keys()))
                weight.append(math.pow(product, 1 / len(question.matrix.keys())))
            
            for i in range(0, len(weight)):
                weight[i] = weight[i] / sum_questions
            questions.append(weight)
        
        for i in range(0, len(questions_weight)):
            questions_weight[i] = questions_weight[i] / sum_weight
        # student preprocessing
        dataset = []
        for student in students:
            answers = []
            index = 0
            for answer in student.answers.keys():
                # answer_preprocessing['answer_type'] = str(student.answers[answer]['answer_type'])
                question = await FormData.find_one({'_id': PydanticObjectId(answer)})
                length = len(question.answers)
                vector = [1 * questions[index][i] if i in student.answers[answer]['answer'] else 0 for i in range(0, length)]
                answers.append(vector)
                index += 1

            cluster_student = dict()
            cluster_student['user_id'] = str(student.id)
            cluster_student['answers'] = answers
            dataset.append(cluster_student)
        
        return dataset, questions_weight
    
    async def response_data_processing(self, centroids: List, dataset: List, capacity: int, empty_rooms: List):
        final_array = []
        short_centroids = []
        for sub_array in centroids:
            if len(sub_array) == capacity:
                final_array.append(sub_array)
            elif len(sub_array) > capacity:
                while len(sub_array) > capacity:
                    final_array.append(sub_array[:capacity])
                    sub_array = sub_array[capacity:]
                if len(sub_array) == capacity:
                    final_array.append(sub_array)
                else:
                    short_centroids.append(sub_array)
            else:
                short_centroids.append(sub_array)

        sorted_array = sorted(short_centroids, key=len)
        merged_array = [element for sub_array in sorted_array for element in sub_array]
        final_array = final_array + [merged_array[i:i + capacity] for i in range(0, len(merged_array), capacity)]

        empty_rooms = empty_rooms[:len(final_array)]
        
        rs = []
        for i in range(0, len(final_array)):
            obj = empty_rooms[i].dict()
            students = []
            for index in final_array[i]:
                student = await UserData.find_one({'_id': PydanticObjectId(dataset[index]['user_id'])})
                student = student.dict()
                del student['answers']
                students.append(student)
            obj['students'] = students
            rs.append(obj)

        return rs