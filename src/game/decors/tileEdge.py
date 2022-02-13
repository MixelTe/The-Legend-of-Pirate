from typing import Any, Callable
import pygame
from functions import load_decor
from game.decor import Decor
from settings import Settings


class DecorTileEdge(Decor):
    images = {}

    def __init__(self, data: dict = None):
        self.sides = (False, False, False, False)  # top, right, bottom, left
        super().__init__(data)
        self.image: pygame.Surface = None
        self.create(self.sides)

    @staticmethod
    def load(images: dict, folder="tileEdge_water"):
        images["top"] = load_decor("top.png", folder)
        images["top-right"] = load_decor("top_right.png", folder)
        images["top-right-left"] = load_decor("top_right_left.png", folder)
        images["top-right-left-bottom"] = load_decor("top_right_left_bottom.png", folder)

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("sides", self.sides, "sides", lambda v: tuple(v))

    def create(self, sides: tuple[bool, bool, bool, bool]):
        img = pygame.Surface((16, 16), pygame.SRCALPHA)
        if (sides == (True, False, False, False)):
            img.blit(self.images["top"], (0, 0))
        elif (sides == (False, True, False, False)):
            img.blit(pygame.transform.rotate(self.images["top"], 270), (0, 0))
        elif (sides == (False, False, True, False)):
            img.blit(pygame.transform.rotate(self.images["top"], 180), (0, 0))
        elif (sides == (False, False, False, True)):
            img.blit(pygame.transform.rotate(self.images["top"], 90), (0, 0))
        elif (sides == (True, True, False, False)):
            img.blit(self.images["top-right"], (0, 0))
        elif (sides == (False, True, True, False)):
            img.blit(pygame.transform.rotate(self.images["top-right"], 270), (0, 0))
        elif (sides == (False, False, True, True)):
            img.blit(pygame.transform.rotate(self.images["top-right"], 180), (0, 0))
        elif (sides == (True, False, False, True)):
            img.blit(pygame.transform.rotate(self.images["top-right"], 90), (0, 0))
        elif (sides == (True, True, False, True)):
            img.blit(self.images["top-right-left"], (0, 0))
        elif (sides == (True, True, True, False)):
            img.blit(pygame.transform.rotate(self.images["top-right-left"], 270), (0, 0))
        elif (sides == (False, True, True, True)):
            img.blit(pygame.transform.rotate(self.images["top-right-left"], 180), (0, 0))
        elif (sides == (True, False, True, True)):
            img.blit(pygame.transform.rotate(self.images["top-right-left"], 90), (0, 0))
        elif (sides == (True, True, True, True)):
            img.blit(self.images["top-right-left-bottom"], (0, 0))

        self.image = pygame.transform.scale(img, (Settings.tileSize, Settings.tileSize))

    def draw(self, surface: pygame.Surface):
        if (self.image):
            surface.blit(self.image, (self.x * Settings.tileSize, self.y * Settings.tileSize))


class DecorTileEdge_water(DecorTileEdge):
    images = {}
    pass


DecorTileEdge_water.load(DecorTileEdge_water.images)
Decor.registerDecor("tileEdge_water", DecorTileEdge_water)


class DecorTileEdge_waterDeep(DecorTileEdge):
    images = {}
    pass


DecorTileEdge_water.load(DecorTileEdge_waterDeep.images, "tileEdge_water_deep")
Decor.registerDecor("tileEdge_water_deep", DecorTileEdge_waterDeep)


class DecorTileEdge_sand(DecorTileEdge):
    images = {}
    pass


DecorTileEdge_water.load(DecorTileEdge_sand.images, "tileEdge_sand")
Decor.registerDecor("tileEdge_sand", DecorTileEdge_sand)