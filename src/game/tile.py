from __future__ import annotations
import pygame


class Tile:
    tileIds: dict[str, Tile]
    def __init__(self, image: str, solid: bool = False, digable: bool = False, speed: float = 1):
        # добавляет себя в tileIds по ключу image отрезав расширение файла (всё после первой точки)
        self.image: pygame.Surface
        self.speed = speed # множитель скорости клетки
        self.digable = digable # можно ли копать на этой клетке
        self.solid = solid # плотная ли клетка (стена)

    @staticmethod
    def fromId(id: str) -> Tile:
        # получить клетку по id из tileIds
        pass

    def draw(self, surface: pygame.Surface, x: int, y: int):
        pass
