from game.entity import Entity, EntityAlive
from game.saveData import SaveData


class EntityPlayer(EntityAlive):
    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = [False, False, False, False]
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.weapon: Entity = None
        self.message = ""
        self.x = saveData.checkPointX + (1 - self.width) / 2
        self.y = saveData.checkPointY + (1 - self.width) / 2

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
