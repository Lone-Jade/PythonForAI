import pygame


class Scoreboard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font(None, 48)
        self.prep_score()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)  # 四舍五入到最近的10的倍数
        score_str = f"{rounded_score:,}"

        # 1. 图片内容
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )
        # 2. 图片位置
        self.score_rect = self.score_image.get_rect()

        # 3.定位
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)