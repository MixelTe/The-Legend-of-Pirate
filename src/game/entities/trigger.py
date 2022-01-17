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
        self.width = 1
        self.height = 1

    def applyData(self, data: dict):
        super().applyData(data)
        if ("zone" in data):
            self.zone = data["zone"]
        if ("dialog" in data):
            self.dialog = data["dialog"]

    def update(self):
        if (self.screen.player.is_inRect(self.zone)):
            if (self.dialog == "end"):
                self.screen.openDialog(GameDialog_end())


Entity.registerEntity("trigger", EntityTrigger)
