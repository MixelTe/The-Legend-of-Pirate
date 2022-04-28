import pygame
from settings import Settings
from window import WindowWithButtons
from functions import Button, createButton, load_image, renderText
import webbrowser


class WindowAbout(WindowWithButtons):
    background = pygame.transform.scale(load_image("background2.png"), (int(Settings.width), int(Settings.height)))

    def __init__(self):
        super().__init__()
        self.back = False
        self.all_sprites = pygame.sprite.Group()
        # self.text_title = renderText(font_title, int(Settings.width * 0.05) + 1, (Settings.width * 0.8, Settings.height * 0.38), "The Legend of Pirate", "#733E39", True, True)

        font_title = pygame.font.Font(Settings.path_font, int(Settings.width * 0.05) + 1)
        self.text_title = font_title.render("The Legend of Pirate", True, "#733E39")
        self.textPos_title = ((Settings.width - self.text_title.get_width()) // 2, int(Settings.height * 0.09))

        font_text = pygame.font.Font(Settings.path_font, int(Settings.width * 0.04) + 1)
        self.text_authors = renderText(font_text, int(Settings.width * 0.04) + 1, (Settings.width * 0.86, Settings.height * 0.7),
                                       """Авторы:
                                        Программист и звукорежиссёр - 
                                        Геймдизайнер и художник -

                                        Спасибо за участие в тестировании игры:
                                        Михаил Б, Пётр К

                                        Исходный код:
                                        """, "#733E39")
        self.textPos_authors = (int(Settings.width * 0.075), int(Settings.height * 0.17))

        createButton("back", 0.1, self.all_sprites, 0.055, 0.765)
        createLink("Mixel Te", font_text, self.all_sprites, 0.7, 0.24)
        createLink("Липатов Андрей", font_text, self.all_sprites, 0.617, 0.314)
        createLink("Github", font_text, self.all_sprites, 0.366, 0.67)

    def action(self):
        if (self.selected == 0):
            self.back = True
        elif (self.selected == 1):
            webbrowser.open("https://github.com/MixelTe")
        elif (self.selected == 2):
            webbrowser.open("https://github.com/AndreyLipato")
        elif (self.selected == 3):
            webbrowser.open("https://github.com/MixelTe/The-Legend-of-Pirate")

    def update(self):
        super().update()
        if (self.back):
            from windowStart import WindowStart
            return WindowStart()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text_title, self.textPos_title)
        screen.blit(self.text_authors, self.textPos_authors)
        self.all_sprites.draw(screen)


def createLink(text: str, font: pygame.font.Font, group: pygame.sprite.Group, x: float, y: float):
    rendered = font.render(text, True, "#0969da")
    rendered_a = font.render(text, True, "#0993dA")
    w, h = rendered.get_width(), rendered.get_height()
    pygame.draw.line(rendered_a, "#0993dA", (0, h - Settings.height * 0.005),
                     (w, h - Settings.height * 0.005), int(Settings.height * 0.005) + 1)
    link = Button(group, rendered, rendered_a)
    link.rect = pygame.Rect(x * Settings.width, y * Settings.height, w, h)
    return link
