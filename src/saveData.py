class SaveData:
    def __init__(self, save: int):
        self.save = save
        self.saveVersion = 1
        self.checkPointX = 0
        self.checkPointY = 0
        self.world = "start"
        self.screen = (0, 0)
        self.coins = 0
        self.health = 3
        self.bullets = 0
        self.time = 0
        self.tags: list[str] = []

    def load(self):
        # если файла сохранения нет, то оставляет значения по умолчанию
        pass

    def save(self):
        pass
