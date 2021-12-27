import pygame
from window import Window
from functions import load_image


class WindowStart(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        self.quit_size = []

        scale = 12
        self.rect_start = pygame.Rect(750, 200, WindowStart.image_start.get_width() * scale, WindowStart.image_start.get_height() * scale)
        self.image_start = pygame.transform.scale(self.image_start, (self.rect_start.width, self.rect_start.height))
        
        self.rect_quit = pygame.Rect(750, 400, WindowStart.image_quit.get_width() * scale, WindowStart.image_quit.get_height() * scale)
        self.image_quit = pygame.transform.scale(self.image_quit, (self.rect_quit.width, self.rect_quit.height))
        
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_start, self.rect_start)
        screen.blit(self.image_quit, self.rect_quit)
    
    def on_event(self, event: pygame.event.Event):       
         if event.type == pygame.MOUSEBUTTONDOWN:
            self.quit_game(event.pos)

    def quit_game(self, pos):
        if self.rect_quit.collidepoint(pos):
            pygame.event.post(pygame.event.Event(pygame.QUIT))