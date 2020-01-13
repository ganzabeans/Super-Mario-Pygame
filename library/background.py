import pygame


class Background:
    """Image in the background."""

    def __init__(self, settings, screen, image_name):
        self.scroll_rate = settings.bg_scroll_rate
        self.screen = screen
        self.image = None
        try:
            self.image = pygame.image.load(image_name).convert()
        except KeyError:
            pass
        self.x = 0

    def draw(self):
        if self.image is not None:
            self.screen.blit(self.image, (self.x, 0))

    def update(self):
        self.x += self.scroll_rate
