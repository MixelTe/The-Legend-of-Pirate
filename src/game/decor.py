from __future__ import annotations
from typing import Any, Callable
import pygame
from functions import GameExeption


class Decor:
    decorDict: dict[str, Decor] = {}
    aboveAll = False

    def __init__(self, data: dict=None):
        self.x: float = 0
        self.y: float = 0
        self.width: float = 0
        self.height: float = 0
        self.image: pygame.Surface = 0
        self.tags: list[str] = 0
        if (data):
            self.applyData(self.getDataSetter(data), data)

    @staticmethod
    def fromData(data: dict) -> Decor:
        clas = data["className"]
        if (clas in Decor.decorDict):
            return Decor.decorDict[clas](data)
        raise GameExeption(f"Decor.fromData: no Decor with className: {clas}")

    @staticmethod
    def registerDecor(id: str, entityClass):
        if (id in Decor.decorDict):
            raise GameExeption(f"Decor.registerEntity: id is already taken: {id}")
        Decor.decorDict[id] = entityClass

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        dataSetter("x", self.x)
        dataSetter("y", self.y)

    def getDataSetter(self, data: dict) -> Callable[[str, Any, str, Callable[[Any], Any]], None]:
        def setter(field: str, default: Any, fieldDest: str = None, fun: Callable[[Any], Any] = lambda x: x):
            if (fieldDest is None):
                fieldDest = field
            if (field in data):
                setattr(self, fieldDest, fun(data[field]))
            else:
                setattr(self, fieldDest, default)
        return setter

    def draw(self, surface: pygame.Surface):
        pass


def loadDecor():
    import game.decors.tileEdge


loadDecor()