import pygame

from library.entities.enemies.enemy import Enemy


class Koopa(Enemy):
    """An upright turtle."""

    def __init__(self, settings, screen, position):
        super().__init__(settings, screen, position, "resources/koopa.json", 150)
        self.hit_image = pygame.image.load("resources/images/koopa_hit.png")
