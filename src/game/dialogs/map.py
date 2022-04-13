import pygame
from functions import getPosMult, load_image
from game.gameDialog import GameDialog
from settings import Settings


multPos = getPosMult(Settings.width * 0.9, Settings.height * 0.9)

map1 = pygame.transform.scale(load_image("mapImg1.png"), (int(Settings.width * 0.9), int(Settings.height * 0.9)))
map2 = pygame.transform.scale(load_image("mapImg2.png"), (int(Settings.width * 0.9), int(Settings.height * 0.9)))


class GameDialog_map(GameDialog):
    def __init__(self, parts):
        super().__init__(lambda: None, *multPos((1, 1)), True)
        self.surface.fill((0, 0, 0, 0))
        if (parts > 0):
            self.surface.blit(map1, (0, 0))
        if (parts > 1):
            self.surface.blit(map2, (0, 0))

    def close(self):
        self.closed = True

    def onMouseUp(self, pos: tuple[int, int]):
        super().onMouseUp(pos)
        self.close()

    def onKeyUp(self, key):
        if (key == pygame.K_ESCAPE or key == pygame.K_SPACE or key == pygame.K_RETURN or key == pygame.K_q):
            self.close()

    def onJoyButonUp(self, button):
        if (button == 0 or button == 3):
            self.close()
