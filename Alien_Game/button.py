import pygame


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50  # 设置按钮的宽度和高度
        self.button_color = (0, 135, 0)  # 设置按钮的颜色
        self.text_color = (255, 255, 255)  # 设置按钮文本的颜色
        self.font = pygame.font.SysFont(None, 48)  # 设置按钮文本的字体和大小

        self.rect = pygame.Rect(
            0, 0, self.width, self.height
        )  # 创建一个矩形对象来表示按钮
        self.rect.center = self.screen_rect.center  # 将按钮放在屏幕中心

        self._prep_msg(msg)  # 将msg渲染为图像，并将其放在按钮上

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  # 将文本图像放在按钮中心

    def draw_button(self):
        # 绘制按钮的背景
        self.screen.fill(self.button_color, self.rect)
        # 绘制按钮的文本
        self.screen.blit(self.msg_image, self.msg_image_rect)
