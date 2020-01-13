import pygame

from library.entities.items.item import Item
from library.timer import Timer


class Coin(Item):

    def __init__(self, settings, surface, position, floating=False):
        super().__init__(settings, surface, position, "resources/images/coin_1.png")
        self.item_type = 1
        self.y_limit = 30
        self.floating = floating
        images = [pygame.image.load("resources/images/coin_" + str(x) + ".png").convert_alpha() for x in range(1, 5)]
        self.spin_animation = Timer(images)

    def update(self, level, scrolling, vel_x=None):
        """Pops out and disappears."""
        if scrolling:
            if vel_x:
                self.rect.x += vel_x
            else:
                self.rect.x += self.scroll_rate
            if self.out_of_bounds():
                self.kill()
        if not self.floating:
            self.rect.y += self.velocity.y
            if self.rect.bottom >= self.position[1]:
                self.rect.bottom = self.position[1]
            self.fall()

    def draw(self):
        super().set_image(self.spin_animation.get_image())
        if not self.floating:
            self.y_limit -= 2
            if self.y_limit < 0:
                self.kill()
            else:
                self.rect.y -= 4
        super().draw()
