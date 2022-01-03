from game.entity import Entity
from saveData import SaveData


class EntityPlayer:
    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = [False, False, False, False]
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.weapon: Entity = None
        self.message = ""

    def onKeyDown(self, key):
        pass

    def onKeyUp(self, key):
        pass

    def onJoyHat(self, value):
        pass

    def onJoyButonDown(self, button):
        pass

    def onJoyButonUp(self, button):
        pass
