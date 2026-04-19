"""
题目：
假设一位旅行商需要访问下列这些城市，并最终返回起始城市，且每个城市仅经过一次。
给定以下城市坐标，编写 Python 代码找到最短的访问路径。
"""

import math
import csv
import matplotlib.pyplot as plt
import numpy as np
import random

plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# csv 文件中，第一列是城市名，第二列是X，第三列是Y，总共 34 个城市
# 例如
# 北京,9932,4439


# 使用模拟退火算法解决旅行商问题
class SimulatedAnnealingTSP:
    def __init__(self, path="data.csv", origin="北京"):
        """
        初始化模拟退火算法解决旅行商问题
        :param path: 城市坐标数据文件路径
        :param origin: 起始城市
        """
        self.path = path  # 城市数据文件路径
        self.origin = origin  # 起始城市
        self.cities, self.coordinates = self._load_data()  # 加载城市数据
        self.num_cities = len(self.cities)  # 城市数量
        self.origin_index = self.get_index(origin) if origin else None  # 起始城市索引
        self.distances = self._cal_matrix_distance()  # 城市距离矩阵

        # 模拟退火算法超参数
        self.initial_temp = 10000.0  # 初始温度
        self.cooling_rate = 0.995  # 降温速率（每轮乘以该系数）
        self.iterations_per_temp = 200  # 每个温度下的迭代次数
        self.stop_temp = 1e-8  # 停止温度（低于此值终止）

    def _load_data(self):
        """
        从CSV文件加载城市坐标数据，并计算城市之间的距离
        :return: 城市列表和城市坐标
        """
        cities = []
        coordinates = []
        with open(self.path, "r", encoding="utf-8") as f:
            next(f)  # 跳过第一行标题
            reader = csv.reader(f)
            for row in reader:
                cities.append(row[0])  # 记录城市名称
                coordinates.append(int(row[1]), int(row[2]))  # 记录城市坐标
        return cities, coordinates

    def _cal_distance(self, i, j):
        """
        计算两个城市之间的距离
        :param i: 城市i
        :param j: 城市j
        """
        x1, y1 = self.coordinates[i]
        x2, y2 = self.coordinates[j]
        return math.hypot(x2 - x1, y2 - y1)  # 计算两点距离

    def _cal_matrix_distance(self):
        """
        计算城市之间的距离矩阵，该矩阵对称，且对角线元素为0
        :return: 城市距离矩阵
        """
        distances = [
            [0 for _ in range(self.num_cities)] for _ in range(self.num_cities)
        ]
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                distances[i][j] = distances[j][i] = self._cal_distance(i, j)
        return distances

    def _total_distance(self, route):
        """
        计算访问路径的总距离
        :param route: list of int, 访问路径
        :return: float, 总距离
        """
        dist = 0
        for i in range(len(route)):
            dist += self.distances[route[i]][route[(i + 1) % len(route)]]
        return dist

    def _random_route(self):
        """
        生成随机的访问路径
        :return: 访问路径，第一个元素是起始城市，其余为其余城市的随机排列
        """
        other_cities = [i for i in range(self.num_cities) if i != self.origin_index]
        random.shuffle(other_cities)
        route = [self.origin_index] + other_cities
        return route

    def _get_city_index(self, city_name):
        """
        获取城市名称对应的索引
        :param city_name: 城市名称
        :return: 城市索引
        """
        try:
            return self.cities.index(city_name)
        except:
            raise ValueError(f"{city_name}不在数据之中")

    def _neighnour_route(self, route):
        """
        产生当前路径的一个邻域解（随机交换两个非起始城市的位置）
        :param route: 当前路径
        :return: 新路径
        """
        new_route = route.copy()
        # 随机选择两个不同的位置，且不包含起点（索引0）
        idx1, idx2 = random.sample(range(1, self.num_cities), 2)
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        return new_route
    
    def simulated_annealing(self):
        """
        执行模拟退火算法，寻找最短访问路径
        :return: 最短路径和对应距离
        """
        # 1. 初始化当前解和最优解
        current_route = self._random_route()  # 随机生成初始路径
        current_dist = self._total_distance(current_route)  # 计算初始路径距离

        best_route = current_route.copy()  # 最优路径
        best_dist = current_dist  # 最优路径距离

        temperature = self.initial_temp  # 初始温度

        #2. 执行模拟退火算法
        while(temperature>self.stop_temp):
            for _ in range(self.num_iter):
                # 生成新解
                new_route = self._neighnour_route(current_route)
                new_dist = self._total_distance(new_route)

                # 计算距离差
                delta = new_dist - current_dist

                # 判断是否接受新解
                if delta < 0 or random.random() < math.exp(-delta / temperature): # 
