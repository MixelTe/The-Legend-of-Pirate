from __future__ import annotations
import pygame

from game.animator import Animator


class Entity:
    entityDict: dict[str, Entity] # словарь всех Entity для метода Entity.fromData
    def __init__(self, screen: pygame.Screen):
        self.screen = screen # экран, для доступа к списку сущностей и к клеткам мира
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

    def fromData(data: dict) -> Entity:
        # создаёт сущность из данных. И вызывает у него applyData(data)
        pass

    def applyData(self, data: dict):
        # установка значений полей из соответствующих полей данных
        pass

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        pass

    def move(self): # -> None | Entity | Tile
        # просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку
        pass

    def remove(self):
        # удаляет себя из списка сущностей
        pass


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

    def takeDamage(damage: int):
        # Уменьшение здоровья и установка damageDelay в Settings.damageDelay, если damageDelay <= 0
        pass
