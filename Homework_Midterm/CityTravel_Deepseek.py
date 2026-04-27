"""
题目：
假设一位旅行商需要访问下列这些城市，并最终返回起始城市，且每个城市仅经过一次。
给定以下城市坐标，编写 Python 代码找到最短的访问路径。
"""

import math
import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置中文显示和负号显示（与模拟退火代码完全一致）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ==================== 辅助函数 ====================
def get_display_width(s):
    width = 0
    for char in s:
        if ord(char) > 127:
            width += 2
        else:
            width += 1
    return width

def pad_string(s, total_width):
    current_width = get_display_width(s)
    padding = total_width - current_width
    return s + " " * padding

# ==================== 统一风格的 TSP 类（2-opt 算法） ====================
class TwoOptTSP:
    def __init__(self, cities, coordinates, origin="北京"):
        """
        初始化 2-opt 算法解决旅行商问题（与模拟退火类结构一致）
        :param cities: 城市名称列表
        :param coordinates: 城市坐标列表
        :param origin: 起始城市
        """
        self.origin = origin
        self.cities = cities
        self.coordinates = np.asarray(coordinates, dtype=np.float64)
        self.num_cities = len(self.cities)
        self.origin_index = self._get_index(origin)
        self.distances = self._cal_matrix_distance()

    def _cal_matrix_distance(self):
        """矩阵距离计算（与模拟退火完全一致）"""
        diff = self.coordinates[:, np.newaxis, :] - self.coordinates[np.newaxis, :, :]
        dist = np.sqrt(np.sum(diff ** 2, axis=-1))
        return dist

    def _total_distance(self, route):
        """总距离计算（统一 numpy 加速）"""
        route = np.asarray(route)
        next_arr = np.roll(route, -1)
        total_dist = np.sum(self.distances[route, next_arr])
        return total_dist

    def _get_index(self, city_name):
        try:
            return self.cities.index(city_name)
        except:
            raise ValueError(f"{city_name} 不在城市列表中")

    # ==================== 2-opt 算法核心（逻辑完全不变） ====================
    def _nearest_neighbor(self, start):
        n = self.num_cities
        visited = [False] * n
        route = [start]
        visited[start] = True
        current = start
        for _ in range(n - 1):
            next_city = min(
                (i for i in range(n) if not visited[i]),
                key=lambda i: self.distances[current][i]
            )
            route.append(next_city)
            visited[next_city] = True
            current = next_city
        return route

    def _two_opt(self, route, max_attempts=1000):
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
                    new_route = best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:]
                    new_dist = self._total_distance(new_route)
                    if new_dist < best_dist - 1e-9:
                        best_route = new_route
                        best_dist = new_dist
                        improved = True
                        break
                if improved:
                    break
        return best_route, best_dist

    def _rotate_route(self, route, target_start_index):
        pos = route.index(target_start_index)
        return route[pos:] + route[:pos]

    def solve(self):
        """对外求解接口（统一风格）"""
        best_route = None
        best_dist = float("inf")
        for start in range(self.num_cities):
            init_route = self._nearest_neighbor(start)
            opt_route, opt_dist = self._two_opt(init_route)
            if opt_dist < best_dist:
                best_dist = opt_dist
                best_route = opt_route

        best_route = self._rotate_route(best_route, self.origin_index)
        return best_route, best_dist

    # ==================== 统一绘图（无超参数，结尾加 _2-opt） ====================
    def print_route(self, route):
        length = len(route)
        for i in range(length):
            city_str = self.cities[route[i]] + " -> "
            print(pad_string(city_str, 12), end="")
            if (i + 1) % 10 == 0:
                print()
        city_end_str = self.cities[route[0]]
        print(pad_string(city_end_str, 12))
        print()

    def plot_route(self, route, best_dist, save_path="."):
        plt.close("all")
        plt.figure(figsize=(12, 9), dpi=100)
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        plt.scatter(x, y, c="brown", s=60, alpha=0.7, label="所有城市")

        route_x = self.coordinates[route, 0].tolist()
        route_y = self.coordinates[route, 1].tolist()
        route_x.append(route_x[0])
        route_y.append(route_y[0])
        plt.plot(route_x, route_y, c="#1f77b4", linewidth=2.5, alpha=0.8, label="访问路径")

        for i in range(len(route_x)-1):
            dx = route_x[i+1] - route_x[i]
            dy = route_y[i+1] - route_y[i]
            plt.arrow(route_x[i], route_y[i], dx, dy, head_width=80, head_length=80,
                      fc="#1f77b4", ec="#1f77b4", length_includes_head=True, alpha=0.7)

        ox, oy = self.coordinates[self.origin_index]
        plt.scatter(ox, oy, c="red", s=180, marker="o", edgecolors="darkred", label="起点", zorder=5)

        for i in route:
            cx, cy = self.coordinates[i]
            plt.annotate(self.cities[i], (cx, cy), fontsize=9, ha="right",
                         bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))

        plt.title(f"2-opt TSP 最优路径\n总距离：{best_dist:.2f} | 城市数：{self.num_cities}", fontsize=14, pad=20)
        plt.xlabel("X 坐标", fontsize=12)
        plt.ylabel("Y 坐标", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper left")
        plt.tight_layout()

        if save_path:
            os.makedirs(save_path, exist_ok=True)
            # 文件名结尾加 _2-opt
            save_path = os.path.join(save_path, f"tsp_best_route_distance_{best_dist:.2f}_2-opt.png")
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"最优路径图已保存至: {save_path}")

# ==================== 读取 CSV（与主程序统一） ====================
def load_city_data(csv_path):
    cities = []
    coords = []
    with open(csv_path, "r", encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            cities.append(row[0])
            coords.append((int(row[1]), int(row[2])))
    return cities, coords

# ==================== 主程序 ====================
if __name__ == "__main__":
    csv_file = "./Homework_Midterm/data.csv"
    cities, coords = load_city_data(csv_file)

    tsp = TwoOptTSP(cities, coords, origin="北京")
    best_route, best_dist = tsp.solve()

    print("=" * 60)
    print("2-opt 算法求解 TSP 最优路径")
    print(f"最短距离：{best_dist:.2f}")
    print("最优路径：")
    tsp.print_route(best_route)
    tsp.plot_route(best_route, best_dist, save_path=".")