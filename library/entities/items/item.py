import pygame

from library.entities.entity import Entity


class Item(Entity):
    """"Class that handles items"""

    def __init__(self, settings, screen, position, image_name):
        super(Item, self).__init__(settings, screen, position)
        self.settings = settings
        self.scroll_rate = settings.scroll_rate
        self.screen = screen
        self.direction = 1
        super().init_image(pygame.image.load(image_name))
        self.velocity.y = -10  # Small bounce when item pops out
        self.gravity = settings.gravity / 2
        self.rect.y -= 10  # So Mario doesn't immediately touch item upon block hit
