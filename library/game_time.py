import pygame


class GameTime:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 35)
        self.color = (0, 0, 0)
        self.time_header = self.font.render('TIME', True, self.color)
        self.time_header_rect = self.time_header.get_rect()
        self.time_header_rect.midtop = self.screen.get_rect().midtop
        self.seconds = 350

    def update(self):
        self.seconds -= 1
        if self.seconds < 0:
            self.seconds = 0

    def draw(self, underground):
        if underground:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)
        self.time_header = self.font.render('TIME', True, self.color)
        text = self.font.render(str(self.seconds), True, self.color)
        text_rect = text.get_rect()

        # Positions the text bottom center of time_header 
        text_rect.center = self.time_header_rect.center
        text_rect.top = self.time_header_rect.bottom

        self.screen.blit(self.time_header, self.time_header_rect)
        self.screen.blit(text, text_rect)
