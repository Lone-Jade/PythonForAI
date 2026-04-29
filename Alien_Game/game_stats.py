
class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings  # 获取游戏设置对象
        self.reset_stats()  # 初始化游戏统计信息

    def reset_stats(self):
        # 初始化游戏统计信息
        self.ships_left = self.settings.ship_limit  # 飞船剩余数量
        self.score = 0  # 游戏得分