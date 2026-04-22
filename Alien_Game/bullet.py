import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()  # 调用父类的初始化方法
        self.screen = ai_game.screen  # 获取游戏屏幕对象
        self.settings = ai_game.settings  # 获取游戏设置对象
        self.color = self.settings.bullet_color  # 获取子弹颜色设置

        # 创建子弹rect对象
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )

        # 子弹定位
        self.rect.midtop = ai_game.ship.rect.midtop


    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.rect.bottom -= self.settings.bullet_speed  # 更新子弹位置（向上移动）
        if self.rect.bottom <= 0:  # 如果子弹超出屏幕，则删除子弹
            self.kill()