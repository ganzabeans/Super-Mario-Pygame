import pygame


class ScoreSystem:
    """Keeps track of the points Mario has accumulated."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 35)
        self.color = (0, 0, 0)
        self.score_header = self.font.render('SCORE', True, self.color)
        self.score_header_rect = self.score_header.get_rect()
        self.score_header_rect.x = 50
        self.lives = 3
        self.coin_counter = 0

        # Point values
        self.enemy_points = 100
        self.coin_points = 200
        self.power_up_points = 1000

        # Player score
        self.score = 0

    def enemy_hit(self):
        self.score += self.enemy_points

    def coin_hit(self, mario):
        self.score += self.coin_points
        self.coin_counter += 1
        if self.coin_counter == 10:
            mario.lifes.lifes += 1
            self.coin_counter = 0

    def power_up_hit(self):
        self.score += self.power_up_points

    def draw(self, underground):
        if underground:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)
        self.score_header = self.font.render('SCORE', True, self.color)
        text = self.font.render(str(self.score), True, self.color)
        text_rect = text.get_rect()

        # Positions the text bottom center of score_header
        text_rect.center = self.score_header_rect.center
        text_rect.top = self.score_header_rect.bottom

        # Score
        self.screen.blit(self.score_header, self.score_header_rect)
        self.screen.blit(text, text_rect)
