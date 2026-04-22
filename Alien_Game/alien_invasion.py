import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet


# 初始化游戏对象
class AlienInvasion:
    def __init__(self):
        pygame.init()  # 初始化pygame库
        # 导入游戏设置
        self.settings = Settings()

        # 设置游戏窗口，保存窗口尺寸
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN
        )  # 将游戏窗口设置为全屏模式
        self.settings.screen_width = (
            self.screen.get_rect().width
        )  # 更新设置中的窗口宽度
        self.settings.screen_height = (
            self.screen.get_rect().height
        )  # 更新设置中的窗口高度

        # 设置窗口标题
        pygame.display.set_caption("Alien Invasion")
        # 设置游戏时钟，控制帧率
        self.clock = pygame.time.Clock()
        # 创建飞船对象
        self.ship = Ship(self)

        # 创建一个用于存储子弹的编组
        self.bullets = pygame.sprite.Group()

    def _check_events(self):
        # 监听并处理游戏事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # 点击关闭按钮，退出游戏

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  # 处理按键按下事件

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)  # 处理按键松开事件

    def _check_keyup_events(self, event):
        # 处理按键松开事件
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False  # 停止左移
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False  # 停止右移
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False  # 停止上移
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False  # 停止下移

    def _check_keydown_events(self, event):
        # 处理按键按下事件
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True  # 开启左移
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True  # 开启右移
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True  # 开启上移
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True  # 开启下移
        elif event.key == pygame.K_q:
            sys.exit()  # 按下Q键，退出游戏
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # 按下空格键，发射子弹

    def _update_screen(self):
        # 重新绘制屏幕
        self.screen.fill(self.settings.bg_color)  # 用背景色填充屏幕
        self.ship.blitme()  # 将飞船绘制到屏幕上
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # 绘制所有子弹
        pygame.display.flip()  # 刷新显示整个屏幕

    def run_game(self):
        # 游戏主循环
        while True:
            # 1. 监听处理游戏事件
            self._check_events()

            # 2. 更新飞船、子弹
            self.ship.update()
            self._update_bullets()

            # 3. 重绘屏幕并刷新显示
            self._update_screen()

            self.clock.tick(60)  # 控制游戏帧率为60帧/秒

    def _fire_bullet(self):
        # 创建一个新子弹并将其加入到编组bullets中
        if len(self.bullets) < self.settings.bullets_allowed:  # 限制子弹数量不超过设置值
            bullet = Bullet(self)  # 创建一个子弹对象
            self.bullets.add(bullet)  # 将子弹对象加入编组

    def _update_bullets(self):
        # 更新子弹位置并删除已消失的子弹
        self.bullets.update()  # 更新子弹位置


if __name__ == "__main__":
    # 创建游戏实例并运行
    game = AlienInvasion()
    game.run_game()
