import pygame
from functions import getPosMult, getRectMult, load_image, renderText
from game.gameDialog import GameDialog
from settings import Settings


multRect = getRectMult(Settings.width, Settings.height)
multPos = getPosMult(Settings.width, Settings.height)
font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.05) + 1)
Text = "Однажны юный капитан собрал свою команду и отправился в море за богатсвом и славой. Но по пути их ждал страшный ураган, во время которого капитан выпал за борт, а корабль помчался прямиком на рифы. К счатью его вынесло на берег ближайшего острова, где его ждали невероятные приключения."


class GameDialog_start(GameDialog):
    def __init__(self):
        super().__init__(lambda: None, Settings.width, Settings.height)
        text = renderText(font, int(Settings.width * 0.05) + 1, (Settings.width *
                          0.92, Settings.height), Text, pygame.Color(81, 44, 40))
        self.surface.blit(text, multPos((0.04, 0.04)))

    def onMouseUp(self, pos: tuple[int, int]):
        super().onMouseUp(pos)
        self.closed = True
