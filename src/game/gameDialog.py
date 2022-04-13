import pygame
from settings import Settings


class GameDialog:
    def __init__(self, onClose=lambda: None, w=10, h=10, alpha=False):
        self.onClose = onClose
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.x = (Settings.width - self.rect.width) / 2
        self.rect.y = (Settings.height - self.rect.height) / 2
        if (alpha):
            self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        else:
            self.surface = pygame.Surface(self.rect.size)
        self.closed = False
        self.exitFromGame = False
        self.drawBack()

    def draw(self) -> pygame.Surface:
        return self.surface

    def drawBack(self):
        self.surface.fill("#5CA8A8")
        border = int(Settings.width * 0.035) + 1
        pygame.draw.rect(self.surface, pygame.Color(194, 133, 105), (0, 0, self.rect.width, self.rect.height), border)

    def update(self) -> bool:
        return self.closed

    def onMove(self, pos: tuple[int, int]):
        return (pos[0] - self.rect.x, pos[1] - self.rect.y)

    def onMouseUp(self, pos: tuple[int, int]):
        if (not self.rect.collidepoint(pos)):
            self.closed = True
        return (pos[0] - self.rect.x, pos[1] - self.rect.y)

    def onKeyUp(self, key):
        pass

    def onJoyHat(self, value):
        pass

    def onJoyAxis(self, axis, value):
        pass

    def onJoyButonUp(self, button):
        pass

