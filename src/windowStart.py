import pygame
from backMusic import setBackMusic
from settings import Settings
from window import WindowWithButtons
from functions import createButton, joinPath
from windowAbout import WindowAbout
from windowSaveSelection import WindowSaveSelection


class WindowStart(WindowWithButtons):
    def __init__(self):
        super().__init__()
        scale = 0.3

        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.1))
        self.titleText_1 = font.render("The Legend", True, "#FFBD4C")
        self.titleTextPos_1 = ((Settings.width - self.titleText_1.get_width()) // 2, int(Settings.height * 0))
        self.titleText_2 = font.render("of Pirate", True, "#FFBD4C")
        self.titleTextPos_2 = ((Settings.width - self.titleText_2.get_width()) // 2, int(Settings.height * 0.13))

        offset = 0.3
        createButton("start", scale, self.all_sprites, (1 - scale) / 2, (1 - offset) / 3 * 0 + offset)
        createButton("about", scale, self.all_sprites, (1 - scale) / 2, (1 - offset) / 3 * 1 + offset)
        createButton("quit", scale, self.all_sprites, (1 - scale) / 2, (1 - offset) / 3 * 2 + offset)
        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.04))
        self.startText = font.render(Settings.version, True, pygame.Color(81, 44, 40))
        self.startTextPos = (int(Settings.width * 0.01), int(Settings.height * 0.93))
        setBackMusic(joinPath(Settings.folder_data, Settings.folder_sounds, "back", "SandWorld.mp3"))

        self.starting = False
        self.about = False

    def action(self):
        if (self.selected == 0):
            self.starting = True
        elif (self.selected == 1):
            self.about = True
        elif (self.selected == 2):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        super().update()
        if self.starting:
            return WindowSaveSelection()
        if (self.about):
            return WindowAbout()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        screen.blit(self.startText, self.startTextPos)
        screen.blit(self.titleText_1, self.titleTextPos_1)
        screen.blit(self.titleText_2, self.titleTextPos_2)
