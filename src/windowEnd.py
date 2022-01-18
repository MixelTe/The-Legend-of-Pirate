import pygame
from window import WindowWithButtons
from functions import createButton
from windowGame import WindowGame
from windowStart import WindowStart


class WindowEnd(WindowWithButtons):
    def __init__(self, save: int):
        super().__init__()
        self.save = save
        self.all_sprites = pygame.sprite.Group()

        createButton("restart", 0.4, self.all_sprites, 0.1, 0.75)
        createButton("quit", 0.4 / 31 * 23, self.all_sprites, 0.6, 0.75)

        self.restart = False
        self.quit = False

    def action(self):
        if (self.selected == 0):
            self.restart = True
        if (self.selected == 1):
            self.quit = True

    def update(self):
        super().update()
        if (self.restart):
            return WindowGame(self.save)
        if (self.quit):
            return WindowStart()
