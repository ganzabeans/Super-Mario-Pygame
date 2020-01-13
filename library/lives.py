import pygame


class Lives:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 35)
        self.color = (0, 0, 0)
        self.life_header = self.font.render('LIVES', True, self.color)
        self.life_header_rect = self.life_header.get_rect()
        self.life_header_rect.midtop = self.screen.get_rect().topright
        self.life_header_rect.x -= 80
        self.lifes = 3

    def draw(self, undergound):
        if undergound:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)
        self.life_header = self.font.render('LIVES', True, self.color)
        text = self.font.render(str(self.lifes), True, self.color)
        text_rect = text.get_rect()

        # Positions the text bottom center of time_header 
        text_rect.center = self.life_header_rect.center
        text_rect.top = self.life_header_rect.bottom

        self.screen.blit(self.life_header, self.life_header_rect)
        self.screen.blit(text, text_rect)
