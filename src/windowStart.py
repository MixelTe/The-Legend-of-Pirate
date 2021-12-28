import pygame
from window import Window
from functions import load_image
from WindowStatistics import WindowStatistics


class WindowStart(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        scale = 12
        self.rect_start = pygame.Rect(750, 200, WindowStart.image_start.get_width() * scale, WindowStart.image_start.get_height() * scale)
        self.image_start = pygame.transform.scale(self.image_start, (self.rect_start.width, self.rect_start.height))
        
        self.rect_quit = pygame.Rect(750, 400, WindowStart.image_quit.get_width() * scale, WindowStart.image_quit.get_height() * scale)
        self.image_quit = pygame.transform.scale(self.image_quit, (self.rect_quit.width, self.rect_quit.height))

        self.stat = False
        
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_start, self.rect_start)
        screen.blit(self.image_quit, self.rect_quit)
    
    def on_event(self, event: pygame.event.Event):       
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_quit.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if self.rect_start.collidepoint(event.pos):
                self.stat = True
    
    def calc(self):
        if self.stat:
            return WindowStatistics()

