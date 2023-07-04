from typing import Optional, List
import numpy as np
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel

class ClusterObjectInput(BaseModel): 
    user_id: Optional[str]
    answers: Optional[List] = []

class ClusterObject(ClusterObjectInput):

    def get_distance_to_another_object(cls, other: ClusterObjectInput, fields_weight: Optional[List]):
        # Kiem tra du lieu dau vao
        if len(cls.answers) is not len(fields_weight) and len(other.answers) is not len(fields_weight):
            print("Trả lời thiếu câu hỏi")
            return None
    
        dis_answer = []
        for i in range(0, len(cls.answers)):
            if len(cls.answers[i]) != len(other.answers[i]):
                print("Sai dữ liệu")
                return None
            # Tinh khoang cach cua 1 cau hoi
            cls_vector = np.array(cls.answers[i])
            other_vector = np.array(other.answers[i])
            dis = np.linalg.norm(cls_vector - other_vector)
            dis_answer.append(dis)
        
        # Mhan voi trong so cau hoi
        rs = 0
        index = 0
        for dis in dis_answer:
            rs += dis * fields_weight[i]
            index += 1
            
        return rs
    
    
    @classmethod
    def calculate_centroid_from_list_and_uik(cls, uik_pow: list, data: list[ClusterObjectInput]):
        new_answers = []
        for i in range(0, len(data[0].answers)):
            list_ = [cls.multiply_array_elements(item.answers[i], uik) for uik, item in zip(uik_pow, data)]
            new_answers.append(cls.add_and_divide_arrays(list_))

        cls.answers = new_answers
        return cls

    def multiply_array_elements(array: list, factor: float):
        result = []
        for element in array:
            result.append(element * factor)
        return result

    def add_and_divide_arrays(arrays):
        total_arrays = len(arrays)
        result = np.zeros_like(arrays[0])  # Tạo một mảng kết quả với kích thước giống với mảng đầu tiên

        for array in arrays:
            result += array

        result /= total_arrays

        return result