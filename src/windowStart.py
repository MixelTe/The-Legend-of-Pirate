import pygame
from window import Window
from functions import load_image


class WindowStart(Window):
    image = load_image("start.png", -1)

    def __init__(self):
        scale = 12
        self.rect = pygame.Rect(500, 500, WindowStart.image.get_width() * scale, WindowStart.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)