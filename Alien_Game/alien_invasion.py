import pygame
import sys
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


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
        # 创建一个用于存储外星人的编组
        self.aliens = pygame.sprite.Group()
        # 创建外星人群
        self._creat_fleet()
        # 创建游戏统计对象
        self.stats = GameStats(self)

        # 设置游戏活动状态标志
        self.game_active = False  # 游戏开始时处于非活动状态
        self.play_button = Button(self, "Play")  # 创建一个Play按钮对象

        # 创建得分牌对象
        self.sb = Scoreboard(self)

    def _check_events(self):
        # 监听并处理游戏事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # 点击关闭按钮，退出游戏

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  # 处理按键按下事件

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)  # 处理按键松开事件

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
                self._check_play_button(mouse_pos)  # 检测Play按钮是否被点击

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
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()  # 按下Q键，退出游戏
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # 按下空格键，发射子弹

    def _check_play_button(self, mouse_pos):
        # 检测Play按钮是否被点击
        button_clicked = self.play_button.rect.collidepoint(
            mouse_pos
        )  # 检测鼠标点击位置是否在Play按钮范围内
        if button_clicked and not self.game_active:
            self.stats.reset_stats()  # 重置游戏统计数据
            self.game_active = True  # 设置游戏为活动状态

            self.bullets.empty()  # 删除现有子弹
            self.aliens.empty()  # 删除现有外星人

            self._creat_fleet()  # 创建一个新的舰队
            self.ship.center_ship()  # 将飞船重新放置在屏幕底部

            self.settings.initialize_dynamic_settings()  # 初始化动态设置

            self.sb.prep_score()  # 准备显示得分牌

            pygame.mouse.set_visible(False)  # 隐藏鼠标光标

    def _update_screen(self):
        # 重新绘制屏幕
        self.screen.fill(self.settings.bg_color)  # 用背景色填充屏幕
        self.ship.blitme()  # 将飞船绘制到屏幕上
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # 绘制所有子弹
        self.aliens.draw(self.screen)  # 绘制所有外星人

        if self.game_active == False:
            self.play_button.draw_button()  # 绘制Play按钮

        self.sb.show_score()  # 显示得分牌

        pygame.display.flip()  # 刷新显示整个屏幕

    def run_game(self):
        # 游戏主循环
        while True:
            # 1. 监听处理游戏事件
            self._check_events()

            # 2. 更新飞船、子弹、外星人舰队位置
            if self.game_active:  # 只有在游戏活动状态下才更新游戏对象
                self.ship.update()
                self._update_bullets()
                self._update_fleet()

            # 3. 重绘屏幕并刷新显示
            self._update_screen()

            self.clock.tick(60)  # 控制游戏帧率为60帧/秒

    def _fire_bullet(self):
        # 创建一个新子弹并将其加入到编组bullets中
        if (
            len(self.bullets) < self.settings.bullets_allowed
        ):  # 限制子弹数量不超过设置值
            bullet = Bullet(self)  # 创建一个子弹对象
            self.bullets.add(bullet)  # 将子弹对象加入编组

    def _update_bullets(self):
        # 更新子弹位置并删除已消失的子弹
        self.bullets.update()  # 更新子弹位置
        self._check_bullet_alien_collisions()  # 检测子弹和外星人碰撞

    def _creat_fleet(self):
        # 创建外星人群
        alien = Alien(self)  # 创建一个外星人对象
        alien_width, alien_height = alien.rect.size  # 获取外星人尺寸

        current_x, current_y = alien_width, alien_height  # 设置初始位置
        while current_y < self.settings.screen_height - 3 * alien_height:  # 循环创建行
            while (
                current_x < self.settings.screen_width - 2 * alien_width
            ):  # 循环创建外星人
                new_alien = Alien(self, current_x, current_y)  # 创建一个外星人对象
                self.aliens.add(new_alien)  # 将外星人对象加入编组
                current_x += alien_width * 2  # 更新x坐标，间隔一个外星人宽度
            current_x = alien_width  # 重置x坐标，开始新行
            current_y += alien_height * 2  # 更新y坐标，间隔一个外星人高度

    def _check_fleet_edges(self):
        # 舰队边缘检测
        for alien in self.aliens.sprites():
            if alien.check_edges():
                return True
        return False

    def _update_fleet(self):
        # 更新舰队位置
        is_out_of_edge = self._check_fleet_edges()  # 检测舰队是否碰到边缘
        if is_out_of_edge:
            self.settings.fleet_direction *= -1  # 碰到边缘，改变舰队移动方向
        self.aliens.update(is_out_of_edge)  # 更新所有外星人位置

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!")
            self._reset_game()  # 检测飞船与外星人碰撞

        self._check_aliens_bottom()  # 检测外星人是否到达屏幕底部

    def _check_aliens_bottom(self):
        # 检测外星人是否到达屏幕底部

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # print("Aliens get to bottom!!!")
                self._reset_game()  # 检测飞船与外星人碰撞
                break

    def _check_bullet_alien_collisions(self):
        # 检查子弹组与外星人组的碰撞
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  # 计算得分
            self.sb.prep_score()  # 准备显示得分牌
        # 如果外星人清空
        if not self.aliens:
            self.bullets.empty()  # 删除现有子弹
            self._creat_fleet()  # 创建一个新的舰队
            # 增加速度
            self.settings.increase_speed()

    def _reset_game(self):
        # 重置游戏状态
        self.stats.ships_left -= 1  # 减少飞船数量
        if self.stats.ships_left > 0:
            self.bullets.empty()  # 删除现有子弹
            self.aliens.empty()  # 删除现有外星人

            self._creat_fleet()  # 创建一个新的舰队
            self.ship.center_ship()  # 将飞船重新放置在屏幕底部\

            time.sleep(0.5)  # 暂停0.5秒，给玩家一个缓冲时间
        else:
            self.game_active = False  # 没有剩余飞船，游戏结束
            pygame.mouse.set_visible(True)  # 显示鼠标光标


if __name__ == "__main__":
    # 创建游戏实例并运行
    game = AlienInvasion()
    game.run_game()
