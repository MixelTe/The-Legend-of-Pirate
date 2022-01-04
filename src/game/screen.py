from __future__ import annotations
from typing import Union
import pygame
from functions import GameExeption
from game.entity import Entity
from game.entityPlayer import EntityPlayer
from game.tile import Tile
from game.world import ScreenData, World
from game.saveData import SaveData
from settings import Settings


class Screen:
    def __init__(self, world: World, data: ScreenData, saveData: SaveData, player: EntityPlayer):
        self.surface = pygame.Surface((Settings.width, Settings.height - Settings.overlay_height))
        self.saveData = saveData
        self.world = world
        self.tiles: list[list[Tile]] = []
        self.entities: list[Entity] = []
        self.goToVar: ScreenGoTo = None

        for y in range(Settings.screen_height):
            row = []
            for x in range(Settings.screen_width):
                row.append(Tile.fromId(data.tiles[y][x]))
            self.tiles.append(row)

        for eData in data.entity:
            self.entities.append(Entity.fromData(eData, self))
        self.entities.append(player)

    def update(self) -> Union[None, ScreenGoTo]:
        for entity in self.entities:
            entity.update()
        return self.goToVar

    def draw(self) -> pygame.Surface:
        self.surface.fill("red")

        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                self.tiles[y][x].draw(self.surface, x, y)

        for entity in self.entities:
            entity.draw(self.surface)

        return self.surface

    def addEntity(self, entity: Entity):
        self.entities.append(entity)

    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)

    def goTo(self, world: str, screen: tuple[int, int]):
        self.goToVar = ScreenGoTo(world, screen, self.surface)

    @staticmethod
    def create(world: World, x: int, y: int, saveData: SaveData, player: EntityPlayer) -> Screen:
        if (not world.screenExist(x, y)):
            raise GameExeption(f"Screen.create: screen not exist, x: {x}, y: {y}")
        return Screen(world, world[x, y], saveData, player)


class ScreenGoTo:
    def __init__(self, world: str, screen: tuple[int, int], image: pygame.Surface):
        self.world = world
        self.screen = screen
        self.image = image # изображение последнего кадра этого экрана
