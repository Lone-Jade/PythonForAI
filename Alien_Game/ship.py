import pygame


# Define the Ship class
class Ship:
    def __init__(self, ai_game):
        # ai_game is the game object
        self.screen = ai_game.screen
        # get its rect
        self.screen_rect = ai_game.screen.get_rect()
        # get the settings object
        self.settings = ai_game.settings
        # load the ship image
        self.image = pygame.image.load("./Alien_Game/images/ship.bmp")
        # get the rect of the ship image
        self.rect = self.image.get_rect()

        # load the ship's center
        self.center_ship()

    def center_ship(self):
        # center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        # draw the ship at its current position
        self.screen.blit(self.image, self.rect)