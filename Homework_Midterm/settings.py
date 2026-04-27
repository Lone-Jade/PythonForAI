class Settings:
    def __init__(self):
        """
        定义模拟退火算法的超参数
        """
        self.initial_temp = 5000.0  # 初始温度
        self.cooling_rate = 0.99  # 降温速率（每轮乘以该系数） 第一次使用0.997
        self.num_iter = 50  # 每个温度下的迭代次数 第一次使用500 发现迭代次数过多但已经收敛，调整cooling_rate和num_iter为现在的值
        self.stop_temp = 1e-10  # 停止温度（低于此值终止）
