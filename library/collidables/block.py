from library.collidables.terrain import Terrain
from library.entities.items.mushroom import Mushroom
from library.entities.items.fire_flower import FireFlower
from library.entities.items.coin import Coin

import pygame.image


class Block(Terrain):
    """A single, small, solid, square object. Can contain an item.
    Item:
    0- Nothing
    1- Coin
    2- Mushroom
    """

    def __init__(self, settings, screen, image_name, position, level, re_entry, has_item=0):
        super().__init__(settings, screen, image_name, position, re_entry)
        self.has_item = has_item
        self.level = level
        self.settings = settings
        self.screen = screen
        self.type = "block"
        self.coin_sound = pygame.mixer.Sound("resources/sounds/coin.wav")
        self.powerup_appears_sound = pygame.mixer.Sound("resources/sounds/powerup_appears.wav")
        self.empty_image = pygame.image.load("resources/images/block.png").convert_alpha()

    def on_collision(self):
        pass

    def show_item(self, mario):
        """creates item tells level to add it to terrain"""
        self.image = self.empty_image
        if self.has_item == 1:
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(1).play(self.coin_sound)
            mario.player_score.coin_hit(mario)
            self.level.items.add(Coin(self.settings, self.screen, self.rect.topleft))
        elif mario.state == "small":
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(1).play(self.powerup_appears_sound)
            self.level.items.add(Mushroom(self.settings, self.screen, self.rect.topleft))
        elif mario.state == "big" or mario.state == "fire":
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(1).play(self.powerup_appears_sound)
            self.level.items.add(FireFlower(self.settings, self.screen, self.rect.topleft))
        self.has_item = 0

    def destroy(self):
        self.kill()
