from typing import Literal
from game.entity import EntityAlive, EntityGroups


class EntitySpear(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.group = EntityGroups.enemy
        self.immortal = True
        self.hidden = True
        self.ghostE = True
        self.ghostT = True
        self.strength = 2
        self.width = 0.4
        self.height = 0.2
        self.startX = 0
        self.startY = 0
        self.direction: Literal["A", "W", "D", "S"] = "S"
        self.stage = 0

    def update(self):
        super().update()

    def nextStage(self):
        if (self.direction == "D"):
            self.width = 0.4 + 0.18 * self.stage
            self.height = 0.7
            self.x = self.startX + 0.32
            self.y = self.startY
        elif (self.direction == "A"):
            self.width = 0.4 + 0.18 * self.stage
            self.height = 0.7
            self.x = self.startX - self.width
            self.y = self.startY
        elif (self.direction == "W"):
            self.width = 0.6
            self.height = 0.7 + 0.15 * self.stage
            self.x = self.startX - 0.4
            self.y = self.startY - self.height + 0.4
        else:
            self.width = 0.6
            self.height = 0.4 + 0.15 * self.stage
            self.x = self.startX + 0.2
            self.y = self.startY + 0.3
        self.stage += 1


EntityAlive.registerEntity("spear", EntitySpear)
