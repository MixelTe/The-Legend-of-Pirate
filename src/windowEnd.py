import pygame
from settings import Settings
from window import WindowWithButtons
from functions import createButton
from windowGame import WindowGame
from windowStart import WindowStart


class WindowEnd(WindowWithButtons):
    def __init__(self, save: int, reason: str):
        super().__init__()
        self.save = save
        self.all_sprites = pygame.sprite.Group()


        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.06) + 1)
        self.text = font.render("Причина: " + reason, True, pygame.Color(81, 44, 40))
        self.textPos = (Settings.width * 0.2, Settings.height * 0.6)

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

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        screen.blit(self.text, self.textPos)
