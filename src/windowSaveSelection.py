import pygame
from window import Window
from functions import createSprite, load_image


class WindowSaveSelection(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        scale = 16

        self.save1 = createSprite(WindowSaveSelection.image_start, scale, self.all_sprites, 750, 200)
        self.save2 = createSprite(WindowSaveSelection.image_start, scale, self.all_sprites, 750, 450)
        self.save3 = createSprite(WindowSaveSelection.image_start, scale, self.all_sprites, 750, 700)

    def draw(self, screen: pygame.Surface):
        self.all_sprites.draw(screen)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
