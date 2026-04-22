# Define the settings for the game
class Settings:
    def __init__(self):
        # 屏幕参数设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 4.5
        
        # 子弹设置
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 15  # 同时屏幕上允许的最大子弹数量

        # 舰队设置
        self.alien_speed = 1.0  # 外星人水平移动速度
        self.fleet_drop_speed = 10  # 外星人下落速度
        self.fleet_direction = 1  # fleet_direction为1表示向右移，为-1表示向左移
