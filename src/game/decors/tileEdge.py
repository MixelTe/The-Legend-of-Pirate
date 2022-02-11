import pygame
from game.decor import Decor


class DecorTileEdge(Decor):
    def __init__(self, data: dict=None):
        super().__init__(data)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, "green", (100, 100, 50, 50))


Decor.registerDecor("tileEdge", DecorTileEdge)