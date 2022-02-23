from typing import Any, Callable
from game.animator import Animator, AnimatorData
from game.entity import Entity, EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("skeleton", [
    ("stay.png", 0, (9, 13), (-0.15, -0.45, 0.69, 1)),
])


class EntitySkeleton(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.speed = 0.05
        self.rise = True
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 0.4
        self.height = 0.55
        self.state = "go"
        self.dirR = True
        self.pastY = self.y

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        if ("direction" in data):
            self.dirR = data["direction"] == "right"
        if ("rise" in data):
            self.rise = bool(data["rise"])

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def update(self):
        collisions = super().update()
        removePlayerFromCollisions(collisions)
        if (not self.alive or Settings.disableAI):
            return
        if (self.state == "go"):
            self.speedX = self.speed * (1 if self.dirR else -1)
            self.speedY = 0
            rise = False
            if (self.dirR):
                if (self.x - int(self.x) >= (1 - self.width) / 2):
                    rise = True
            else:
                if (self.x - int(self.x) <= (1 - self.width) / 2):
                    rise = True
            if (rise):
                nx = int(self.x) + (1 if self.dirR else -1) + (1 - self.width) / 2
                collisions = self.predictCollisions(nx, self.y)
                removePlayerFromCollisions(collisions)
                if (len(collisions) != 0):
                    self.dirR = not self.dirR
                    self.x = int(self.x) + (1 - self.width) / 2
                    self.state = "rise"
                    self.pastY = self.y
                    ny = int(self.y) + (-1 if self.rise else 1) + (1 - self.height) / 2
                    collisions = self.predictCollisions(self.x, ny)
                    removePlayerFromCollisions(collisions)
                    if (len(collisions) != 0):
                        self.rise = not self.rise
        elif (self.state == "rise"):
            self.speedX = 0
            self.speedY = self.speed * (-1 if self.rise else 1)
            if (abs(self.pastY - self.y) >= 1 or len(collisions) != 0):
                self.y = int(self.y) + (1 - self.height) / 2
                self.state = "go"


def removePlayerFromCollisions(collisions: list):
    for i, (rect, obj) in enumerate(collisions):
        if (isinstance(obj, Entity)):
            if (obj.id == "player"):
                collisions.pop(i)
                return


EntityAlive.registerEntity("skeleton", EntitySkeleton)
