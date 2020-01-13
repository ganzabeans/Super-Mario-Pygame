from library.entities.items.item import Item


class Mushroom(Item):

    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/mushroom.png")
        self.item_type = 2
        self.is_active = False

    def update(self, level, scrolling, vel_x=None):
        super().update(level, scrolling, vel_x)
        # Prevent colliding while popping out of block
        if self.velocity.y <= 0:
            self.is_active = True

    def on_horizontal_collision(self):
        if self.is_active:
            self.direction *= -1
