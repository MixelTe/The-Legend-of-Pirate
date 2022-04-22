from random import choice
import pygame
from settings import Settings
from window import WindowWithButtons
from functions import createButton, load_image, renderText
from windowGame import WindowGame
from windowStart import WindowStart


img_gameover = pygame.transform.scale(load_image("gameover.png"), (int(Settings.width * 0.7), int(Settings.height * 0.32)))
texts = {
    "crab": ["Краб оказался сильнее", "Теперь крабу одиноко", "КРАБ!", "Краб - лучший друг #####"],
    "cactus": ["Кактусу надоело стоять на месте", "Кактус победил!", "Остерегайтесь кактусов!", "Колючий попался кактус"],
    "cannonball": ["Не стой перед пушкой!", "Ядро не друг, попадёт - убьёт"],
    "aborigineBow": ["Лучник не беззащитен!"],
    "bone": ["Остерегайтесь скелетов!", "Кости могут и ранить", "Костлявый скелет!"],
    "ink": ["Чернила опаснее, чем кажутся", "Оно попало!"],
    "arrow": ["Меткий выстрел!", "Прямо в цель!"],
    "lavaBubble": ["Этот шарик слишком горячий", "Ай, горячо!"],
    "piranha": ["У пираньи острые зубы", "Вот это скорость!"],
    "spear": ["Туземец сильнее, чем кажется"],
    "default": ["Кажется, вы проиграли", "Не сдавайся!", "Всё получится!"],
}


class WindowEnd(WindowWithButtons):
    def __init__(self, save: int, reason: str):
        super().__init__()
        self.save = save
        self.all_sprites = pygame.sprite.Group()

        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.06) + 1)
        text = choice(texts[reason] if reason in texts else texts["default"])
        self.text = renderText(font, int(Settings.width * 0.05) + 1, (Settings.width *
                               0.8, Settings.height * 0.38), text, pygame.Color(255, 187, 50), True, True)
        self.textPos = (Settings.width * 0.1, Settings.height * 0.37)

        self.img_gameoverPos = (Settings.width * 0.15, Settings.height * 0.05)

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
        screen.blit(img_gameover, self.img_gameoverPos)
