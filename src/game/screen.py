from __future__ import annotations
from typing import Callable, Literal, Union
import pygame
from functions import GameExeption
from game.decor import Decor
from game.entity import Entity
from game.entityPlayer import EntityPlayer
from game.tile import Tile
from game.world import ScreenData, World
from game.saveData import SaveData
from settings import Settings
from random import randint, choices


class Screen:
    def __init__(self, world: World, data: ScreenData, pos: tuple[int, int], saveData: SaveData, player: EntityPlayer, openDialog: Callable):
        self.surface = pygame.Surface((Settings.width, Settings.height - Settings.overlay_height))
        self.pos = pos
        self.saveData = saveData
        self.world = world
        self.player = player
        self.openDialog = openDialog
        self.tiles: list[list[Tile]] = []
        self.entities: list[Entity] = []
        self.decor: list[Decor] = []
        self.decorAbove: list[Decor] = []
        self.goToVar: ScreenGoTo = None

        for y in range(Settings.screen_height):
            row = []
            for x in range(Settings.screen_width):
                row.append(Tile.fromId(data.tiles[y][x]))
            self.tiles.append(row)

        for eData in data.entity:
            self.entities.append(Entity.fromData(eData, self))

        for dData in data.decor:
            decor = Decor.fromData(dData)
            if (decor.aboveAll):
                self.decorAbove.append(decor)
            else:
                self.decor.append(decor)

        self.entities.append(player)
        player.screen = self

        self.onCreate()

    def onCreate(self):
        places = []
        for tile, x, y in self.getTiles():
            if (tile.id.startswith("sand")):
                if (x - 1 >= 0 and not self.tiles[y][x - 1].solid):
                    places.append((x, y))

        for x, y in choices(places, k=min(randint(0, 2), len(places))):
            e = Entity.createById("dig_place", self)
            e.x = x
            e.y = y
            self.addEntity(e)

    def update(self) -> Union[None, ScreenGoTo]:
        self.entities.sort(key=lambda e: (e.drawPriority, e.y + e.height))
        for entity in self.entities:
            entity.preUpdate()
        for entity in self.entities:
            entity.update()
        return self.goToVar

    def draw(self) -> pygame.Surface:
        self.surface.fill("red")

        for (tile, x, y) in self.getTiles():
            tile.draw(self.surface, x, y)

        for decor in self.decor:
            decor.draw(self.surface)

        for entity in self.entities:
            entity.draw(self.surface)

        for decor in self.decorAbove:
            decor.draw(self.surface)

        return self.surface

    def addEntity(self, entity: Entity):
        self.entities.append(entity)

    def removeEntity(self, entity: Entity):
        if (entity in self.entities):
            self.entities.remove(entity)

    def goTo(self, world: str, screen: tuple[int, int], pos: tuple[int, int] = None):
        self.goToVar = ScreenGoTo(world, screen, self.surface, pos)

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
    def create(world: World, x: int, y: int, saveData: SaveData, player: EntityPlayer, openDialog: Callable) -> Screen:
        if (not world.screenExist(x, y)):
            raise GameExeption(f"Screen.create: screen not exist, x: {x}, y: {y}")
        return Screen(world, world[x, y], (x, y), saveData, player, openDialog)


class ScreenGoTo:
    def __init__(self, world: str, screen: tuple[int, int], image: pygame.Surface, pos: Union[tuple[int, int], None] = None):
        self.world = world
        self.screen = screen
        self.pos = pos
        self.image = image  # изображение последнего кадра этого экрана


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
