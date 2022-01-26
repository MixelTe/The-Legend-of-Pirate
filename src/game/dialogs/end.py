import pygame
from functions import TextAnimator, getPosMult, getRectMult, load_image
from game.gameDialog import GameDialog
from settings import Settings


multRect = getRectMult(Settings.width, Settings.height)
multPos = getPosMult(Settings.width, Settings.height)
font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.053) + 1)
Text = "За таинственной дверью пирата ждал полностью целый корабль. Капитан собрал команду и продолжил свой путь."
background = pygame.transform.scale(load_image("background2.png"), (Settings.width, Settings.height))


class GameDialog_end(GameDialog):
    def __init__(self):
        super().__init__(lambda: None, Settings.width, Settings.height)
        self.surface.blit(background, (0, 0))
        self.text = TextAnimator(font, int(Settings.width * 0.0415) + 1, (Settings.width *
                          0.84, Settings.height), Text, pygame.Color(81, 44, 40))

    def close(self):
        if (self.text.stop):
            self.closed = True
            self.exitFromGame = True
        else:
            self.text.toEnd()

    def onMouseUp(self, pos: tuple[int, int]):
        super().onMouseUp(pos)
        self.close()

    def onKeyUp(self, key):
        if (key == pygame.K_ESCAPE or key == pygame.K_SPACE or key == pygame.K_RETURN):
            self.close()

    def onJoyButonUp(self, button):
        if (button == 0):
            self.close()

    def update(self):
        self.text.update()
        return super().update()

    def draw(self):
        self.surface.blit(background, (0, 0))
        self.surface.blit(self.text.draw(), multPos((0.08, 0.08)))
        return self.surface
