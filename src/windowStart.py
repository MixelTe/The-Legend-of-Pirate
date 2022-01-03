import pygame
from window import Window
from functions import load_image
from WindowStatistics import WindowStatistics


class WindowStart(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        scale = 16

        self.start = pygame.sprite.Sprite(self.all_sprites)
        self.start.rect = pygame.Rect(750, 200, WindowStart.image_start.get_width() * scale, WindowStart.image_start.get_height() * scale)
        self.start.image = pygame.transform.scale(self.image_start, (self.start.rect.width, self.start.rect.height))

        self.quit = pygame.sprite.Sprite(self.all_sprites)
        self.quit.rect = pygame.Rect(750, 400, WindowStart.image_quit.get_width() * scale, WindowStart.image_quit.get_height() * scale)
        self.quit.image = pygame.transform.scale(self.image_quit, (self.quit.rect.width, self.quit.rect.height))

        self.stat = False
        
    def draw(self, screen: pygame.Surface):
        self.all_sprites.draw(screen)
    
    def on_event(self, event: pygame.event.Event):       
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit.rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if self.start.rect.collidepoint(event.pos):
                self.stat = True
    
    def calc(self):
        if self.stat:
            return WindowStatistics()

