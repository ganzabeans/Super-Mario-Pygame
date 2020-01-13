from library.entities.items.item import Item


class Star(Item):

    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/star.png")
        self.item_type = 4
        self.gravity = 0.25

    def on_horizontal_collision(self):
        self.direction *= -1

    def on_vertical_collision(self):
        self.velocity.y = -6
