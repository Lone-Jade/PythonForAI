import math
import random
import matplotlib.pyplot as plt
import numpy as np

# ======================== 1. 城市坐标数据（直接定义） ========================
# 城市名称与坐标 (x, y) 对应题目中的表格
cities = {
    "北京": (9932, 4439),
    "天津": (10109, 4351),
    "上海": (11552, 3472),
    "重庆": (10302, 3290),
    "拉萨": (8776, 3333),
    "乌鲁木齐": (7040, 4867),
    "银川": (9252, 4278),
    "呼和浩特": (9395, 4545),
    "南宁": (11101, 2540),
    "哈尔滨": (9825, 5087),
    "长春": (10047, 4879),
    "沈阳": (10227, 4648),
    "石家庄": (10027, 4229),
    "太原": (9878, 4211),
    "西宁": (9087, 4065),
    "济南": (10438, 4075),
    "郑州": (10382, 3865),
    "南京": (11196, 3563),
    "合肥": (11075, 3543),
    "杭州": (11533, 4365),
    "福州": (11915, 2900),
    "南昌": (11305, 3189),
    "长沙": (11073, 3137),
    "武汉": (10950, 3394),
    "广州": (11576, 2575),
    "台北": (12239, 2785),
    "海口": (11529, 2226),
    "兰州": (9328, 4006),
    "西安": (10012, 3811),
    "成都": (9952, 3410),
    "贵阳": (10612, 2954),
    "昆明": (10349, 2784),
    "香港": (11747, 2469),
    "澳门": (11673, 2461),
}

# 将城市名和坐标转为列表，便于索引操作
city_names = list(cities.keys())
coords = np.array([cities[name] for name in city_names])
num_cities = len(city_names)

# ======================== 2. 辅助函数 ========================
def distance(city_a, city_b):
    """计算两个城市之间的欧氏距离（题目坐标为平面坐标，可直接计算）"""
    return math.hypot(city_a[0] - city_b[0], city_a[1] - city_b[1])

def total_distance(route):
    """计算一条路径的总距离（闭合回路，需返回起点）"""
    dist = 0
    for i in range(len(route)):
        dist += distance(coords[route[i]], coords[route[(i+1) % len(route)]])
    return dist

# ======================== 3. 最近邻算法构造初始路径 ========================
def nearest_neighbor(start=0):
    """
    最近邻算法：从指定起点出发，每次选择未访问的最近城市。
    返回路径（城市索引列表）。
    """
    unvisited = set(range(num_cities))
    route = [start]
    unvisited.remove(start)
    current = start
    while unvisited:
        # 找出未访问中距离当前城市最近的那个
        next_city = min(unvisited, key=lambda city: distance(coords[current], coords[city]))
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    return route

# ======================== 4. 2-opt 局部搜索优化 ========================
def two_opt(route, max_attempts=1000):
    """
    2-opt 优化：反复反转路径中的子段，若总距离变短则接受。
    返回优化后的路径和最终距离。
    """
    best_route = route[:]
    best_dist = total_distance(best_route)
    improved = True
    attempts = 0
    while improved and attempts < max_attempts:
        improved = False
        attempts += 1
        for i in range(1, num_cities - 1):
            for j in range(i+1, num_cities):
                # 反转 i 到 j 之间的子段
                new_route = best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:]
                new_dist = total_distance(new_route)
                if new_dist < best_dist - 1e-9:  # 有明显改进
                    best_route = new_route
                    best_dist = new_dist
                    improved = True
                    break  # 重置循环，重新开始扫描
            if improved:
                break
    return best_route, best_dist

# ======================== 5. 主流程 ========================
def main():
    # 5.1 尝试多个起点，选取最优的最近邻+2-opt结果
    best_overall_route = None
    best_overall_dist = float('inf')
    
    for start in range(num_cities):
        # 最近邻构造
        init_route = nearest_neighbor(start)
        init_dist = total_distance(init_route)
        # 2-opt 优化
        opt_route, opt_dist = two_opt(init_route)
        if opt_dist < best_overall_dist:
            best_overall_dist = opt_dist
            best_overall_route = opt_route
    
    # 5.2 输出结果
    print("最优路径（城市索引，从0开始）:")
    print(best_overall_route)
    print("\n最优路径（城市名称）:")
    route_names = [city_names[i] for i in best_overall_route] + [city_names[best_overall_route[0]]]  # 闭合回路
    print(" -> ".join(route_names))
    print(f"\n最短总距离: {best_overall_dist:.2f}")
    
    # 5.3 可视化
    # plt.figure(figsize=(12, 8))
    # # 绘制所有城市点
    # for name, (x, y) in cities.items():
    #     plt.scatter(x, y, c='blue', s=50)
    #     plt.annotate(name, (x, y), fontsize=8, ha='center', va='bottom')
    
    # # 绘制最优路径连线（闭合回路）
    # route_coords = coords[best_overall_route]
    # # 添加起点到终点的闭合连线
    # route_coords = np.vstack([route_coords, route_coords[0]])
    # plt.plot(route_coords[:, 0], route_coords[:, 1], 'r-', linewidth=1.5, alpha=0.7)
    
    # # 标记起点（绿色五角星）
    # start_city = city_names[best_overall_route[0]]
    # start_x, start_y = cities[start_city]
    # plt.scatter(start_x, start_y, c='green', s=100, marker='*', edgecolors='black', zorder=5)
    
    # plt.title(f"TSP 最优路径（总距离: {best_overall_dist:.2f}）", fontsize=14)
    # plt.xlabel("X 坐标")
    # plt.ylabel("Y 坐标")
    # plt.grid(True, linestyle='--', alpha=0.5)
    # plt.tight_layout()
    # plt.savefig("tsp_optimal_route.png", dpi=150)
    # plt.show()

if __name__ == "__main__":
    main()