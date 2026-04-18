"""
题目：
假设一位旅行商需要访问下列这些城市，并最终返回起始城市，且每个城市仅经过一次。
给定以下城市坐标，编写 Python 代码找到最短的访问路径。
"""

# 导入必要的库
import math
import csv


# csv 文件中，第一列是城市名，第二列是X，第三列是Y，总共 34 个城市
# 例如
# 北京,9932,4439


# 定义城市类
class City:
    def __init__(self, path="data.csv", origin="北京"):
        """
        读取 csv 文件，初始化城市名和坐标
        :param path: csv 文件路径
        """
        self.path = path  # csv 文件路径
        self.cities, self.relative_coords = self.read_data()  # 读取城市名和坐标
        self.num_cities = len(self.cities)  # 城市数量
        self.origin = origin  # 起始城市名
        self.origin_index = self.get_index(origin)  # 起始城市索引
        self.distances = self.calculate_distances()  # 计算距离矩阵，即代价矩阵

    def read_data(self):
        """
        实现读取 csv 文件，返回城市名和坐标
        """
        cities = []
        relative_coords = []
        with open(self.path, "r", encoding="utf-8") as f:
            next(f)  # 跳过第一行
            reader = csv.reader(f)  # 读取 csv 文件
            for row in reader:
                cities.append(str(row[0]))  # 城市名
                relative_coords.append((int(row[1]), int(row[2])))  # 相对坐标
        return cities, relative_coords

    def calculate_distances(self):
        """
        计算距离矩阵
        """
        distances = [
            [0 for _ in range(self.num_cities)] for _ in range(self.num_cities)
        ]  # 初始化距离矩阵

        # 计算距离，形成 n * n 的距离矩阵图
        for i in range(self.num_cities):
            x1, y1 = self.relative_coords[i]
            for j in range(i + 1, self.num_cities):
                x2, y2 = self.relative_coords[j]
                distances[i][j] = distances[j][i] = math.hypot(
                    x2 - x1, y2 - y1
                )  # 计算两点之间的距离
        return distances

    def get_shortest_path(self):
        """
        获取最短路径，使用 贪心TSP 算法
        """
        n = self.num_cities
        visited = [False for _ in range(n)]
        path = []
        current = self.origin_index
        total_distance = 0

        # 经历 n 个城市
        for _ in range(n):
            path.append(current)
            visited[current] = True
            min_distance = math.inf  # 最小距离设置为无穷大
            next_city = -1  # 下一个城市索引

            # 遍历未访问的城市，找出离当前城市最近的未访问城市
            for i in range(n):
                if not visited[i] and self.distances[current][i] < min_distance:
                    min_distance = self.distances[current][i]
                    next_city = i

            # 未访问的城市数量为 0，说明已经回到起始城市，结束循环
            if next_city == -1:
                break

            # 更新当前城市和总距离
            current = next_city
            total_distance += min_distance

        # 回到起始城市
        total_distance += self.distances[current][self.origin_index]
        path.append(self.origin_index)

        path_names = [self.cities[i] for i in path]
        return path_names, total_distance

    def print_path(self, path):
        """
        打印路径
        """
        for i, city in enumerate(path):
            if i != self.num_cities:
                city_ = city + "->"
            else:
                city_ = city
            print(pad_string(city_, 12), end="")
            if (i + 1) % 10 == 0:
                print()
        print()

    def get_index(self, city_name):
        """
        获取城市名对应的索引
        """
        return self.cities.index(city_name)


# 以下为测试用函数，与主程序无关
def get_display_width(s):
    """计算字符串的实际显示宽度"""
    width = 0
    for char in s:
        if ord(char) > 127:  # 中文字符
            width += 2
        else:
            width += 1
    return width


def pad_string(s, total_width):
    """按显示宽度填充字符串"""
    current_width = get_display_width(s)
    padding = total_width - current_width
    return s + " " * padding


# 主程序
if __name__ == "__main__":
    # 实例化 City 类
    city = City("./Homework_Midterm/data.csv")

    # 测试
    length = city.num_cities
    print(length)
    # 打印城市名
    for i in range(length):
        print(pad_string(city.cities[i], 10), end="")
        if (i + 1) % 10 == 0:
            print()
    print()
    # 打印坐标
    # for i in range(length):
    #     print(f"Start from {city.cities[i]}")
    #     for j in range(length):
    #         print(f"{city.distances[i][j]:.2f}", end=" ")
    #         if (j + 1) % 10 == 0:
    #             print()

    #     print()

    # 打印结果
    print("The shortest path is:")
    path_name, min_distance = city.get_shortest_path()
    city.print_path(path_name)
