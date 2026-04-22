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