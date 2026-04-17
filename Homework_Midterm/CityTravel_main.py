"""
题目：
假设一位旅行商需要访问下列这些城市，并最终返回起始城市，且每个城市仅经过一次。
给定以下城市坐标，编写 Python 代码找到最短的访问路径。
"""

# 导入必要的库
import math
import csv

# csv 文件中，第一列是城市名，第二列是X，第三列是Y


# 定义城市类
class City:
    def __init__(self, path="data.csv"):
        self.path = path  # csv 文件路径
        self.cities, self.relative_coords = self.read_data()  # 读取城市名和坐标
        self.num_cities = len(self.cities)  # 城市数量
        self.x0, self.y0 = self.relative_coords[0]  # 起始城市坐标, 即北京的坐标
        self.relative_coords = [
            (x - self.x0, y - self.y0) for x, y in self.relative_coords
        ]  # 相对坐标
        self.distances = self.calculate_distances()  # 计算距离矩阵

    def read_data(self):
        cities = []
        relative_coords = []
        with open(self.path, "r", encoding="utf-8") as f:
            next(f)  # 跳过第一行
            reader = csv.reader(f)
            for row in reader:
                cities.append(row[0])
                relative_coords.append((int(row[1]), int(row[2])))
        return cities, relative_coords
    
    def calculate_distances(self):
        distances = [[0 for _ in range(self.num_cities)] for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                x1, y1 = self.relative_coords[i]
                x2, y2 = self.relative_coords[j]
                distances[i][j] = distances[j][i] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distances




if __name__ == "__main__":
    # 实例化 City 类
    city = City("./Homework_Midterm/data.csv")

    # 测试
    print(city.cities)
    print(city.relative_coords)
    print(city.distances)
