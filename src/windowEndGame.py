import pygame
from game.saveData import SaveData
from settings import Settings
from window import WindowWithButtons
from functions import createButton, getGameProgress, load_image, renderText, wordWithNum


class WindowEndGame(WindowWithButtons):
    background = pygame.transform.scale(load_image("background2.png"), (int(Settings.width), int(Settings.height)))

    def __init__(self, saveData: SaveData):
        super().__init__()
        self.back = False
        self.restart = False
        self.all_sprites = pygame.sprite.Group()
        self.saveData = saveData
        # self.text_title = renderText(font_title, int(Settings.width * 0.05) + 1, (Settings.width * 0.8, Settings.height * 0.38), "The Legend of Pirate", "#733E39", True, True)

        font_title = pygame.font.Font(Settings.path_font, int(Settings.width * 0.06) + 1)
        self.text_title = font_title.render("The Legend of Pirate", True, "#733E39")
        self.textPos_title = ((Settings.width - self.text_title.get_width()) // 2, int(Settings.height * 0.09))

        progress = getGameProgress(saveData.tags)
        time = secondsToTime(saveData.time)
        text = "Спасибо за прохождение игры!" + "\n\n"
        text += f"Вы прошли игру на {progress}% за {time}" + "\n"
        if (progress == 100):
            text += "Поздравляем! Вы преодалели все испытания" + "\n"
        else:
            text += "Что-то интересное ещё осталось на острове!" + "\n"

        font_text = pygame.font.Font(Settings.path_font, int(Settings.width * 0.05) + 1)
        self.text_authors = renderText(font_text, int(Settings.width * 0.044) + 1,
                                       (Settings.width * 0.86, Settings.height * 0.7), text, "#733E39")
        self.textPos_authors = (int(Settings.width * 0.075), int(Settings.height * 0.19))

        createButton("back", 0.1, self.all_sprites, 0.055, 0.765)
        createButton("continue", 0.53, self.all_sprites, 0.415, 0.765)

    def action(self):
        if (self.selected == 0):
            self.back = True
        elif (self.selected == 1):
            self.restart = True

    def update(self):
        super().update()
        if (self.back):
            from windowStart import WindowStart
            return WindowStart()
        if (self.restart):
            from windowGame import WindowGame
            return WindowGame(self.saveData.saveFile)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text_title, self.textPos_title)
        screen.blit(self.text_authors, self.textPos_authors)
        self.all_sprites.draw(screen)

def secondsToTime(seconds: int):
    hours = seconds // 3600
    minutes = seconds // 60 % 60
    text = ""
    if (hours > 0):
        word = wordWithNum(hours, "час", "часа", "часов")
        text += f"{hours} {word} и "
    word = wordWithNum(minutes, "минуту", "минуты", "минут")
    text += f"{minutes} {word}"
    return text
