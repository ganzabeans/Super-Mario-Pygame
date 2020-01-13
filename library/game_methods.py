import sys

import pygame
from pygame.locals import *


def on_event(mario, level, second, game_time, settings):
    """Handles Pygame events."""
    for event in pygame.event.get():
        if not mario.settings.level_over:
            if event.type == second:
                game_time.update()
            if event.type == KEYDOWN:
                on_key_down(event, mario, level, settings)
            elif event.type == KEYUP:
                on_key_up(event, mario)
        if event.type == QUIT:
            sys.exit()


def on_key_down(event, mario, level, settings):
    """Handles key presses."""
    if not mario.animating and not mario.hit and not settings.level_over and not mario.dead:
        if mario.pipe_down or mario.pipe_up or mario.pipe_side:
            return
        if event.key == K_RIGHT and not mario.crouching:
            mario.moving_right = True
            mario.moving_left = False
            if mario.underground:
                mario.check_pipe_exit(level)
        elif event.key == K_LEFT and not mario.crouching:
            mario.moving_left = True
            mario.moving_right = False
        elif event.key == K_DOWN:
            if not mario.pipe_down:
                mario.crouching = True
            mario.moving_left = False
            mario.moving_right = False
            mario.running = False
            mario.is_scrolling = False
            mario.check_pipe()
        elif event.key == K_s:
            if mario.moving_left or mario.moving_right:
                mario.running = True
        elif event.key == K_SPACE:
            if mario.state == "fire":
                mario.throw_fireball()
        elif event.key == K_UP:
            mario.jump()


def on_key_up(event, mario):
    """Handles key releases."""
    if event.key == K_RIGHT:
        mario.moving_right = False
        mario.is_scrolling = False
    if event.key == K_LEFT:
        mario.moving_left = False
        mario.is_scrolling = False
    if event.key == K_DOWN:
        mario.crouching = False
    if event.key == K_s:
        mario.running = False


def on_update(level, mario):
    """Handles positions and logic."""
    mario.update(level)
    # Freeze updates while Mario has death animation/is respawning
    if not mario.dead:
        level.update(mario, mario.is_scrolling)
        if mario.running:
            level.update(mario, mario.is_scrolling, -mario.velocity.x)
        else:
            level.update(mario, mario.is_scrolling)


def on_draw(level, mario, game_time, player_score):
    """Displays all objects to screen."""
    level.background.draw()
    # Draw Mario in front of flag pole and castle
    if mario.settings.level_over or mario.dead:
        level.draw()
        mario.draw()
        if not mario.level_2:
            level.castle_layer.draw()
    # Draw Mario behind pipes during animations
    else:
        mario.draw()
        level.draw()
    if mario.level_2:
        mario.lifes.draw(True)
        game_time.draw(True)
        player_score.draw(True)
        return
    mario.lifes.draw(mario.underground)
    game_time.draw(mario.underground)
    player_score.draw(mario.underground)
