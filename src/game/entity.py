from __future__ import annotations
import pygame
from functions import GameExeption, multRect
from game.animator import Animator
from settings import Settings


class Entity:
    entityDict: dict[str, Entity] # словарь всех Entity для метода Entity.fromData
    def __init__(self, screen, data: dict=None):
        from game.screen import Screen
        self.screen: Screen = screen # экран, для доступа к списку сущностей и к клеткам мира
        self.group = EntityGroups.neutral # группа к которой пренадлежит сущность, для определения нужно ли наносить урон (присваивать значение только с помощью полей класса EntityGroups)
        self.x: float = 0
        self.y: float = 0
        self.width: int = 1
        self.height: int = 1
        self.speed: float = 0
        self.speedX: float = 0
        self.speedY: float = 0
        self.image: pygame.Surface = None
        self.hitbox: pygame.Rect = None # область для просчёта столкновений, относительно сущности.
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
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        multRect(rect, Settings.tileSize)
        if (self.image is None):
            pygame.draw.rect(surface, "green", rect)
        else:
            surface.blit(self.image, rect.topleft, rect.size)

    def move(self): # -> None | Entity | Tile
        # просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку
        pass

    def remove(self):
        self.screen.removeEntity(self)


class EntityGroups:
    neutral = 0
    player = 1
    enemy = 2


class EntityAlive(Entity):
    def __init__(self, screen: pygame.Screen):
        super().__init__(screen)
        self.animator: Animator = None
        self.health = 1
        self.damageDelay = 0 # при вызове update уменьшается на 1000 / Settings.fps

    def takeDamage(self, damage: int):
        # Уменьшение здоровья и установка damageDelay в Settings.damageDelay, если damageDelay <= 0
        pass
