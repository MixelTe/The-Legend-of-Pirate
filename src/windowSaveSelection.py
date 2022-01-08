import pygame
from window import Window
from functions import createSprite, load_image
from windowGame import WindowGame


class WindowSaveSelection(Window):
    img_save1 = load_image("save1.png")
    img_save2 = load_image("save2.png")
    img_save3 = load_image("save3.png")

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        scale = 0.4

        self.save1 = createSprite(WindowSaveSelection.img_save1, scale, self.all_sprites, 0.3, 0.05)
        self.save2 = createSprite(WindowSaveSelection.img_save2, scale, self.all_sprites, 0.3, 0.37)
        self.save3 = createSprite(WindowSaveSelection.img_save3, scale, self.all_sprites, 0.3, 0.7)

        self.startSave = None

    def draw(self, screen: pygame.Surface):
        self.all_sprites.draw(screen)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.save1.rect.collidepoint(event.pos):
                self.startSave = 1
            if self.save2.rect.collidepoint(event.pos):
                self.startSave = 2
            if self.save3.rect.collidepoint(event.pos):
                self.startSave = 3

    def update(self):
        if (self.startSave is not None):
            return WindowGame(self.startSave)
