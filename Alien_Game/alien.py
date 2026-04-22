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
