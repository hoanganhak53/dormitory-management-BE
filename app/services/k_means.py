import sys
import math
import numpy as np
from typing import Optional, List
import random

from app.models.cluster_object import ClusterStudentService, ClusterObjectInput

class KMEANS :
    def __init__(
        self,
        # Danh sách các sinh viên sau khi tiền xử lý
        dataset: List[ClusterObjectInput],
        # Mảng trọng số
        fields_weight: Optional[List] = [],
        # Số cụm
        n_clusters: Optional[int] = 3,
        # Hệ số M nên mặc định là 2
        # Điểm dừng
        epsilon: Optional[float] = 0.000001,
        # Số vòng lặp tối đa
        n_loop: Optional[int] = 50,
        max_size_cluster: int = 6,
    ) -> None:
        self.dataset = dataset
        self.fields_weight = fields_weight
        self.n_clusters = n_clusters
        self.epsilon = epsilon
        self.max_size_cluster = max_size_cluster
        self.centroid = []
        self.n_loop = n_loop
        self.is_stop = False
        self.pred_labels = [[] for _ in range(self.n_clusters)]
        self.loss_values = []

    def clustering(self):
        self.__generate_centroid()
        th_loop = 1
        while th_loop <= self.n_loop and not self.is_stop:
            self.is_stop = True
            self.__update_membership()
            self.__update_centroid()
            self.__calculate_loss_function()
            th_loop += 1

        return self.pred_labels, th_loop, self.epsilon, self.loss_values

    def __generate_centroid(self):
        exclude_list = []
        # khởi tạo ngẫu nhiên tâm cụm
        first_centroid = random.randint(0, self.n_clusters - 1)
        self.centroid.append(self.dataset[first_centroid])
        exclude_list.append(first_centroid)

        for k in range(self.n_clusters - 1):
            random_list = list(set([i for i in range(0, self.n_clusters - 1)]) - set(exclude_list))
            next_centroid = random.choice(random_list)
            for i in range(len(self.dataset)):
                if i in exclude_list:
                    continue
                next_centroid = i

            exclude_list.append(next_centroid)
            self.centroid.append(self.dataset[next_centroid])


    def __update_membership(self):

        Dij = [
            [
                self.__calculate_point_distance(point, centroid)
                for centroid in self.centroid
            ]
            for point in self.dataset
        ]

        for id_point, point in enumerate(self.dataset):
            sorted_membership = sorted(Dij[id_point], key=float, reverse=True)
            for data in sorted_membership:
                id_cluster = Dij[id_point].index(data)
                if len(self.pred_labels[id_cluster]) < self.max_size_cluster:
                    self.pred_labels[id_cluster].append(id_point)
                    break


    def __update_centroid(self):
        th_centroid = []
        for id_centroid, centroid in enumerate(self.centroid):
            data = [self.dataset[i] for i in self.pred_labels[id_centroid]]
            service = ClusterStudentService()
            new_centroid = service.calculate_centroid_k_means(data=data)
            th_centroid.append(new_centroid)
            if self.__calculate_point_distance(centroid, new_centroid) > self.epsilon:
                self.is_stop = False

        self.centroid = th_centroid

    def __calculate_point_distance(self, p1, p2):
        service = ClusterStudentService()
        distance = service.get_distance_to_another_object(p1, p2, self.fields_weight)
        return distance if distance else self.epsilon


    def __calculate_loss_function(self):
        self.loss_values.append(
            sum(
                [
                    sum(
                        [
                            math.pow(self.__calculate_point_distance(point, centroid), 2)
                            for id_centroid, centroid in enumerate(self.centroid)
                        ]
                    ) / len(self.dataset) * 5
                    for id_point, point in enumerate(self.dataset)
                ]
            )
        )