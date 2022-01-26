import pygame
from settings import Settings
from window import WindowWithButtons
from functions import createButton
from windowSaveSelection import WindowSaveSelection


class WindowStart(WindowWithButtons):
    def __init__(self):
        super().__init__()
        scale = 0.4

        createButton("start", scale, self.all_sprites, 0.3, 0.15)
        createButton("quit", scale, self.all_sprites, 0.3, 0.55)
        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.04))
        self.startText = font.render(Settings.version, True, pygame.Color(81, 44, 40))
        self.startTextPos = (int(Settings.width * 0.01), int(Settings.height * 0.93))

        self.starting = False

    def action(self):
        if (self.selected == 0):
            self.starting = True
        elif (self.selected == 1):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        super().update()
        if self.starting:
            return WindowSaveSelection()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        screen.blit(self.startText, self.startTextPos)
