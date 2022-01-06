from ntpath import join
from functions import GameExeption, joinPath
from settings import Settings
import os

class SaveData:
    def __init__(self, save: int):
        self.saveFile = save
        self.saveVersion = "1"
        self.checkPointX = 8
        self.checkPointY = 4
        # self.world = "start"
        self.world = "test"  # Temp
        self.screen = (0, 0)
        self.coins = 0
        self.health = 3
        self.bullets = 0
        self.time = 0
        self.tags: list[str] = []

    def load(self):
        path = joinPath(Settings.folder_data, Settings.folder_saves, f"{self.saveFile}.txt")
        if (not os.path.isfile(path)):
            return self
        with open(path, "r", encoding="utf-8") as f:
            def line():
                return f.readline().strip()
            saveVersion = line()
            if (saveVersion != self.saveVersion):
                raise GameExeption("Old save version")
            self.checkPointX, self.checkPointY = map(int, line().split())
            self.world = line()
            self.screen = tuple(map(int, line().split()))
            self.coins = int(line())
            self.health = int(line())
            self.bullets = int(line())
            self.time = int(line())
            self.tags = line().split(";")

        return self

    def save(self):
        path = joinPath(Settings.folder_data, Settings.folder_saves, f"{self.saveFile}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{self.saveVersion}\n")
            f.write(f"{self.checkPointX} {self.checkPointY}\n")
            f.write(f"{self.world}\n")
            f.write(f"{self.screen[0]} {self.screen[1]}\n")
            f.write(f"{self.coins}\n")
            f.write(f"{self.health}\n")
            f.write(f"{self.bullets}\n")
            f.write(f"{self.time}\n")
            f.write(";".join(self.tags))
