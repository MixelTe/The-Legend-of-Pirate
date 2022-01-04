from __future__ import annotations


class World:
    worlds: dict[str, World] = {}

    def __init__(self, name: str):
        World.worlds[name] = self
        # загрузка ScreenData и size
        self.name = name
        self.size: tuple[int, int]
        self.screens: dict[(int, int), ScreenData]

    def screenExist(self, x: int, y: int) -> bool:
        # проверка существует ли экран с такими координатами
        pass


class ScreenData:
    def __init__(self):
        self.tiles: list[list[str]] = []
        self.entity: list[dict] = []
