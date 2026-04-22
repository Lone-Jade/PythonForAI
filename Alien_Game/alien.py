import pygame
from pygame.sprite import Sprite
from settings import Settings


class Alien(Sprite):
    def __init__(self, ai_game, x_pos=0, y_pos=0):
        super().__init__()  # 调用父类的初始化方法
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 外星人的图像和尺寸
        self.image = pygame.image.load("./Alien_Game/images/alien.bmp")
        self.rect = self.image.get_rect()

        # 外星人初始位置
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self, is_move_down=False):
        # 更新外星人位置
        if is_move_down:
            self.rect.y += self.settings.fleet_drop_speed  # 向下移动
        self.rect.x += self.settings.alien_speed * self.settings.fleet_direction
    
    def check_edges(self):
        # 检查外星人是否碰到屏幕边缘
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False