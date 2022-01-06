from functions import joinPath
from settings import Settings
import os

class SaveData:
    def __init__(self, save: int):
        self.saveFile = save
        self.saveVersion = 1
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
        path = joinPath(Settings.folder_data, Settings.folder_save, f"{self.saveFile}.txt")
        if (not os.path.isfile(path)):
            return
        with open(path) as f:
            pass

    def save(self):
        pass
