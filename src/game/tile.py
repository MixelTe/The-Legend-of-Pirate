from __future__ import annotations
import pygame
from functions import GameExeption, load_image
from settings import Settings


class Tile:
    tileIds: dict[str, Tile] = {}
    def __init__(self, image: str, solid: bool = False, digable: bool = False, speed: float = 1):
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (Settings.tileSize, Settings.tileSize))
        self.speed = speed # множитель скорости клетки
        self.digable = digable # можно ли копать на этой клетке
        self.solid = solid # плотная ли клетка (стена)
        key = image[:image.index(".")]
        Tile.tileIds[key] = self

    @staticmethod
    def fromId(id: str) -> Tile:
        if (id in Tile.tileIds):
            return Tile.tileIds[id]
        raise GameExeption(f"Tile.fromId: no tile with id: {id}")

    def draw(self, surface: pygame.Surface, x: int, y: int):
        surface.blit(self.image, (x * Settings.tileSize, y * Settings.tileSize))


Tile("sand1.png")
Tile("sand2.png")
Tile("sand3.png")
Tile("grass1.png")
Tile("grass2.png")
Tile("grass3.png")
Tile("water_deep.png", True)
Tile("water_low.png")
Tile("water_sand.png")