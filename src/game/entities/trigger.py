from typing import Any, Callable
from functions import GameExeption
from game.dialogs.end import GameDialog_end
from game.entity import Entity

TRIGGER_TYPES = ["dialog", "travelToWorld", "checkpoint"]
# dialog:
#   value - dialog id
#   value2 - unused
#   value3 - unused
# travelToWorld:
#   value - world id
#   value2 - screen of the world
#   value3 - position in the screen
# checkpoint:
#   value - unused
#   value2 - unused
#   value3 - respawn point


class EntityTrigger(Entity):
    def __init__(self, screen, data: dict = None):
        self.zone = (0, 0, 0, 0)
        self.type = TRIGGER_TYPES[0]
        self.value = ""
        self.value2 = [0, 0]
        self.value3 = [0, 0]
        super().__init__(screen, data)
        self.hidden = True
        self.ghostE = True
        self.ghostT = True

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("zone", self.zone)
        dataSetter("type", self.type)
        if (self.type not in TRIGGER_TYPES):
            raise GameExeption("EntityTrigger.applyData: Unknown trigger type")
        dataSetter("value", self.value)
        dataSetter("value2", self.value2)
        dataSetter("value3", self.value3)

    def update(self):
        if (self.screen.player.is_inRect(self.zone)):
            if (self.type == TRIGGER_TYPES[0]):  # dialog
                if (self.value == "end"):
                    self.screen.openDialog(GameDialog_end())
            if (self.type == TRIGGER_TYPES[1]):  # travelToWorld
                self.screen.goTo(self.value, self.value2, self.value3)
            if (self.type == TRIGGER_TYPES[2]):  # checkpoint
                self.screen.player.saveData.checkPointX = self.value3[0]
                self.screen.player.saveData.checkPointY = self.value3[1]
                self.screen.player.saveData.screen = self.screen.pos
                self.screen.player.saveData.world = self.screen.world.name


Entity.registerEntity("trigger", EntityTrigger)
