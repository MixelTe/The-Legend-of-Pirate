from typing import Any, Callable
from functions import compare, removeFromCollisions
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("piranha", [
    ("stay.png", 0, (35, 32), (-0.05, -0.15, 1, 0.91)),
    ("moveA.png", 150, (35, 32), (-0.05, -0.15, 0.91, 1)),
    ("moveD.png", 150, (35, 32), (-0.05, -0.15, 0.91, 1)),
    ("moveW.png", 150, (32, 35), (-0.15, -0.05, 1, 0.91)),
    ("moveS.png", 150, (32, 35), (-0.15, -0.05, 1, 0.91)),
])


class EntityPiranha(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.moveStyle = "ver"  # ver, hor
        self.dirR = True
        self.rise = True
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.speed = 0.05
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 0.8
        self.height = 0.7
        self.state = "go"

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("moveStyle", self.moveStyle)
        dataSetter("dirR", self.dirR)
        dataSetter("rise", self.rise)

    def canGoOn(self, tile: Tile) -> bool:
        return "water" in tile.tags or "water-deep" in tile.tags

    def tileSpeed(self, tile: Tile) -> float:
        if ("water" in tile.tags):
            return 1.3
        return super().tileSpeed(tile)

    def onDeath(self):
        tile = self.get_tile()
        if (tile[0] and "water-deep" not in tile[0].tags):
            coin = EntityAlive.createById("coin", self.screen)
            self.screen.addEntity(coin)
            coin.x = self.x + self.width / 2
            coin.y = self.y + self.height / 2

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["player"])
        if (not self.alive or Settings.disableAI):
            return
        if (self.state == "go"):
            if (self.moveStyle == "ver"):
                self.speedX = self.speed * (1 if self.dirR else -1)
                self.speedY = 0
                self.y = int(self.y) + (1 - self.height) / 2
                rise = False
                if (self.dirR):
                    if (compare(self.x - int(self.x), ">=", (1 - self.width) / 2)):
                        rise = True
                else:
                    if (compare(self.x - int(self.x), "<=", (1 - self.width) / 2)):
                        rise = True
                if (rise or len(collisions) != 0):
                    ny = int(self.x) + (1 if self.dirR else -1) + (1 - self.width) / 2
                    collisions = self.predictCollisions(ny, self.y)
                    removeFromCollisions(collisions, ["player"])
                    if (len(collisions) != 0):
                        self.animator.setAnimation("moveW" if self.rise else "moveS")
                        self.dirR = not self.dirR
                        self.x = int(self.x) + (1 - self.width) / 2
                        self.speedX = 0
                        self.speedY = self.speed * (-1 if self.rise else 1)
                        self.state = "rise"
                        self.pastCoord = self.y
                        ny = int(self.y) + (-1 if self.rise else 1) + (1 - self.height) / 2
                        collisions = self.predictCollisions(self.x, ny)
                        removeFromCollisions(collisions, ["player"])
                        if (len(collisions) != 0):
                            self.rise = not self.rise
                if (self.state == "go"):
                    self.animator.setAnimation("moveD" if self.dirR else "moveA")
            else:
                self.speedY = self.speed * (-1 if self.dirR else 1)
                self.speedX = 0
                self.x = int(self.x) + (1 - self.width) / 2
                rise = False
                if (self.dirR):
                    if (compare(self.y - int(self.y), "<=", (1 - self.height) / 2)):
                        rise = True
                else:
                    if (compare(self.y - int(self.y), ">=", (1 - self.height) / 2)):
                        rise = True
                if (rise or len(collisions) != 0):
                    ny = int(self.y) + (-1 if self.dirR else 1) + (1 - self.height) / 2
                    collisions = self.predictCollisions(self.x, ny)
                    removeFromCollisions(collisions, ["player"])
                    if (len(collisions) != 0):
                        self.animator.setAnimation("moveD" if self.rise else "moveA")
                        self.dirR = not self.dirR
                        self.y = int(self.y) + (1 - self.height) / 2
                        self.speedY = 0
                        self.speedX = self.speed * (1 if self.rise else -1)
                        self.state = "rise"
                        self.pastCoord = self.x
                        nx = int(self.x) + (1 if self.rise else -1) + (1 - self.width) / 2
                        collisions = self.predictCollisions(nx, self.y)
                        removeFromCollisions(collisions, ["player"])
                        if (len(collisions) != 0):
                            self.rise = not self.rise
                if (self.state == "go"):
                    self.animator.setAnimation("moveW" if self.dirR else "moveS")
        elif (self.state == "rise"):
            if (self.moveStyle == "ver"):
                self.animator.setAnimation("moveW" if self.rise else "moveS")
                self.x = int(self.x) + (1 - self.width) / 2
                self.speedX = 0
                self.speedY = self.speed * (-1 if self.rise else 1)
                if (compare(abs(self.pastCoord - self.y), ">=", 1) or len(collisions) != 0):
                    self.y = int(self.y) + (1 - self.height) / 2
                    self.state = "go"
            else:
                self.animator.setAnimation("moveD" if self.rise else "moveA")
                self.y = int(self.y) + (1 - self.height) / 2
                self.speedY = 0
                self.speedX = self.speed * (1 if self.rise else -1)
                if (compare(abs(self.pastCoord - self.x), ">=", 1) or len(collisions) != 0):
                    self.x = int(self.x) + (1 - self.width) / 2
                    self.state = "go"


EntityAlive.registerEntity("piranha", EntityPiranha)
