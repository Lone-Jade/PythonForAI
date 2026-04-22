
class Settings:
    def __init__(self):
        """
        定义模拟退火算法的超参数
        """
        self.initial_temp = 5000.0  # 初始温度
        self.cooling_rate = 0.99  # 降温速率（每轮乘以该系数） 第一次0.997
        self.num_iter = 50  # 每个温度下的迭代次数 第一次500 发现迭代次数过多但已经收敛
        self.stop_temp = 1e-10  # 停止温度（低于此值终止）

        self.early_stop_patience = 50  # 早停参数，当连续early_stop_patience次迭代都没有提升时，停止训练