# Corner Crew
# Super Mario

import pygame

import library.game_methods as game_methods
from library.entities.player.mario import Mario
from library.game_time import GameTime
from library.level import Level
from library.lives import Lives
from library.score_system import ScoreSystem
from library.settings import Settings


def run_game():
    """ Main function of Super Mario."""

    # Sound initialization
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("Super Mario")
    settings = Settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    # Time factors
    second = pygame.USEREVENT
    pygame.time.set_timer(second, 1000)
    game_time = GameTime(screen)

    # Player objects
    player_score = ScoreSystem(screen)
    lives = Lives(screen)
    mario = Mario(settings, screen, "resources/mario.json", player_score, game_time, lives)

    # World 1-1
    level = Level(settings, screen, "resources/w1_1.json", mario)

    # Game loop
    while True:
        game_methods.on_event(mario, level, second, game_time, settings)
        game_methods.on_update(level, mario)
        game_methods.on_draw(level, mario, game_time, player_score)
        pygame.display.flip()
        clock.tick(60)


run_game()
