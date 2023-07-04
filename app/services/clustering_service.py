import sys
import math
import traceback
import scipy.optimize
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List

from app.models.cluster_object import ClusterObject

class FCM :
    def __init__(
        self,
        # Danh sách các sinh viên sau khi tiền xử lý
        dataset: List[ClusterObject],
        # Mảng trọng số
        fields_weight: Optional[List] = [],
        # Số cụm
        n_clusters: Optional[int] = 3,
        # Hệ số M nên mặc định là 2
        fuzzi_M: Optional[int] = 2,
        alpha: Optional[float] = 0.6,
        # Điểm dừng
        epsilon: Optional[float] = 0.001,
        # Số vòng lặp tối đa
        n_loop: Optional[int] = 50,
        is_plot: Optional[bool] = False,
    ) -> None:
        self.dataset = dataset
        self.fields_weight = fields_weight
        self.n_clusters = n_clusters
        self.fuzzi_M = fuzzi_M
        self.alpha = alpha
        self.epsilon = epsilon
        self.membership = [[0] * self.n_clusters for i in range(len(dataset))]
        self.fuzzi_set = [[fuzzi_M] * self.n_clusters for i in range(len(dataset))]
        self.centroid = []
        self.n_loop = n_loop
        self.is_stop = False
        self.pred_labels = [[] for _ in range(self.n_clusters)]
        self.is_plot = is_plot
        self.loss_values = []

    def clustering(self):
        self.__generate_centroid()
        th_loop = 1
        while th_loop <= self.n_loop:
            self.is_stop = True
            self.__update_membership(th_loop)
            self.__update_centroid(th_loop)
            self.__calculate_loss_function()
            th_loop += 1
        for idx, membership in enumerate(self.membership):
            id_cluster = np.argmax(membership)
            self.pred_labels[id_cluster].append(idx)
        self.pred_labels = np.array(self.pred_labels, dtype=object)
        
        return self.pred_labels

    def __generate_centroid(self):
        # computing random centroid for unsupervised clusters (apply kmean++)
        for k in range(self.n_clusters - len(self.centroid)):
            ## initialize a list to store distances of data
            ## points from nearest centroid
            dist = []
            for i in range(len(self.dataset)):
                point = self.dataset[i]
                d = sys.maxsize

                ## compute distance of 'point' from each of the previously
                ## selected centroid and store the minimum distance
                for j in range(len(self.centroid)):
                    temp_dist = self.__calculate_point_distance(self.centroid[j], point)
                    d = min(d, temp_dist)
                dist.append(d)

            ## select data point with maximum distance as our next centroid
            dist = np.array(dist)
            next_centroid = self.dataset[np.argmax(dist)]
            self.centroid.append(next_centroid)


    def __update_membership(self, th_loop):

        fuzzi_M_pow = 1 / (self.fuzzi_M - 1)
        Dij = [
            [
                self.__calculate_point_distance(point, centroid)
                for centroid in self.centroid
            ]
            for point in self.dataset
        ]

        # without supervision
        for id_point, point in enumerate(self.dataset):
            Dij_pow = []
            sum_Dij_pow = 0
            for id_centroid, centroid in enumerate(self.centroid):
                Dik_pow = math.pow(Dij[id_point][id_centroid], fuzzi_M_pow)
                Dij_pow.append(Dik_pow)
                sum_Dij_pow += 1 / Dik_pow

            membership = [1 / (Dik_pow * sum_Dij_pow) for Dik_pow in Dij_pow]
            self.membership[id_point] = membership


    def __update_centroid(self, th_loop):
        th_centroid = []
        for id_centroid, centroid in enumerate(self.centroid):
            uik_pow = [
                math.pow(
                    self.membership[id_point][id_centroid],
                    self.fuzzi_set[id_point][id_centroid],
                )
                for id_point in range(len(self.dataset))
            ]
            new_centroid = ClusterObject()
            new_centroid.calculate_centroid_from_list_and_uik(uik_pow=uik_pow, data=self.dataset)
            th_centroid.append(new_centroid)
            # if self.__calculate_point_distance(centroid, new_centroid) > self.epsilon:
            #     self.is_stop = False


    def __calculate_point_distance(self, p1, p2):
        distance = p1.get_distance_to_another_object(p2, self.fields_weight)
        return distance if distance else self.epsilon


    def __calculate_loss_function(self):
        self.loss_values.append(
            sum(
                [
                    sum(
                        [
                            math.pow(
                                self.membership[id_point][id_centroid],
                                self.fuzzi_set[id_point][id_centroid],
                            )
                            * self.__calculate_point_distance(point, centroid)
                            for id_centroid, centroid in enumerate(self.centroid)
                        ]
                    )
                    for id_point, point in enumerate(self.dataset)
                ]
            )
        )

    def show_cluster_members(self):
        print("Cluster members: ")
        for cluster in self.pred_labels:
            print(cluster)

    def show_loss_function(self):
        plt.plot(self.loss_values)
        plt.title("Loss function")
        plt.show()
        print("loss functions: ")
        print(self.loss_values)
        