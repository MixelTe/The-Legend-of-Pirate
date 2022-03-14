from __future__ import annotations
from typing import Union
from functions import GameExeption, joinPath, loadJSON
from settings import Settings


class World:
    worlds: dict[str, World] = {}

    def __init__(self, name: str):
        World.worlds[name] = self
        self.name = name
        self.size = (0, 0)
        self.screens: list[list[Union[ScreenData, None]]] = []
        self.load()

    def load(self):
        try:
            data = loadJSON(joinPath(Settings.folder_data, Settings.folder_worlds, self.name + ".json"))
            self.size = (data["width"], data["height"])
            for y in range(self.size[1]):
                row = []
                for x in range(self.size[0]):
                    d = data["map"][y][x]
                    if (data["map"][y][x] is None):
                        row.append(None)
                    else:
                        row.append(ScreenData(d))
                self.screens.append(row)

        except Exception as x:
            raise GameExeption(f"World.load: cannot load world: {self.name}\n" + str(x))

    def screenExist(self, x: int, y: int) -> bool:
        if (self.size[0] <= x or self.size[1] <= y or x < 0 or y < 0):
            return False
        return self[x, y] is not None

    @staticmethod
    def getWorld(id: str):
        if (id in World.worlds):
            return World.worlds[id]
        raise GameExeption(f"World.getWorld: no such world: '{id}'")

    def __getitem__(self, key: tuple[int, int]):
        x, y = key
        if (self.size[0] <= x or self.size[1] <= y):
            raise GameExeption(f"World.__getitem__: coords out of range: x: {x}, y: {y}, size: {self.size}")
        return self.screens[y][x]


class ScreenData:
    def __init__(self, data: dict):
        self.tiles: list[list[str]] = data["tiles"]
        self.entity: list[dict] = data["entity"]
        self.decor: list[dict] = data["decor"] if ("decor" in data) else []


World("SandWorld")
World("WaterWorld")
World("ForestWorld")
