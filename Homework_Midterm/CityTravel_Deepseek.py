"""
题目：
假设一位旅行商需要访问下列这些城市，并最终返回起始城市，且每个城市仅经过一次。
给定以下城市坐标，编写 Python 代码找到最短的访问路径。
"""

import math
import csv
import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示和负号显示
plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


# 定义城市类
class City:
    def __init__(self, path="data.csv", origin="北京"):
        """
        读取 csv 文件，初始化城市名和坐标
        :param path: csv 文件路径
        :param origin: 起始城市名（用于最终输出路径的起点，若为 None 则使用最优回路原起点）
        """
        self.path = path
        self.cities, self.relative_coords = self.read_data()
        self.num_cities = len(self.cities)
        self.origin = origin
        self.origin_index = self.get_index(origin) if origin else None
        self.distances = self.calculate_distances()  # 距离矩阵

    def read_data(self):
        """读取 csv 文件，返回城市名列表和坐标列表"""
        cities = []
        relative_coords = []
        with open(self.path, "r", encoding="utf-8") as f:
            next(f)  # 跳过标题行
            reader = csv.reader(f)
            for row in reader:
                cities.append(str(row[0]))
                relative_coords.append((int(row[1]), int(row[2])))
        return cities, relative_coords

    def calculate_distances(self):
        """计算对称距离矩阵（欧氏距离）"""
        distances = [[0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            x1, y1 = self.relative_coords[i]
            for j in range(i + 1, self.num_cities):
                x2, y2 = self.relative_coords[j]
                dist = math.hypot(x2 - x1, y2 - y1)
                distances[i][j] = distances[j][i] = dist
        return distances

    # ==================== 新增核心优化方法 ====================

    def _total_distance(self, route):
        """计算一条路径（城市索引列表，不闭合）的闭合回路总距离"""
        dist = 0
        for i in range(len(route)):
            dist += self.distances[route[i]][route[(i + 1) % len(route)]]
        return dist

    def _nearest_neighbor(self, start):
        """
        最近邻算法构造初始路径（从指定起点出发）
        返回路径列表（城市索引，未闭合）
        """
        n = self.num_cities
        visited = [False] * n
        route = [start]
        visited[start] = True
        current = start
        for _ in range(n - 1):
            # 寻找未访问中距离最近的城市
            next_city = min(
                (i for i in range(n) if not visited[i]),
                key=lambda i: self.distances[current][i],
            )
            route.append(next_city)
            visited[next_city] = True
            current = next_city
        return route

    def _two_opt(self, route, max_attempts=1000):
        """
        2-opt 局部搜索优化，反复反转子段以缩短总距离
        :param route: 初始路径（城市索引列表）
        :return: 优化后的路径、优化后的总距离
        """
        best_route = route[:]
        best_dist = self._total_distance(best_route)
        improved = True
        attempts = 0
        n = self.num_cities
        while improved and attempts < max_attempts:
            improved = False
            attempts += 1
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    # 反转 i 到 j 之间的子段
                    new_route = (
                        best_route[:i]
                        + best_route[i : j + 1][::-1]
                        + best_route[j + 1 :]
                    )
                    new_dist = self._total_distance(new_route)
                    if new_dist < best_dist - 1e-9:  # 有明显改进
                        best_route = new_route
                        best_dist = new_dist
                        improved = True
                        break  # 重置外层循环
                if improved:
                    break
        return best_route, best_dist

    def _rotate_route(self, route, target_start_index):
        """
        将路径循环旋转，使得新路径的起点为 target_start_index
        注意：route 是未闭合的路径（长度 = 城市数），旋转后仍保持相对顺序
        """
        if target_start_index not in route:
            raise ValueError(f"目标起点 {target_start_index} 不在路径中")
        pos = route.index(target_start_index)
        return route[pos:] + route[:pos]

    def get_shortest_path(self, optimize=True, rotate_to_origin=True):
        """
        获取最短路径（改进版：多起点最近邻 + 2-opt 优化）
        :param optimize: 是否进行 2-opt 优化，默认为 True
        :param rotate_to_origin: 是否将最终路径旋转到 self.origin 作为起点，默认为 True
        :return: (path_names, total_distance)   path_names 为城市名列表（含闭合起点）
        """
        best_route = None
        best_dist = float("inf")

        # 遍历每个城市作为起点，执行最近邻 + 可选优化
        for start in range(self.num_cities):
            init_route = self._nearest_neighbor(start)
            if optimize:
                opt_route, opt_dist = self._two_opt(init_route)
            else:
                opt_route, opt_dist = init_route, self._total_distance(init_route)

            if opt_dist < best_dist - 1e-9:
                best_dist = opt_dist
                best_route = opt_route

        # 如果需要，将最优路径的起点旋转为用户指定的 origin
        if rotate_to_origin and self.origin_index is not None:
            best_route = self._rotate_route(best_route, self.origin_index)

        # 构造闭合路径名列表（末尾添加起点以形成回路）
        path_names = [self.cities[i] for i in best_route] + [self.cities[best_route[0]]]
        return path_names, best_dist

    # ==================== 原有辅助方法（保留并增强） ====================

    def print_path(self, path):
        """美化打印路径（每行最多10个城市）"""
        for i, city in enumerate(path):
            if i != len(path) - 1:
                city_str = city + "->"
            else:
                city_str = city
            print(pad_string(city_str, 12), end="")
            if (i + 1) % 10 == 0:
                print()
        print()

    def get_index(self, city_name):
        """根据城市名获取索引"""
        return self.cities.index(city_name)

    # ==================== 新增可视化方法 ====================

    def plot_path(self, path_names, savefig="tsp_route.png"):
        """
        可视化路径
        :param path_names: 城市名列表（闭合回路，最后一个与第一个相同）
        :param savefig: 保存图片文件名，若为 None 则不保存
        """
        # 获取路径对应的坐标
        route_coords = [
            self.relative_coords[self.cities.index(city)] for city in path_names[:-1]
        ]
        route_coords = np.array(route_coords)

        plt.figure(figsize=(12, 8))
        # 绘制所有城市点
        for name, (x, y) in zip(self.cities, self.relative_coords):
            plt.scatter(x, y, c="blue", s=50)
            plt.annotate(name, (x, y), fontsize=8, ha="center", va="bottom")

        # 绘制最优路径连线（闭合）
        plt.plot(route_coords[:, 0], route_coords[:, 1], "r-", linewidth=1.5, alpha=0.7)
        # 标记起点（绿色五角星）
        start_name = path_names[0]
        start_x, start_y = self.relative_coords[self.cities.index(start_name)]
        plt.scatter(
            start_x, start_y, c="green", s=100, marker="*", edgecolors="black", zorder=5
        )

        total_dist = self._total_distance(
            [self.cities.index(c) for c in path_names[:-1]]
        )
        plt.title(f"TSP 最优路径（总距离: {total_dist:.2f}）", fontsize=14)
        plt.xlabel("X 坐标")
        plt.ylabel("Y 坐标")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        if savefig:
            plt.savefig(savefig, dpi=150)
        plt.show()


# ==================== 辅助函数（与原代码保持一致） ====================
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


# 主程序
if __name__ == "__main__":
    # 实例化 City 类（请根据实际 CSV 文件路径修改）
    city = City("./Homework_Midterm/data.csv", origin="北京")

    # 测试基本信息
    print(f"城市数量: {city.num_cities}")
    print("城市列表（每行10个）:")
    for i, name in enumerate(city.cities):
        print(pad_string(name, 10), end="")
        if (i + 1) % 10 == 0:
            print()
    print("\n" + "=" * 60)

    # 获取优化后的最短路径（自动多起点+2-opt）
    print("正在搜索最优路径（多起点最近邻 + 2-opt优化）...")
    path_names, min_distance = city.get_shortest_path(
        optimize=True, rotate_to_origin=True
    )

    # 打印结果
    print("最优路径（城市名）:")
    city.print_path(path_names)
    print(f"最短总距离: {min_distance:.2f}")

    # 可视化
    city.plot_path(path_names, savefig="optimal_tsp_route.png")
