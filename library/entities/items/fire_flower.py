import pygame

from library.entities.items.item import Item
from library.timer import Timer


class FireFlower(Item):

    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/fire_flower_1.png")
        self.item_type = 3
        images =\
            [pygame.image.load("resources/images/fire_flower_" + str(x) + ".png").convert_alpha() for x in range(1, 4)]
        images.append(pygame.image.load("resources/images/fire_flower_2.png").convert_alpha())
        self.sway_animation = Timer(images, wait=250)

    def update(self, level, scrolling, vel_x=None):
        """Pops out and remains still."""
        if scrolling:
            if vel_x:
                self.rect.x += vel_x
            else:
                self.rect.x += self.scroll_rate
                if self.out_of_bounds():
                    self.kill()
        self.rect.y += self.velocity.y
        if self.rect.bottom >= self.position[1]:
            self.rect.bottom = self.position[1]
        self.fall()

    def draw(self):
        super().set_image(self.sway_animation.get_image())
        super().draw()
