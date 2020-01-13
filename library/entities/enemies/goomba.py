from library.entities.enemies.enemy import Enemy

import pygame


class Goomba(Enemy):
    """A strange mushroom."""

    def __init__(self, settings, screen, position):
        super().__init__(settings, screen, position, "resources/goomba.json")
        self.hit_image = pygame.image.load("resources/images/gh2.png")
