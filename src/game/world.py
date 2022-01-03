from game.entityPlayer import EntityPlayer
from game.screen import Screen
from saveData import SaveData
from windowGame import WindowGame


class World:
    def __init__(self, name: str):
        WindowGame.worlds[name] = self
        # загрузка ScreenData и size
        self.name = name
        self.size: tuple[int, int]
        self.screens: dict[(int, int), ScreenData]

    def screenExist(self, x: int, y: int) -> bool:
        # проверка существует ли экран с такими координатами
        pass

    def createScreen(self, x: int, y: int, saveData: SaveData, player: EntityPlayer) -> Screen:
        pass


class ScreenData:
    def __init__(self):
        self.tiles: list[list[str]] = []
        self.entity: list[dict] = []
