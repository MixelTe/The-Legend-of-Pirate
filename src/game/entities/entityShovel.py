from typing import Literal
from game.entity import EntityAlive, EntityGroups


class EntityShovel(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.group = EntityGroups.player
        self.immortal = True
        self.hidden = True
        self.ghostE = True
        self.ghostT = True
        self.strength = 1
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
            self.x = self.startX + self.screen.player.width
            self.y = self.startY
        elif (self.direction == "A"):
            self.width = 0.4 + 0.18 * self.stage
            self.height = 0.7
            self.x = self.startX - self.width
            self.y = self.startY
        elif (self.direction == "W"):
            self.width = self.screen.player.width
            self.height = 0.5 + 0.15 * self.stage
            self.x = self.startX
            self.y = self.startY - self.height
        else:
            self.width = self.screen.player.width
            self.height = 0.2 + 0.1 * self.stage
            self.x = self.startX
            self.y = self.startY + self.screen.player.height
        self.stage += 1


EntityAlive.registerEntity("shovel", EntityShovel)
