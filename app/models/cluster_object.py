from typing import Optional, List
import numpy as np
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel

class ClusterObjectInput(BaseModel): 
    user_id: Optional[str]
    answers: Optional[List] = []

class ClusterStudentService():

    def get_distance_to_another_object(self, first: ClusterObjectInput, other: ClusterObjectInput, fields_weight: Optional[List]):
        # Kiem tra du lieu dau vao
        if len(first.answers) is not len(fields_weight) and len(other.answers) is not len(fields_weight):
            print("Trả lời thiếu câu hỏi")
            return None
    
        dis_answer = []
        for i in range(0, len(first.answers)):
            if len(first.answers[i]) != len(other.answers[i]):
                print("Sai dữ liệu")
                return None
            # Tinh khoang cach cua 1 cau hoi
            first_vector = np.array(first.answers[i])
            other_vector = np.array(other.answers[i])
            dis = np.linalg.norm(first_vector - other_vector)
            dis_answer.append(dis)
        
        # Mhan voi trong so cau hoi
        rs = 0
        index = 0
        for dis in dis_answer:
            rs += dis * fields_weight[i]
            index += 1
            
        return rs
    
    def calculate_centroid_from_list_and_uik(cls, uik_pow: list, data: list[ClusterObjectInput]):
        new_answers = []
        for i in range(0, len(data[0].answers)):
            list_ = [cls.multiply_array_elements(item.answers[i], uik) for uik, item in zip(uik_pow, data)]
            new_answers.append(cls.add_and_divide_arrays(list_))

        new_centroid = ClusterObjectInput(
            user_id="",
            answers=new_answers
        )
        return new_centroid
    
    def calculate_centroid_k_means(cls, data: list[ClusterObjectInput]):
        new_answers = []
        for i in range(0, len(data[0].answers)):
            list_ = [item.answers[i] for item in data]
            new_answers.append(cls.add_and_divide_arrays(list_))

        new_centroid = ClusterObjectInput(
            user_id="",
            answers=new_answers
        )
        return new_centroid

    def multiply_array_elements(cls, array: list, factor: float):
        result = []
        for element in array:
            result.append(element * factor)
        return result

    def add_and_divide_arrays(cls, arrays):
        total_arrays = len(arrays)
        result = np.zeros_like(arrays[0])  # Tạo một mảng kết quả với kích thước giống với mảng đầu tiên

        for array in arrays:
            result += array

        result /= total_arrays

        return result