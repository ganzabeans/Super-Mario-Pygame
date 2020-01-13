import pygame

from library.entities.entity import Entity
from library.timer import Timer


class Fireball(Entity):

    def __init__(self, settings, screen, position, direction):
        super().__init__(settings, screen, position, direction=direction)
        super().init_image(pygame.image.load("resources/images/fireball.png"))
        self.scroll_rate = settings.scroll_rate
        self.spin_animation = self.load_spin_animation()
        self.death_animation = self.load_death_animation()
        self.velocity.x = 10
        self.height = 5
        self.gravity = 1

    def load_spin_animation(self):
        """Spins while moving."""
        animation = []
        for x in range(4):
            rotated_image = pygame.transform.rotate(self.image, 90 * x)
            animation.append(rotated_image)
        return Timer(animation)

    def load_death_animation(self):
        """Shrinks when collided with terrain."""
        animation = []
        death_image = pygame.image.load("resources/images/boom.png").convert_alpha()
        for x in range(1, 7):
            scale = self.rect.width - 2 * x, self.rect.height - 2 * x
            scaled_image = pygame.transform.scale(death_image, scale).convert_alpha()
            animation.append(scaled_image)
        return Timer(animation, wait=self.death_delay/6)

    def handle_horizontal_collision(self, level):
        """Called after updating x-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            for collision in collisions:
                if self.rect.right < collision.rect.left + 50 or self.rect.left > collision.rect.right - 50:
                    super().hit_sequence()
                    break

    def handle_vertical_collision(self, level):
        """Called after updating y-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            self.height = 4
            self.gravity -= 0.1
            for collision in collisions:
                # Collision with ceilings
                if self.velocity.y < 0 and self.rect.top > collision.rect.bottom:
                    self.rect.top = collision.rect.bottom
                    self.velocity.y = 0
                    self.height = 0
                # Odd conditionals, but seems to fix fireball clipping through floor
                elif ((self.velocity.y > 0 and self.rect.bottom < collision.rect.top)
                        or collision.rect.collidepoint(self.rect.center)):
                    self.rect.bottom = collision.rect.top

    def update(self, level, scrolling, vel_x=None):
        if vel_x:
            self.scroll_rate = vel_x
        else:
            self.scroll_rate = self.settings.scroll_rate

        if self.hit:
            if scrolling:
                self.rect.x += self.scroll_rate
                if self.out_of_bounds():
                    self.kill()
            if super().awaited_death():
                self.kill()
        else:
            # x-position
            self.rect.x += self.velocity.x * self.direction
            if self.out_of_bounds():
                self.kill()
            self.handle_horizontal_collision(level)
            # y-position
            self.velocity.y = (-1 if self.height > 0 else 1) * (self.gravity * self.height**2)
            self.rect.y += self.velocity.y
            self.height -= 0.5
            self.handle_vertical_collision(level)

    def draw(self):
        if self.hit:
            super().set_image(self.death_animation.get_image())
        else:
            super().set_image(self.spin_animation.get_image())
        super().draw()

    def out_of_bounds(self):
        """Sprite is to left or right of screen"""
        return self.rect.right <= 0 or self.rect.left >= self.screen_rect.width
