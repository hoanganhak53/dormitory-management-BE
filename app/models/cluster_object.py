from typing import Optional
import numpy as np
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel


class ClusterObjectInput(BaseModel):
    field_one: Optional[str]
    field_one_feature: Optional[list]
    field_two: Optional[str]
    field_two_feature: Optional[list]
    need_nlp_extract: bool = True


class ClusterObject(ClusterObjectInput, RootModel):

    @classmethod
    def get_distance_to_another_object(cls, other: ClusterObjectInput):
        # Exceptions
        if not cls.need_nlp_extract or not other.need_nlp_extract:
            print("One of the two has not extracted features")
            return None
        if len(cls.field_one_feature) != len(other.field_one_feature):
            print("Field one has mismatch feature length")
            return None
        if len(cls.field_two_feature) != len(other.field_two_feature):
            print("Field two has mismatch feature length")
            return None
        
        # Calculation
        dis1 = np.linalg.norm(cls.field_one_feature - other.field_one_feature)
        dis2 = np.linalg.norm(cls.field_two_feature - other.field_two_feature)
        return dis1 + dis2
    
    @classmethod
    def calculate_centroid_from_list(cls, data: list[ClusterObjectInput]):
        list_1 = [item.field_one_feature for item in data]
        list_2 = [item.field_two_feature for item in data]
        cls.field_one_feature = np.sum(list_1, axis=0) / len(list_1)
        cls.field_two_feature = np.sum(list_2, axis=0) / len(list_2)
        return cls
    
    @classmethod
    def calculate_centroid_from_list_and_uik(cls, uik_pow: list, data: list[ClusterObjectInput]):
        list_1 = [uik * item.field_one_feature for uik, item in zip(uik_pow, data)]
        list_2 = [uik * item.field_two_feature for uik, item in zip(uik_pow, data)]
        cls.field_one_feature = np.sum(list_1, axis=0) / len(list_1)
        cls.field_two_feature = np.sum(list_2, axis=0) / len(list_2)
        return cls
