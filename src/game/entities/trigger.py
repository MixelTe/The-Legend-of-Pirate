from typing import Any, Callable
from game.dialogs.end import GameDialog_end
from game.entity import Entity


class EntityTrigger(Entity):
    def __init__(self, screen, data: dict = None):
        self.zone = (0, 0, 0, 0)
        self.dialog = ""
        super().__init__(screen, data)
        self.hidden = True
        self.ghostE = True
        self.ghostT = True

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(data)
        dataSetter("zone", self.zone)
        dataSetter("dialog", self.dialog)

    def update(self):
        if (self.screen.player.is_inRect(self.zone)):
            if (self.dialog == "end"):
                self.screen.openDialog(GameDialog_end())


Entity.registerEntity("trigger", EntityTrigger)
