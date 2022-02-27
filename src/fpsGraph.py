import pygame
from settings import Settings


class FpsGraph:
    def __init__(self):
        self.lenght = 300
        self.lineW = 1
        self.enabled = False

        self.data = [0] * self.lenght
        self.start = 0

    def add(self, num):
        self._moveStartBack()
        self.data[self.start] = num

    def _moveStartBack(self):
        self.start = (self.start - 1 + self.lenght) % self.lenght

    def draw(self, surface: pygame.Surface):
        for j in range(self.lenght):
            i = (j + self.start) % self.lenght
            num = self.data[i]
            p1 = (Settings.width - j * self.lineW, Settings.height)
            p2 = (Settings.width - j * self.lineW, Settings.height - max(num - 6, 0))
            pygame.draw.line(surface, self._getColor(num), p1, p2, self.lineW)
        p1 = (Settings.width - self.lenght * self.lineW, Settings.height - 10)
        p2 = (Settings.width, Settings.height - 10)
        pygame.draw.line(surface, "blue", p1, p2, self.lineW)
        p1 = (Settings.width - self.lenght * self.lineW, Settings.height - 22)
        p2 = (Settings.width, Settings.height - 22)
        pygame.draw.line(surface, "red", p1, p2, self.lineW)

    def _getColor(self, num):
        maxV = 30 - 16
        num = min(max(num - 16, 0), maxV)
        color = pygame.Color(0, 0, 0)
        color.hsla = ((1 - num / maxV) * 120, 100, 50, 100)
        return color
