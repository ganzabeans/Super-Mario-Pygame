import pygame

from library.collidables.terrain import Terrain


class FlagPole(Terrain):
    """End-game flag pole."""

    def __init__(self, settings, screen, position, re_entry, level, mario):
        super().__init__(settings, screen, "resources/images/flag_pole.png", position, re_entry)
        self.level = level
        self.mario = mario
        self.is_flag_pole = True
        self.flag_image = pygame.image.load("resources/images/flag.png").convert()
        self.flag_rect = self.flag_image.get_rect()
        self.flag_rect.topleft = self.rect.x - 60, self.rect.y + 40

    def scroll(self, vel_x=None):
        if not self.settings.level_over:
            if vel_x:
                self.scroll_rate = vel_x
            else:
                self.scroll_rate = self.settings.scroll_rate
            self.flag_rect.x += self.scroll_rate
            self.rect.x += self.scroll_rate

            if self.mario.rect.right >= self.rect.left:
                self.mario.prep_castle_walk()
                self.mario.rect.x = self.rect.x - 15
                self.mario.rect.y = max(self.mario.rect.y, self.rect.y)

    def draw(self):
        """Draws non-collideable flag with collideable flag pole."""
        if super().is_visible():
            self.screen.blit(self.flag_image, self.flag_rect)
            self.screen.blit(self.image, self.rect)
