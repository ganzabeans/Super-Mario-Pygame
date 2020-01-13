import pygame

from library.collidables.terrain import Terrain


class Pipe(Terrain):
    """Can be entered."""

    def __init__(self, settings, screen, image_name, position, enter, re_entry):
        super().__init__(settings, screen, image_name, position, re_entry)
        self.enter = False
        self.exit = False
        self.image = pygame.image.load(image_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.rect.x -= re_entry

        if enter == 1:
            self.enter = True
        elif enter == 2:
            self.exit = False
