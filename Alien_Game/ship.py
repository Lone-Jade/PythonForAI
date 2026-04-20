import pygame


# 定义飞船类
class Ship:
    def __init__(self, ai_game):
        # ai_game 是外星人入侵游戏的主实例对象
        self.screen = ai_game.screen
        # 获取游戏屏幕的矩形区域
        self.screen_rect = ai_game.screen.get_rect()
        # 获取游戏设置对象
        self.settings = ai_game.settings
        # 加载飞船图片资源
        self.image = pygame.image.load("./Alien_Game/images/ship.bmp")
        # 获取飞船图片的矩形区域
        self.rect = self.image.get_rect()

        # 将飞船放置在屏幕底部中央
        self.center_ship()

        # 初始化飞船移动标志位，默认为停止状态
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        # 将飞船居中放置在屏幕底部中央位置
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        # 在当前位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 根据移动标志位更新飞船的位置
        # 向左移动，且不超出屏幕左边界
        if self.moving_left and self.rect.left > 0:
            self.rect.left -= self.settings.ship_speed
        # 向右移动，且不超出屏幕右边界
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.right += self.settings.ship_speed
        # 向下移动，且不超出屏幕下边界
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += self.settings.ship_speed
        # 向上移动，且不超出屏幕上边界
        if self.moving_up and self.rect.top > 0:
            self.rect.top -= self.settings.ship_speed
