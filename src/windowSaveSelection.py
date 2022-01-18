import pygame
from window import WindowWithButtons
from functions import createButton
from windowGame import WindowGame


class WindowSaveSelection(WindowWithButtons):
    def __init__(self):
        super().__init__()
        self.all_sprites = pygame.sprite.Group()
        scale = 0.4

        createButton("save1", scale, self.all_sprites, 0.3, 0.05)
        createButton("save2", scale, self.all_sprites, 0.3, 0.37)
        createButton("save3", scale, self.all_sprites, 0.3, 0.7)

        self.startSave = None

    def action(self):
        if (self.selected >= 0):
            self.startSave = self.selected + 1

    def update(self):
        super().update()
        if (self.startSave is not None):
            return WindowGame(self.startSave)
