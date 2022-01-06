from __future__ import annotations
from typing import Union
import pygame
from functions import GameExeption, multRect
from game.animator import Animator
from game.tile import Tile
from settings import Settings


class Entity:
    entityDict: dict[str, Entity] = {}  # словарь всех Entity для метода Entity.fromData

    def __init__(self, screen, data: dict = None):
        from game.screen import Screen
        self.screen: Screen = screen  # экран, для доступа к списку сущностей и к клеткам мира
        # группа к которой пренадлежит сущность, для определения нужно ли наносить урон (присваивать значение только с помощью полей класса EntityGroups)
        self.group = EntityGroups.neutral
        self.x: float = 0
        self.y: float = 0
        self.width: float = 1
        self.height: float = 1
        self.speed: float = 0
        self.speedX: float = 0
        self.speedY: float = 0
        self.image: pygame.Surface = None
        # область отрисовки изображения, относительно сущности.
        self.imgRect: tuple[float, float, float, float] = [0, 0, 1, 1]
        if (data):
            self.applyData(data)

    @staticmethod
    def fromData(data: dict, screen: pygame.Surface):
        clas = data["className"]
        if (clas in Entity.entityDict):
            return Entity.entityDict[clas](screen, data)
        raise GameExeption(f"Entity.fromData: no Entity with className: {clas}")

    def applyData(self, data: dict):
        self.x = data["x"]
        self.y = data["y"]

    def update(self):
        self.move()

    def draw(self, surface: pygame.Surface):
        rect = (self.imgRect[0] + self.x, self.imgRect[1] + self.y, self.imgRect[2], self.imgRect[3])
        rect = multRect(rect, Settings.tileSize)
        if (self.image is None):
            pygame.draw.rect(surface, "green", rect)
        else:
            surface.blit(self.image, (rect[0], rect[1]), (rect[2], rect[3]))

    def move(self) -> Union[tuple[None, None], tuple[tuple[int, int, int, int], Union[Tile, Entity]]]:
        # просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку
        nX = self.x + self.speedX
        nY = self.y + self.speedY
        newRect = pygame.Rect(*multRect((nX, nY, self.width, self.height), Settings.tileSize))
        for (tile, x, y) in self.screen.getTiles():
            if (not tile.solid):
                continue
            rect = (x, y, 1, 1)
            if (newRect.colliderect(multRect(rect, Settings.tileSize))):
                self.move_toEdge(rect)
                return [rect, tile]
        for entity in self.screen.entities:
            if (entity == self):
                continue
            rect = entity.get_rect()
            if (newRect.colliderect(multRect(rect, Settings.tileSize))):
                self.move_toEdge(rect)
                return [rect, entity]
        self.x = nX
        self.y = nY
        return (None, None)

    def move_toEdge(self, rect: tuple[int, int, int, int]):
        pos = self.get_relPos(rect)
        if (pos[0] < 0):
            self.x = rect[0] - self.width
        if (pos[0] > 0):
            self.x = rect[0]  + rect[2]
        if (pos[1] < 0):
            self.y = rect[1] - self.height
        if (pos[1] > 0):
            self.y = rect[1]  + rect[3]

    def get_relPos(self, rect: tuple[int, int, int, int]):
        pos = [0, 0]
        if (self.x + self.width <= rect[0]):
            pos[0] = -1
        if (self.x >= rect[0] + rect[2]):
            pos[0] = 1
        if (self.y + self.height <= rect[1]):
            pos[1] = -1
        if (self.y >= rect[1] + rect[3]):
            pos[1] = 1
        return pos[0], pos[1]

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def remove(self):
        self.screen.removeEntity(self)


class EntityGroups:
    neutral = 0
    player = 1
    enemy = 2


class EntityAlive(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator: Animator = None
        self.health = 1
        self.damageDelay = 0  # при вызове update уменьшается на 1000 / Settings.fps

    def takeDamage(self, damage: int):
        # Уменьшение здоровья и установка damageDelay в Settings.damageDelay, если damageDelay <= 0
        pass


def loadEntities():
    from game.entities.entityCrab import EntityCrab
    Entity.entityDict["Entity_Crab"] = EntityCrab
    from game.entities.entityShovel import EntityShovel
    Entity.entityDict["Entity_Shovel"] = EntityShovel


loadEntities()
