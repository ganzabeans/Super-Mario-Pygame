from itertools import cycle

import pygame
from pygame.sprite import Group

from library.entities.entity import Entity
from library.entities.player.fireball import Fireball
from library.timer import Timer

iterator = cycle(range(10))


def now():
    return pygame.time.get_ticks()


def play_sound(sound):
    pygame.mixer.Channel(1).stop()
    pygame.mixer.Channel(1).play(sound)


def play_music(music_name, loop=False):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_name)
    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()


def load_bigger_animation():
    animation = []
    small_image = pygame.image.load("resources/images/s_mw1.png").convert_alpha()
    scale = small_image.get_rect().width, small_image.get_rect().height + 5
    medium_image = pygame.transform.scale(small_image, scale).convert_alpha()
    scale = small_image.get_rect().width, small_image.get_rect().height + 10
    big_image = pygame.transform.scale(small_image, scale).convert_alpha()
    bigger_image = pygame.image.load("resources/images/mw1.png").convert_alpha()
    animation.append(medium_image)
    animation.append(big_image)
    animation.append(bigger_image)
    animation.append(big_image)
    animation.append(medium_image)
    animation.append(small_image)
    animation.append(medium_image)
    animation.append(big_image)
    animation.append(bigger_image)
    return Timer(animation, wait=80, loop_once=True)


def load_fire_animation():
    animation = []
    normal_image = pygame.image.load("resources/images/mw1.png").convert_alpha()
    fire_image = pygame.image.load("resources/images/fm1.png").convert_alpha()
    for i in range(4):
        animation.append(fire_image)
        animation.append(normal_image)
    animation.append(fire_image)
    return Timer(animation, wait=80, loop_once=True)


class Mario(Entity):
    """The playable character, Mario."""

    def __init__(self, settings, screen, data, player_score, game_time, lifes):
        super().__init__(settings, screen, (100, 525), data, 1)
        self.settings = settings
        self.velocity.x = -settings.scroll_rate
        self.player_score = player_score
        self.game_time = game_time
        self.lifes = lifes
        self.state = "small"
        self.dead = False

        # Will be initialized later
        self.walk_animation = self.run_animation = None
        self.still_image = self.jump_image = self.hit_image = self.crouch_image = None

        # Animated states
        super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]))
        self.load_state()
        self.bigger_animation = load_bigger_animation()
        self.fire_animation = load_fire_animation()

        # Single-state images
        self.pole_slide_image = pygame.image.load("resources/images/m_pole.png").convert_alpha()
        self.fire_pole_slide_image = pygame.image.load("resources/images/m_fpole.png").convert_alpha()
        self.throw_image = pygame.image.load("resources/images/m_throw.png").convert_alpha()
        self.death_image = pygame.image.load("resources/images/sm_hit.png")

        # Movement variables
        self.moving_left = self.moving_right = self.is_scrolling = False
        self.is_jumping = self.is_d_jumping = False

        self.fireballs = Group()

        self.throw_time = 0
        self.animation_time = 0
        self.invincible_time = 0

        # True if animating going through pipe
        self.pipe_down = False
        self.pipe_up = False
        self.pipe_side = False

        # Sounds
        self.jump_sound = pygame.mixer.Sound("resources/sounds/jump.wav")
        self.coin_sound = pygame.mixer.Sound("resources/sounds/coin.wav")
        self.enemy_kill_sound = pygame.mixer.Sound("resources/sounds/enemy_killed.wav")
        self.fireball_sound = pygame.mixer.Sound("resources/sounds/fireball.wav")
        self.powerup_sound = pygame.mixer.Sound("resources/sounds/powerup.wav")
        self.brick_break_sound = pygame.mixer.Sound("resources/sounds/brick_break.wav")
        self.pipe_sound = pygame.mixer.Sound("resources/sounds/pipe.wav")
        self.death_sound = pygame.mixer.Sound("resources/sounds/mario_dies.wav")
        self.switch_bg_music = False
        self.level_2 = False

        # States
        self.invincible = False
        self.pipe_entrance = False
        self.pipe_exit = False
        self.underground = False
        self.running = False
        self.crouching = False
        self.animating = False

        # End-game variable
        self.castle_entrance_x = 778

        # Music
        self.bg_music_1 = "resources/sounds/background.mp3"
        self.bg_music_2 = "resources/sounds/underground.mp3"
        self.star_music = "resources/sounds/star_power.mp3"
        self.dead_music = "resources/sounds/mario_dies.wav"
        self.end_music = "resources/sounds/level_cleared.wav"
        play_music(self.bg_music_1, True)

    def load_state(self):
        """State animations and images."""
        super().init_mario_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
        self.load_state_images()
        self.walk_animation = self.load_walk_animation(100)
        self.run_animation = self.load_walk_animation(50)

    def load_state_images(self):
        self.still_image = self.image
        self.jump_image = pygame.image.load(self.data[self.state]["jump"]).convert_alpha()
        self.hit_image = pygame.image.load(self.data[self.state]["hit"]).convert_alpha()
        self.crouch_image = pygame.image.load(self.data[self.state]["crouch"]).convert_alpha()

    def load_walk_animation(self, animation_speed):
        animation = []
        for x in range(self.data[self.state]["walking"]["sequence_sz"]):
            animation.append(pygame.image.load(self.data[self.state]["walking"]["sequence"][x]).convert_alpha())
        return Timer(animation, wait=animation_speed)

    def throw_fireball(self):
        fireball = Fireball(self.settings, self.screen, self.rect.center, self.direction)
        play_sound(self.fireball_sound)
        self.fireballs.add(fireball)
        self.throw_time = now()

    def jump(self):
        """Increases Mario's y-position. Must land before performing another jump."""
        if self.is_jumping:
            if not self.is_d_jumping:
                self.velocity.y = -15  # Weaker double jump
                self.is_d_jumping = True
                play_sound(self.jump_sound)
        else:
            self.velocity.y = -20  # Regular jump
            self.is_jumping = True
            play_sound(self.jump_sound)

    def reset_jump(self):
        """Allows Mario to perform jumps."""
        self.is_jumping = False
        self.is_d_jumping = False
        self.velocity.y = 0

    def handle_horizontal_collision(self, level):
        """Called after updating x-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        for collision in collisions:
            if collision.is_castle:
                continue
            if self.moving_right:
                self.is_scrolling = False
                self.rect.right = collision.rect.left
            elif self.moving_left:
                self.rect.left = collision.rect.right
        # Check for pipe if underground
        if self.underground:
            if pygame.sprite.collide_rect(self, level.exit_pipe):
                self.check_pipe_exit(level)

    def handle_vertical_collision(self, level):
        """Called after updating y-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            for collision in collisions:
                # Mario is jumping
                if self.velocity.y < 0:
                    self.rect.top = collision.rect.bottom
                    self.velocity.y = 0
                    self.fall()
                    # Check for block collisions
                    try:
                        if collision.has_item != 0:
                            collision.show_item(self)
                        elif (collision.has_item == 0 and self.state != "small"
                                and collision.type == "brick" and not collision.dead):
                            # Break block
                            play_sound(self.brick_break_sound)
                            collision.destroy()
                    except AttributeError:
                        pass
                    break
                # Mario is falling
                elif self.velocity.y > 0:
                    # Check if pipe is an entrance
                    try:
                        if collision.enter:
                            self.pipe_entrance = True
                    except AttributeError:
                        self.pipe_entrance = False
                    self.rect.bottom = collision.rect.top
                    self.reset_jump()

        # No vertical collisions, apply gravity
        else:
            self.fall()

    def update_fireballs(self, level, vel_x=None):
        for fireball in self.fireballs:
            # Skip fireballs that have already collided
            if not fireball.hit:
                collisions = pygame.sprite.spritecollide(fireball, level.enemies, False)
                for collision in collisions:
                    # Skip enemies that are already dead (playing death animation)
                    if not collision.hit:
                        self.player_score.enemy_hit()
                        play_sound(self.enemy_kill_sound)
                        collision.hit_sequence()
                        fireball.hit_sequence()
            # Moves fireball position
            fireball.update(level, self.is_scrolling, vel_x)

    def check_pipe(self):
        """Checks if it is an underground pipe."""
        if self.pipe_entrance:
            play_sound(self.pipe_sound)
            self.moving_left = False
            self.moving_right = False
            self.pipe_down = True
            self.crouching = False
            self.pipe_entrance = False

    def check_pipe_exit(self, level):
        """Checks if it is an underground pipe."""
        if pygame.sprite.collide_rect(self, level.exit_pipe):
            play_sound(self.pipe_sound)
            self.moving_left = False
            self.moving_right = False
            self.pipe_side = True
            self.pipe_exit = False

    def update(self, level, scrolling=None, vel_x=None):
        # Time ran out
        if self.game_time.seconds <= 0 and not self.dead:
            self.died()
            play_music(self.dead_music)
        # Actually moves Mario horizontally, if on left side of screen.
        # Otherwise, scroll screen to simulate movement
        if self.dead:
            # Waited for death music/animation to finish playing
            if now() - self.death_time >= 2500:
                self.dead = False
                self.game_time.seconds = 350

                # No more lives available, restart at level 1
                # print(self.rect.topleft)
                if self.lifes.lifes == 0:
                    self.state = "small"
                    self.player_score.score = 0
                    self.lifes.lifes = 3
                    self.level_2 = False
                    level.load("resources/w1_1.json", True)
                # Resume gameplay at current level
                elif self.level_2:
                    level.load("resources/w1_2.json")
                else:
                    level.load("resources/w1_1.json")
                # Respawn location
                self.position = (50, 350)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]))
                play_music(self.bg_music_2 if self.level_2 else self.bg_music_1, True)
        # Fell out of screen
        elif self.rect.y > self.settings.screen_height and not self.dead:
            play_music(self.dead_music)
            self.switch_bg_music = False
            self.died(False)

        # Falling death movement
        if self.dead:
            self.fall()
            self.rect.y += self.velocity.y
            return

        # Fireball movement
        if self.running:
            self.update_fireballs(level, -self.velocity.x)
        else:
            self.update_fireballs(level)

        # Freeze Mario on taking damage
        if self.hit:
            self.moving_left = False
            self.moving_right = False
            self.is_scrolling = False
        # Going down pipe animation
        elif self.pipe_down:
            self.rect.y += 2
            if self.rect.y >= 500:
                self.underground = True
                self.pipe_down = False
                # reposition
                self.position = (100, -300)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]))
                level.create_underground()
        # Going into pipe from side animation
        elif self.pipe_side:
            self.rect.x += 2
            if self.rect.x >= 900:
                self.pipe_side = False
                self.pipe_up = True
                self.underground = False
                self.position = (25, level.go_surface() + 80)
                play_sound(self.pipe_sound)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]))
        # Coming out of pipe animation
        elif self.pipe_up:
            self.rect.y -= 2
            if self.rect.bottom <= 505:
                self.pipe_up = False
        else:
            # Running increases scroll speed
            if self.running:
                self.velocity.x = -self.settings.scroll_rate * 2
            # Resets speed if not running
            else:
                self.velocity.x = -self.settings.scroll_rate
            # Disables scrolling underground
            if self.underground:
                if self.moving_right:
                    self.rect.centerx += self.velocity.x
                    self.direction = 1
                elif self.moving_left:
                    self.direction = -1
                    self.rect.x -= self.velocity.x
            # End of level
            elif self.settings.level_over:
                self.castle_walk(level)
                return
            # Regular movement
            elif self.moving_right:
                self.direction = 1
                if self.rect.centerx + self.velocity.x <= self.screen_rect.centerx:
                    self.rect.centerx += self.velocity.x
                else:
                    self.is_scrolling = True
            elif self.moving_left:
                self.direction = -1
                if self.rect.x - self.velocity.x >= 0:
                    self.rect.x -= self.velocity.x
                else:
                    self.moving_left = False
                    self.is_scrolling = False
            self.handle_horizontal_collision(level)
            # Jumping, moves Mario vertically
            self.rect.y += self.velocity.y
            self.handle_vertical_collision(level)

            # Entity collisions
            self.check_enemy_collisions(level)
            self.check_item_collisions(level)

    def check_enemy_collisions(self, level):
        if self.dead:
            return
        collisions = pygame.sprite.spritecollide(self, level.enemies, False)
        for collision in collisions:
            if not collision.hit:
                # Jumping on enemy
                if self.invincible or (self.rect.bottom <= collision.rect.centery):
                    play_sound(self.enemy_kill_sound)
                    collision.hit_sequence()
                    self.player_score.enemy_hit()
                    if not self.invincible:
                        self.rect.bottom = collision.rect.top
                        self.is_jumping = True  # Prevent jumping after bounce
                        self.is_d_jumping = True
                        self.velocity.y = -10  # Small bounce when jumping on enemies
                else:
                    # Touched enemy, Mario takes damage
                    if not self.hit and not self.invincible:
                        if self.state is "small":
                            play_music(self.dead_music)
                            self.died()
                        else:
                            play_sound(self.pipe_sound)
                            self.hit_sequence()
                            self.go_down_state()

    def check_item_collisions(self, level):
        """Detect if touched an item."""
        collisions = pygame.sprite.spritecollide(self, level.items, True)
        for collision in collisions:
            if collision.item_type == 1:
                play_sound(self.coin_sound)
                self.player_score.coin_hit(self)
            if collision.item_type == 2:
                play_sound(self.powerup_sound)
                self.get_bigger()
            if collision.item_type == 3:
                play_sound(self.powerup_sound)
                self.get_fire()
            if collision.item_type == 4:
                play_sound(self.powerup_sound)
                self.get_star()

    def get_bigger(self):
        self.player_score.power_up_hit()
        if not self.state == "big":
            self.state = "big"
            self.load_state()
            self.animation_time = now()
            self.bigger_animation.reset()
            self.animating = True

    def get_fire(self):
        self.player_score.power_up_hit()
        if not self.state == "fire":
            self.state = "fire"
            self.load_state()
            self.animation_time = now()
            self.fire_animation.reset()
            self.animating = True

    def get_star(self):
        self.player_score.power_up_hit()
        play_music(self.star_music, True)
        self.invincible = True
        self.invincible_time = now()

    def go_down_state(self):
        if self.state == "big":
            self.state = "small"
            self.bigger_animation.reset()
        elif self.state == "fire":
            self.fire_animation.reset()
            self.state = "big"
        self.load_state()
        self.animation_time = now()

    def prep_castle_walk(self):
        self.settings.level_over = True
        self.moving_right = False
        self.is_scrolling = False
        self.switch_bg_music = True

    def castle_walk(self, level):
        # Cleared level music
        if self.switch_bg_music:
            self.player_score.score += self.game_time.seconds * 2
            play_music(self.end_music)
            self.switch_bg_music = False
        # Sliding down pole
        if not self.moving_right:
            if self.rect.bottom <= 598:
                self.rect.bottom += 3
                self.player_score.score += 5
            else:
                self.moving_right = True
                super().init_mario_image(
                    pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
        else:
            # Walking towards castle
            if self.rect.x < self.castle_entrance_x + 120:
                self.rect.x += 2
            # Fall into level 2
            else:
                self.moving_right = False
                self.running = False
                self.settings.level_over = False
                level.load("resources/w1_2.json", True)
                self.switch_bg_music = False
                self.level_2 = True
                play_music(self.bg_music_2 if self.level_2 else self.bg_music_1, True)
                self.game_time.seconds = 350
                self.position = (100, -300)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]))

    def draw(self):
        # Fireballs
        for fireball in self.fireballs.sprites():
            fireball.draw()

        # Sliding image
        if self.settings.level_over:
            if self.moving_right:
                super().set_image(self.walk_animation.get_image())
            else:
                if self.state == "fire":
                    super().set_image(self.fire_pole_slide_image)
                else:
                    super().set_image(self.pole_slide_image)
        elif self.dead:
            super().set_image(self.death_image)

        elif self.hit:
            # Big to small Mario
            if self.state == "small" and now() - self.animation_time <= 800:
                super().init_mario_image(self.bigger_animation.get_image(True))
                super().set_image(self.image)
            # Fire to big Mario
            elif self.state == "big" and now() - self.animation_time <= 640:
                super().init_mario_image(self.fire_animation.get_image(True))
                super().set_image(self.image)
            else:
                # Fixing image offsets
                super().init_mario_image(
                    pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
                self.hit = False
        elif self.animating:
            self.moving_left = False
            self.moving_right = False
            self.is_scrolling = False
            # Bigger Mario animation
            if self.state == "big" and now() - self.animation_time <= 800:
                super().init_mario_image(self.bigger_animation.get_image())
                super().set_image(self.image)
            # Fire Mario animation
            elif self.state == "fire" and now() - self.animation_time <= 640:
                super().init_mario_image(self.fire_animation.get_image())
                super().set_image(self.image)
            else:
                self.animating = False
        else:
            # Throw animation
            if now() - self.throw_time < 250:
                super().set_image(self.throw_image)
            elif self.crouching:
                super().set_image(self.crouch_image)
            else:
                if self.moving_right or self.moving_left:
                    if self.is_jumping:
                        super().set_image(self.jump_image)
                    elif self.running:
                        super().set_image(self.run_animation.get_image())
                    else:
                        super().set_image(self.walk_animation.get_image())
                # Standing still
                else:
                    if self.is_jumping:
                        super().set_image(self.jump_image)
                    else:
                        super().set_image(self.still_image)

        # Brighten image
        if self.invincible:
            if now() - self.invincible_time <= 8000:
                if next(iterator) < 5:
                    brightness = 100
                    brighter_image = self.image.copy().convert_alpha()
                    brighter_image.fill((brightness, brightness, brightness), special_flags=pygame.BLEND_RGB_ADD)
                    self.screen.blit(brighter_image, self.rect)
                    return
            else:
                self.invincible = False
                play_music(self.bg_music_2 if self.level_2 else self.bg_music_1, True)
        # Parent draw() actually blits the image
        super().draw()

    def died(self, jump=True):
        """Sets Mario to death state to draw death animation."""
        self.state = "small"
        self.moving_left = False
        self.moving_right = False
        self.is_scrolling = False
        self.dead = True
        self.lifes.lifes -= 1
        self.death_time = now()
        if jump:
            self.jump()
