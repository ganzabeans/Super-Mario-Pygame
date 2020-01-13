import json

import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite


class Entity(Sprite):
    """Any object that moves and collides with terrain."""
    def __init__(self, settings, screen, position, data=None, direction=-1, death_delay=250):
        super().__init__()
        self.settings = settings
        self.scroll_rate = settings.scroll_rate
        self.gravity = settings.gravity
        self.velocity = Vector2()
        self.velocity.x = abs(settings.scroll_rate)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.position = position
        if data is not None:
            with open(data) as data_f:
                self.data = json.load(data_f)
        self.direction = direction  # -1 for left, 1 for right
        self.image = self.rect = None
        self.death_image = self.death_time = None
        self.death_delay = death_delay
        self.hit = False

    def init_image(self, image):
        """Called on constructor to initialize self.image and self.rect."""
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def init_mario_image(self, image):
        """Changes mario states without changing position."""
        self.image = image
        temp = self.rect.bottomright
        self.rect = self.image.get_rect()
        self.rect.bottomright = temp

    def set_image(self, image):
        """Updates the image that should be drawn."""
        self.image = image if self.direction == 1 else pygame.transform.flip(image, True, False)

    def fall(self):
        self.velocity.y += self.gravity

    def hit_sequence(self):
        self.hit = True
        self.death_time = pygame.time.get_ticks()

    def on_horizontal_collision(self):
        pass

    def on_vertical_collision(self):
        pass

    def handle_horizontal_collision(self, level):
        """Called after updating x-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            for collision in collisions:
                if self.direction == 1 and self.rect.right < collision.rect.left + 10:
                    self.rect.right = collision.rect.left
                    self.on_horizontal_collision()
                elif self.direction == -1 and self.rect.left > collision.rect.right - 10:
                    self.rect.left = collision.rect.right
                    self.on_horizontal_collision()

    def handle_vertical_collision(self, level):
        """Called after updating y-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            for collision in collisions:
                if self.velocity.y < 0 and self.rect.top > collision.rect.centery:
                    self.rect.top = collision.rect.bottom
                    self.on_vertical_collision()
                    self.velocity.y = 0
                elif self.velocity.y > 0 and self.rect.bottom < collision.rect.centery:
                    self.rect.bottom = collision.rect.top
                    self.on_vertical_collision()
        else:
            self.fall()

    def is_visible(self):
        return self.rect.x < self.screen_rect.width

    def update(self, level, scrolling, vel_x=None):
        if not self.hit:
            if vel_x:
                self.scroll_rate = vel_x
            else:
                self.scroll_rate = self.settings.scroll_rate

        # Change x-position
        if scrolling:
            self.rect.x += self.scroll_rate
            # Sprite is left of screen, remove it
            if self.out_of_bounds():
                self.kill()
        if self.hit:
            if self.awaited_death():
                self.kill()
        # Slow down movement speed
        elif self.is_visible() and not self.hit:
            self.rect.x += self.velocity.x * 0.25 * self.direction
            self.handle_horizontal_collision(level)
        if not self.hit:
            # Change y-position.
            self.rect.y += self.velocity.y
            # Sprite is under screen, remove it
            if self.rect.y > self.screen_rect.height:
                self.kill()
            self.handle_vertical_collision(level)

    def draw(self):
        if self.is_visible():
            self.screen.blit(self.image, self.rect)

    def awaited_death(self):
        """Returns True if death animation time is over."""
        return pygame.time.get_ticks() - self.death_time > self.death_delay

    def out_of_bounds(self):
        """Sprite is to left of screen."""
        return self.rect.right <= 0
