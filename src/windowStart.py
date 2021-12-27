import pygame
from window import Window
from functions import load_image


class WindowStart(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        self.quit_size = []
        self.all_sprites = pygame.sprite.Group()

        scale = 12
        self.start = pygame.sprite.Sprite(self.all_sprites)
        self.start.rect = pygame.Rect(750, 200, WindowStart.image_start.get_width() * scale, WindowStart.image_start.get_height() * scale)
        self.start.image = pygame.transform.scale(self.image_start, (self.start.rect.width, self.start.rect.height))

        self.quit = pygame.sprite.Sprite(self.all_sprites)
        self.quit.rect = pygame.Rect(750, 400, WindowStart.image_quit.get_width() * scale, WindowStart.image_quit.get_height() * scale)
        self.quit.image = pygame.transform.scale(self.image_quit, (self.quit.rect.width, self.quit.rect.height))

    def draw(self, screen: pygame.Surface):
        self.all_sprites.draw(screen)

    def on_event(self, event: pygame.event.Event):
         if event.type == pygame.MOUSEBUTTONDOWN:
            self.quit_game(event.pos)

    def quit_game(self, pos):
        if self.quit.rect.collidepoint(pos):
            pygame.event.post(pygame.event.Event(pygame.QUIT))