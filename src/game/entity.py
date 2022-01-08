from __future__ import annotations
from typing import Union
import pygame
from functions import GameExeption, rectIntersection
from game.animator import Animator
from game.tile import Tile
from settings import Settings


screenBorders = [
    (-1, 0, 1, Settings.screen_height),
    (Settings.screen_width, 0, 1, Settings.screen_height),
    (0, -1, Settings.screen_width, 1),
    (0, Settings.screen_height, Settings.screen_width, 1),
]


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
        self.imagePos: tuple[float, float] = (0, 0)
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
        return self.move()

    def draw(self, surface: pygame.Surface):
        rect = (self.x * Settings.tileSize, self.y * Settings.tileSize,
                self.width * Settings.tileSize, self.height * Settings.tileSize)
        if (self.image is None):
            pygame.draw.rect(surface, "green", rect)
        else:
            surface.blit(self.image, (rect[0] + self.imagePos[0] * Settings.tileSize,
                         rect[1] + self.imagePos[1] * Settings.tileSize))
        if (Settings.drawHitboxes):
            pygame.draw.rect(surface, "cyan", rect, round(Settings.tileSize * 0.03125) + 1)

    def move(self) -> list[tuple[tuple[int, int, int, int], Union[Tile, Entity, None]]]:
        # просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку
        moveX = 1
        moveY = 1
        nX = self.x + self.speedX
        nY = self.y + self.speedY
        newRect = (nX, nY, self.width, self.height)
        colision = []
        for (tile, x, y) in self.screen.getTiles():
            rect = (x, y, 1, 1)
            if (not rectIntersection(newRect, rect)):
                continue
            if (tile.solid):
                pos = self.move_toEdge(rect)
                colision.append((rect, tile))
                if (not rectIntersection((nX, self.y, self.width, self.height), rect)):
                    nY = self.y
                    moveY = 0
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (not rectIntersection((self.x, nY, self.width, self.height), rect)):
                    nX = self.x
                    moveX = 0
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (pos[0] == 0 and pos[1] == 0):
                    self.pushOutside(rect)
                return colision
            else:
                nX = self.x + self.speedX * tile.speed * moveX
                nY = self.y + self.speedY * tile.speed * moveY

        for entity in self.screen.entities:
            if (entity == self):
                continue
            rect = entity.get_rect()
            if (rectIntersection(newRect, rect)):
                pos = self.move_toEdge(rect)
                colision.append((rect, entity))
                if (not rectIntersection((nX, self.y, self.width, self.height), rect)):
                    nY = self.y
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (not rectIntersection((self.x, nY, self.width, self.height), rect)):
                    nX = self.x
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (pos[0] == 0 and pos[1] == 0):
                    self.pushOutside(rect)
                return colision

        for rect in screenBorders:
            if (not rectIntersection(newRect, rect)):
                continue
            pos = self.move_toEdge(rect)
            colision.append((rect, None))
            if (not rectIntersection((nX, self.y, self.width, self.height), rect)):
                nY = self.y
                newRect = (nX, nY, self.width, self.height)
                continue
            if (not rectIntersection((self.x, nY, self.width, self.height), rect)):
                nX = self.x
                newRect = (nX, nY, self.width, self.height)
                continue
            if (pos[0] == 0 and pos[1] == 0):
                self.pushOutside(rect)
            return colision

        self.x = nX
        self.y = nY
        return colision

    def move_toEdge(self, rect: tuple[int, int, int, int]):
        pos = self.get_relPos(rect)
        if (pos[0] < 0):
            self.x = rect[0] - self.width
        if (pos[0] > 0):
            self.x = rect[0] + rect[2]
        if (pos[1] < 0):
            self.y = rect[1] - self.height
        if (pos[1] > 0):
            self.y = rect[1] + rect[3]
        return pos

    def pushOutside(self, rect: tuple[int, int, int, int]):
        hor_c = ((self.x + self.width / 2) - (rect[0] + rect[2] / 2)) / (rect[2] / 2 + self.width / 2)
        ver_c = ((self.y + self.height / 2) - (rect[1] + rect[3] / 2)) / (rect[3] / 2 + self.height / 2)
        if (abs(hor_c) > abs(ver_c)):
            if (hor_c > 0):
                self.x = rect[0] + rect[2]
            else:
                self.x = rect[0] - self.width
        else:
            if (ver_c > 0):
                self.y = rect[1] + rect[3]
            else:
                self.y = rect[1] - self.height

    def get_relPos(self, rect: tuple[int, int, int, int]):
        pos = [0, 0]
        # rect = pygame.Rect(*multRect(rect, Settings.tileSize))
        # this = pygame.Rect(*multRect((self.x, self.y, self.width, self.height), Settings.tileSize))

        # if (this.x + this.width <= rect[0]):
        #     pos[0] = -1
        # if (this.x >= rect[0] + rect[2]):
        #     pos[0] = 1
        # if (this.y + this.height <= rect[1]):
        #     pos[1] = -1
        # if (this.y >= rect[1] + rect[3]):
        #     pos[1] = 1

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
    playerSelf = 1
    player = 2
    enemy = 3


class EntityAlive(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator: Animator = None
        self.health = 1
        self.damageDelay = 0  # при вызове update уменьшается на 1000 / Settings.fps
        self.strength = 1
        self.alive = True
        self.immortal = False

    def takeDamage(self, damage: int):
        if (self.immortal):
            return
        if (self.damageDelay <= 0):
            self.damageDelay = Settings.demageDelay
            self.health -= damage
            if (self.health <= 0):
                self.alive = False

    def update(self):
        if (not self.alive):
            return (None, None)
        collisions = super().update()
        if (self.damageDelay > 0):
            self.damageDelay -= 1000 / Settings.fps
        for rect, collision in collisions:
            if (self.group == EntityGroups.player and isinstance(collision, EntityAlive)):
                if (collision.group == EntityGroups.enemy or
                        collision.group == EntityGroups.neutral):
                    collision.takeDamage(self.strength)
            if (self.group == EntityGroups.enemy and isinstance(collision, EntityAlive)):
                if (collision.group == EntityGroups.player or
                        collision.group == EntityGroups.playerSelf):
                    collision.takeDamage(self.strength)
            if (isinstance(collision, EntityAlive) and collision.group == EntityGroups.neutral):
                if (self.group == EntityGroups.playerSelf or
                    self.group == EntityGroups.player or
                        self.group == EntityGroups.enemy):
                    self.takeDamage(collision.strength)
        return collisions


def loadEntities():
    from game.entities.entityCrab import EntityCrab
    Entity.entityDict["crab"] = EntityCrab
    from game.entities.entityShovel import EntityShovel
    Entity.entityDict["shovel"] = EntityShovel


loadEntities()
