import pygame
import sys
from setting import Settings
from ship import Ship


# Init Game Objects
class AlienInvasion:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        # import settings
        self.settings = Settings()
        # Set the display surface, save the display size
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # Set the window title
        pygame.display.set_caption("Alien Invasion")
        # Set timer for the game
        self.clock = pygame.time.Clock()
        # Create a ship object
        self.ship = Ship(self)

    def _check_events(self):
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        # Redraw the screen
        self.screen.fill(self.settings.bg_color)  # fill the screen with black color
        self.ship.blitme()  # blit the ship to the screen
        pygame.display.flip()  # refresh the display

    def run_game(self):
        # Game loop
        while True:
            # 1st event loop
            self._check_events()

            # 2nd postion and number of aliens update


            # 3rd redraw the screen and refresh the display
            self._update_screen()

            self.clock.tick(60)  # set the game speed to 60 frames per second


if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()
