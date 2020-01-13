import json

from pygame.sprite import Group

from library.collidables.brick import Brick
from library.collidables.dead_block import DeadBlock
from library.collidables.flag_pole import FlagPole
from library.collidables.item_block import ItemBlock
from library.collidables.terrain import Terrain
from library.collidables.pipe import Pipe
from library.collidables.stairs import Stairs
from library.entities.enemies.koopa import Koopa
from library.entities.enemies.goomba import Goomba
from library.background import Background
from library.entities.items.coin import Coin


class Level:
    """Handles the images and positions of assets."""

    def __init__(self, settings, screen, data, mario):
        self.settings = settings
        self.screen = screen
        self.is_underground = False
        self.is_surfacing = False
        self.exit = [0, 0]
        self.re_entry = 0
        self.exit_pipe = None
        self.mario = mario
        self.castle_layer = None
        self.pipe_group = None

        # Load data
        with open(data) as data_f:
            self.data = json.load(data_f)

        # Load sprite groups
        self.items = Group()
        self.blocks = self.load_blocks()
        self.terrain = self.load_terrain()
        self.terrain.add(self.blocks)

        self.enemies = self.load_enemies()

        self.background = Background(settings, screen, self.data["background"]["image"])

    def load(self, data, reset=False):
        with open(data) as data_f:
            self.data = json.load(data_f)

        self.re_entry = 0

        # Clear old data, then add new data
        if reset:
            self.items.empty()
            self.blocks.empty()
            self.terrain.empty()
            self.enemies.empty()

            self.items = self.load_items()
            self.blocks = self.load_blocks()
            self.terrain = self.load_terrain()
            self.terrain.add(self.blocks)
            self.enemies = self.load_enemies()

            self.background = Background(self.settings, self.screen, self.data["background"]["image"])

    def load_items(self):
        items = Group()
        for x in range(self.data["coins"]["count"]):
            position = self.data["coins"]["position"][x]
            coin = Coin(self.settings, self.screen, position, True)
            items.add(coin)
        return items

    def load_terrain(self):
        """Loads terrain sprites."""
        terrain = Group()
        # Pipes
        for x in range(self.data["pipe"]["count"]):
            position = self.data["pipe"]["position"][x]
            enter = self.data["pipe"]["enter"][x]
            if enter == 2:
                self.exit = position
            pipe = Pipe(self.settings, self.screen, "resources/images/pipe.png", position, enter, self.re_entry)
            terrain.add(pipe)

        # Down stairs; L shape
        stairs = Stairs(self.settings, self.screen, self.data["down_stairs"], 1, self.re_entry)
        terrain.add(stairs.blocks)
        # Up stairs; flipped L shape
        stairs = Stairs(self.settings, self.screen, self.data["up_stairs"], -1, self.re_entry)
        terrain.add(stairs.blocks)

        # Pillars
        for i in range(self.data["pillar"]["count"]):
            position = self.data["pillar"]["position"][i]
            pillar = Terrain(self.settings, self.screen, "resources/images/pillar.png", position, self.re_entry)
            terrain.add(pillar)

        # Castle
        image = self.data["castle"]["image"]
        position = self.data["castle"]["position"]
        castle = Terrain(self.settings, self.screen, image, position, self.re_entry)
        terrain.add(castle)
        # Castle top layer
        if self.data["castle"]["image"] == "resources/images/castle.png":
            position = self.data["castle"]["position"]
            self.castle_layer = Terrain(
                self.settings, self.screen, "resources/images/castle1.png", position, self.re_entry)
            self.castle_layer.rect.x += 116
            terrain.add(self.castle_layer)

        # Flag pole
        position = self.data["flag_pole"]
        pole = FlagPole(self.settings, self.screen, position, self.re_entry, self, self.mario)
        terrain.add(pole)
        # Ground
        for x in range(self.data["ground"]["count"]):
            image_name = self.data["ground"]["image"][x]
            position = self.data["ground"]["position"][x]
            ground = Terrain(self.settings, self.screen, image_name, position, self.re_entry)
            terrain.add(ground)
        return terrain

    def load_enemies(self):
        """Loads enemy sprites."""
        enemies = Group()
        # Goomba's
        for x in range(self.data["goomba"]["count"]):
            position = self.data["goomba"]["position"][x]
            position[0] += self.re_entry
            goomba = Goomba(self.settings, self.screen, position)
            enemies.add(goomba)
        # Koopa's
        for i in range(self.data["koopa"]["count"]):
            position = self.data["koopa"]["position"][i]
            position[0] += self.re_entry
            koopa = Koopa(self.settings, self.screen, position)
            enemies.add(koopa)
        return enemies

    def load_blocks(self):
        """Loads block sprites."""
        blocks = Group()
        # Yellow ? blocks
        for x in range(self.data["yellow"]["count"]):
            position = self.data["yellow"]["position"][x]
            has_item = self.data["yellow"]["item"][x]
            block = ItemBlock(self.settings, self.screen, position, self, self.re_entry, has_item)
            blocks.add(block)

        # Bricks
        for x in range(self.data["brick"]["count"]):
            position = self.data["brick"]["position"][x]
            image = self.data["brick"]["image"]
            has_item = self.data["brick"]["item"][x]
            block = Brick(self.settings, self.screen, image, position, self, self.re_entry, has_item)
            blocks.add(block)

        # Dead blocks
        for x in range(self.data["block"]["count"]):
            position = self.data["block"]["position"][x]
            block = DeadBlock(self.settings, self.screen, position, self, self.re_entry, )
            blocks.add(block)

        return blocks

    def create_underground(self):
        self.is_underground = True
        # empty everything
        self.terrain.empty()
        self.blocks.empty()
        self.items.empty()
        self.enemies.empty()

        # create background
        self.background = Background(self.settings, self.screen, self.data["underground"]["background"])

        # create undergorund terrain
        for x in range(self.data["underground"]["terrain"]["count"]):
            image_name = self.data["underground"]["terrain"]["image"][x]
            position = self.data["underground"]["terrain"]["position"][x]
            ground = Terrain(self.settings, self.screen, image_name, position, self.re_entry)
            self.terrain.add(ground)

        # Coins
        for x in range(self.data["underground"]["coin"]["count"]):
            position = self.data["underground"]["coin"]["position"][x]
            coin = Coin(self.settings, self.screen, position, True)
            self.items.add(coin)

        # load pipe
        self.pipe_group = Group()
        position = self.data["underground"]["pipe"]["position"]
        enter = 1
        self.exit_pipe = Pipe(self.settings, self.screen, self.data["underground"]["pipe"]["image"], position, enter,
                              self.re_entry)

    def go_surface(self):
        self.is_underground = False
        self.is_surfacing = True
        self.re_entry = self.exit[0]
        # empty everything
        self.terrain.empty()
        self.blocks.empty()
        self.items.empty()
        self.enemies.empty()

        # recreate groups
        self.blocks = self.load_blocks()
        self.terrain = self.load_terrain()
        self.terrain.add(self.blocks)
        self.enemies = self.load_enemies()

        self.background = Background(self.settings, self.screen, self.data["background"]["image"])

        return self.exit[1]

    def update(self, mario, scrolling, vel_x=None):
        """Scrolls all objects in the level, excluding Mario."""
        if self.is_underground:
            pass
        else:
            if scrolling and not mario.hit:
                self.background.update()

                for ground in self.terrain.sprites():
                    ground.scroll(vel_x)
            self.items.update(self, scrolling, vel_x)
            self.enemies.update(self, scrolling, vel_x)

    def draw(self):
        """Draws all objects in the level, excluding Mario."""
        if self.is_underground:
            for ground in self.terrain.sprites():
                ground.draw()
            for item in self.items.sprites():
                item.draw()
            self.exit_pipe.draw()
        else:
            for ground in self.terrain.sprites():
                ground.draw()
            for enemy in self.enemies.sprites():
                enemy.draw()
            for item in self.items.sprites():
                item.draw()
