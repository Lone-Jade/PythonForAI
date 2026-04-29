# Define the settings for the game
class Settings:
    def __init__(self):
        # 屏幕参数设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船设置
        # self.ship_speed = 4.5
        self.ship_limit = 3  # 飞船的生命值
        
        # 子弹设置
        # self.bullet_speed = 3.0
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 15  # 同时屏幕上允许的最大子弹数量

        # 舰队设置
        # self.alien_speed = 1.0  # 外星人水平移动速度
        self.fleet_drop_speed = 10  # 外星人下落速度
        # self.fleet_direction = 1  # fleet_direction为1表示向右移，为-1表示向左移
        self.initialize_dynamic_settings()

        # 提速比例
        self.speedup_scale = 1.1
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        self.ship_speed = 4.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)