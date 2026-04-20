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
import time


plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# csv 文件中，第一列是城市名，第二列是X，第三列是Y，总共 34 个城市
# 例如
# 北京,9932,4439


# 使用模拟退火算法解决旅行商问题
class SimulatedAnnealingTSP:
    def __init__(self, cities, coordinates, origin="北京"):
        """
        初始化模拟退火算法解决旅行商问题
        :param path: 城市坐标数据文件路径
        :param origin: 起始城市
        """

        self.origin = origin  # 起始城市
        self.cities = cities  # 加载城市数据
        self.coordinates = coordinates  # 加载城市坐标
        self.num_cities = len(self.cities)  # 城市数量
        self.origin_index = self._get_index(origin) if origin else None  # 起始城市索引
        self.distances = np.array(
            self._cal_matrix_distance()
        )  # 城市距离矩阵，并转换为 NumPy 数组以加速计算

        # 模拟退火算法超参数
        self.initial_temp = 5000.0  # 初始温度
        self.cooling_rate = 0.997  # 降温速率（每轮乘以该系数）
        self.num_iter = 100  # 每个温度下的迭代次数
        self.stop_temp = 1e-10  # 停止温度（低于此值终止）

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
        length = len(route)
        for i in range(length):
            dist += self.distances[route[i]][route[(i + 1) % length]]
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

    def _greed_route(self):
        """
        生成贪婪算法的访问路径
        :return: 访问路径，第一个元素是起始城市，其余为其余城市的顺序
        """
        unvisited = set(range(self.num_cities))
        unvisited.remove(self.origin_index)
        route = [self.origin_index]
        while unvisited:
            last = route[-1]
            next_city = min(unvisited, key=lambda c: self.distances[last][c])
            route.append(next_city)
            unvisited.remove(next_city)
        return route

    def _get_index(self, city_name):
        """
        获取城市名称对应的索引
        :param city_name: 城市名称
        :return: 城市索引
        """
        try:
            return self.cities.index(city_name)
        except:
            raise ValueError(f"{city_name}不在数据之中")

    def _neighour_route(self, route):
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
        # current_route = self._random_route()  # 随机生成初始路径，优化为贪婪算法生成初始路径，通常更接近最优解，能加速收敛
        current_route = self._greed_route()  # 使用贪婪算法生成初始路径
        current_dist = self._total_distance(current_route)  # 计算初始路径距离

        best_route = current_route.copy()  # 最优路径
        best_dist = current_dist  # 最优路径距离

        temperature = self.initial_temp  # 初始温度

        # 2. 执行模拟退火算法
        while temperature > self.stop_temp:
            for _ in range(self.num_iter):
                # 生成新解
                new_route = self._neighour_route(current_route)
                new_dist = self._total_distance(new_route)

                # 计算距离差
                delta = new_dist - current_dist

                # 判断是否接受新解
                if delta < 0 or random.random() < math.exp(
                    -delta / temperature
                ):  # Metropolis 准则
                    current_route = new_route
                    current_dist = new_dist
                    # 更新最优解
                    if current_dist < best_dist:
                        best_route = current_route.copy()
                        best_dist = current_dist

            # 降温
            temperature *= self.cooling_rate
            # 优化：自适应降温
            # if best_dist < current_dist * 0.95:
            #     temperature *= 0.998  # 找到更优解：慢降温
            # else:
            #     temperature *= 0.99  # 没找到：快降温

        return best_route, best_dist

    def print_route(self, route):
        """
        打印访问路径
        :param route: 访问路径
        """
        length = len(route)
        for i in range(length):
            city_str = self.cities[route[i]] + " -> "
            print(pad_string(city_str, 12), end="")
            if (i + 1) % 10 == 0:
                print()  # 每行打印10个城市，保持整齐
        city_end_str = self.cities[route[0]]  # 最后返回起点
        print(pad_string(city_end_str, 12))
        print()

    def plot_route(self, route, best_dist):
        """
        可视化TSP最优路径：带城市名称、方向箭头、起点高亮
        :param route: 最优路径索引列表
        :param best_dist: 最短总距离
        """
        plt.figure(figsize=(12, 9), dpi=100)

        # 获取所有城市坐标
        x = [self.coordinates[i][0] for i in range(self.num_cities)]
        y = [self.coordinates[i][1] for i in range(self.num_cities)]

        # 绘制所有城市点（灰色）
        plt.scatter(x, y, c="lightgray", s=60, alpha=0.7, label="所有城市")

        # 绘制最优路径（蓝色带箭头）
        route_x = [self.coordinates[i][0] for i in route]
        route_y = [self.coordinates[i][1] for i in route]
        # 闭合回路（回到起点）
        route_x.append(route_x[0])
        route_y.append(route_y[0])

        # 画路径线
        plt.plot(
            route_x, route_y, c="#1f77b4", linewidth=2.5, alpha=0.8, label="访问路径"
        )

        # 绘制方向箭头（显示行走方向）
        for i in range(len(route_x) - 1):
            plt.arrow(
                route_x[i],
                route_y[i],  # 起点
                route_x[i + 1] - route_x[i],  # dx
                route_y[i + 1] - route_y[i],  # dy
                head_width=80,
                head_length=80,
                fc="#1f77b4",
                ec="#1f77b4",
                length_includes_head=True,
                alpha=0.7,
            )

        # 高亮起点（北京）：红色大圆点
        origin_x, origin_y = self.coordinates[self.origin_index]
        plt.scatter(
            origin_x,
            origin_y,
            c="red",
            s=180,
            marker="o",
            edgecolors="darkred",
            label="起点(北京)",
            zorder=5,
        )

        # 标注城市名称（只标注路径上的城市）
        for i in route:
            cx, cy = self.coordinates[i]
            city_name = self.cities[i]
            plt.annotate(
                city_name,
                (cx, cy),
                fontsize=9,
                ha="right",
                color="black",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7),
            )

        # 图表标题与标签
        plt.title(
            f"模拟退火TSP最优路径\n总距离：{best_dist:.2f} | 城市数：{self.num_cities}",
            fontsize=14,
            pad=20,
        )
        plt.xlabel("X 坐标", fontsize=12)
        plt.ylabel("Y 坐标", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.show()


# 辅助函数
def get_display_width(s):
    """计算字符串的实际显示宽度（中文占2，英文占1）"""
    width = 0
    for char in s:
        if ord(char) > 127:
            width += 2
        else:
            width += 1
    return width


def pad_string(s, total_width):
    """按显示宽度填充空格，用于对齐打印"""
    current_width = get_display_width(s)
    padding = total_width - current_width
    return s + " " * padding


if __name__ == "__main__":
    # key = input("是否需要固定随机数种子以确保结果可复现？(y/n): ").strip().lower()
    # 设置随机数种子，确保结果可复现
    key = "n"
    random.seed(42) if key == "y" else None

    # 导入csv文件，获取城市列表和坐标
    csv_path = "./Homework_Midterm/data.csv"
    cities = []
    coordinates = []

    start_time = time.time()  # 记录开始时间

    # 读取csv文件
    with open(csv_path, "r", encoding="utf-8") as f:
        next(f)  # 跳过表头
        reader = csv.reader(f)
        for row in reader:
            city_name = row[0].strip()
            x = int(row[1])
            y = int(row[2])
            cities.append(city_name)
            coordinates.append((x, y))

    # 实例化模拟退火算法类
    sa_tsp = SimulatedAnnealingTSP(cities, coordinates, origin="北京")
    # 执行模拟退火算法，获取最短路径和对应距离
    best_route, best_dist = sa_tsp.simulated_annealing()

    # 测试基本信息
    print(f"城市数量: {sa_tsp.num_cities}")
    print("城市列表（每行10个）:")
    for i, name in enumerate(sa_tsp.cities):
        print(pad_string(name, 10), end="")
        if (i + 1) % 10 == 0:
            print()
    print("\n" + "=" * 60)

    # 打印最短路径和对应距离
    print("最短访问路径:")
    sa_tsp.print_route(best_route)
    print(f"最短距离: {best_dist:.2f}")
    sa_tsp.plot_route(best_route, best_dist)  # 可视化最短路径
    print(f"运行时间: {time.time() - start_time:.2f}秒")
