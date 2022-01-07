from __future__ import annotations
from typing import Literal, Union
import pygame
from functions import GameExeption
from game.entity import Entity
from game.entityPlayer import EntityPlayer
from game.tile import Tile
from game.world import ScreenData, World
from game.saveData import SaveData
from settings import Settings


class Screen:
    def __init__(self, world: World, data: ScreenData, pos: tuple[int, int], saveData: SaveData, player: EntityPlayer):
        self.surface = pygame.Surface((Settings.width, Settings.height - Settings.overlay_height))
        self.pos = pos
        self.saveData = saveData
        self.world = world
        self.player = player
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
        player.screen = self

    def update(self) -> Union[None, ScreenGoTo]:
        for entity in self.entities:
            entity.update()
        return self.goToVar

    def draw(self) -> pygame.Surface:
        self.surface.fill("red")

        for (tile, x, y) in self.getTiles():
            tile.draw(self.surface, x, y)

        for entity in self.entities:
            entity.draw(self.surface)

        return self.surface

    def addEntity(self, entity: Entity):
        self.entities.append(entity)

    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)

    def goTo(self, world: str, screen: tuple[int, int]):
        self.goToVar = ScreenGoTo(world, screen, self.surface)

    def tryGoTo(self, dir: Union[Literal["up"], Literal["right"], Literal["down"], Literal["left"]]):
        pos = list(self.pos)
        if (dir == "up"):
            pos[1] -= 1
        if (dir == "right"):
            pos[0] += 1
        if (dir == "down"):
            pos[1] += 1
        if (dir == "left"):
            pos[0] -= 1
        if (self.world.screenExist(*pos)):
            self.goToVar = ScreenGoTo(self.world.name, pos, self.surface)
            return True
        return False

    def getTiles(self):
        return TileIterator(self.tiles)

    @staticmethod
    def create(world: World, x: int, y: int, saveData: SaveData, player: EntityPlayer) -> Screen:
        if (not world.screenExist(x, y)):
            raise GameExeption(f"Screen.create: screen not exist, x: {x}, y: {y}")
        return Screen(world, world[x, y], (x, y), saveData, player)


class ScreenGoTo:
    def __init__(self, world: str, screen: tuple[int, int], image: pygame.Surface):
        self.world = world
        self.screen = screen
        self.image = image # изображение последнего кадра этого экрана


class TileIterator:
    def __init__(self, tiles: list[list[Tile]]):
        self.tiles = tiles
        self.y = 0
        self.x = 0

    def __iter__(self):
        self.y = 0
        self.x = 0
        return self

    def __next__(self):
        if (self.y >= Settings.screen_height):
            raise StopIteration
        tile = self.tiles[self.y][self.x]
        x = self.x
        y = self.y
        self.x += 1
        if (self.x >= Settings.screen_width):
            self.x = 0
            self.y += 1
        return (tile, x, y)
