import pygame
from settings import Settings
from window import WindowWithButtons
from functions import createButton, load_image, renderText


class WindowAbout(WindowWithButtons):
    background = pygame.transform.scale(load_image("background2.png"), (int(Settings.width), int(Settings.height)))

    def __init__(self):
        super().__init__()
        self.back = False
        self.all_sprites = pygame.sprite.Group()

        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.06) + 1)
        # self.text = renderText(font, int(Settings.width * 0.05) + 1, (Settings.width *
        #                        0.8, Settings.height * 0.38), text, pygame.Color(255, 187, 50), True, True)
        self.textPos = (Settings.width * 0.1, Settings.height * 0.37)

        self.img_gameoverPos = (Settings.width * 0.15, Settings.height * 0.05)

        createButton("back", 0.1, self.all_sprites, 0.055, 0.765)

    def action(self):
        if (self.selected == 0):
            self.back = True

    def update(self):
        super().update()
        if (self.back):
            from windowStart import WindowStart
            return WindowStart()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        # screen.blit(self.text, self.textPos)
        # screen.blit(img_gameover, self.img_gameoverPos)
