import pygame
from window import Window
from functions import load_image


class WindowStatistics(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        scale = 12
        
        self.rect_save1 = pygame.Rect(750, 200, WindowStatistics.image_quit.get_width() * scale, WindowStatistics.image_quit.get_height() * scale)
        self.image_save1 = pygame.transform.scale(self.image_quit, (self.rect_save1.width, self.rect_save1.height))

        self.rect_save2 = pygame.Rect(750, 400, WindowStatistics.image_quit.get_width() * scale, WindowStatistics.image_quit.get_height() * scale)
        self.image_save2 = pygame.transform.scale(self.image_quit, (self.rect_save2.width, self.rect_save2.height))

        self.rect_save3 = pygame.Rect(750, 600, WindowStatistics.image_quit.get_width() * scale, WindowStatistics.image_quit.get_height() * scale)
        self.image_save3 = pygame.transform.scale(self.image_quit, (self.rect_save3.width, self.rect_save3.height))
        
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_save1, self.rect_save1)
        screen.blit(self.image_save2, self.rect_save2)
        screen.blit(self.image_save3, self.rect_save3)
    
    def on_event(self, event: pygame.event.Event):       
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass