import pygame
from functions import getPosMult, getRectMult, load_image, renderText, scaleImg
from game.gameDialog import GameDialog
from settings import Settings


multRect = getRectMult(Settings.width, Settings.height)
multPos = getPosMult(Settings.width, Settings.height)
font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.053) + 1)
Text = "Однажны юный капитан собрал свою команду и отправился в море за богатсвом и славой. Но по пути их ждал страшный ураган, во время которого капитан выпал за борт, а корабль помчался прямиком на рифы. К счатью его вынесло на берег ближайшего острова, где его ждали невероятные приключения."
background = pygame.transform.scale(load_image("background2.png"), (Settings.width, Settings.height))
# img = load_image("background.png")


class GameDialog_start(GameDialog):
    def __init__(self):
        super().__init__(lambda: None, Settings.width, Settings.height)
        self.surface.blit(background, (0, 0))
        text = renderText(font, int(Settings.width * 0.0415) + 1, (Settings.width *
                          0.84, Settings.height), Text, pygame.Color(81, 44, 40))
        self.surface.blit(text, multPos((0.08, 0.08)))

    def onMouseUp(self, pos: tuple[int, int]):
        super().onMouseUp(pos)
        self.closed = True

    def onKeyUp(self, key):
        if (key == pygame.K_ESCAPE or key == pygame.K_SPACE or key == pygame.K_RETURN):
            self.closed = True

    def onJoyButonUp(self, button):
        if (button == 0):
            self.closed = True
