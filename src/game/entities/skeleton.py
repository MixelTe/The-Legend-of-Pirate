from typing import Any, Callable
from functions import compare, dropCoin, removeFromCollisions
from game.animator import Animator, AnimatorData
from game.entity import Entity, EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("skeleton", [
    ("stay.png", 0, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveW.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveS.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveA.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveD.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("attack.png", 250, (9, 13), (-0.15, -0.45, 0.69, 1)),
])


class EntitySkeleton(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.moveStyle = "ver"  # ver, hor
        self.dirR = True
        self.rise = True
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.speed = 0.05
        self.strength = 0
        self.healthMax = 2
        self.health = 2
        self.width = 0.4
        self.height = 0.55
        self.state = "go"
        self.pastCoord = self.y
        self.attackDelay = 0
        self.bone = None

        if (self.checkInTrap()):
            self.state = "stay"

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("moveStyle", self.moveStyle)
        dataSetter("dirR", self.dirR)
        dataSetter("rise", self.rise)

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        dropCoin(self)

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["player"])
        if (not self.alive or Settings.disableAI):
            return
        self.attackDelay = max(self.attackDelay - 1000 / Settings.fps, 0)
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
                    nx = int(self.x) + (1 if self.dirR else -1)
                    collisions = self.predictCollisions(nx + 0.1, int(self.y) + 0.1, 0.8, 0.8)
                    removeFromCollisions(collisions, ["player"])
                    if (len(collisions) != 0):
                        self.dirR = not self.dirR
                        self.x = int(self.x) + (1 - self.width) / 2
                        self.state = "rise"
                        self.pastCoord = self.y
                        ny = int(self.y) + (-1 if self.rise else 1)
                        collisions = self.predictCollisions(int(self.x) + 0.1, ny + 0.1, 0.8, 0.8)
                        removeFromCollisions(collisions, ["player"])
                        if (len(collisions) != 0):
                            self.rise = not self.rise
                        self.animator.setAnimation("moveW" if self.rise else "moveS")
                        self.speedX = 0
                        self.speedY = self.speed * (-1 if self.rise else 1)
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
                    ny = int(self.y) + (-1 if self.dirR else 1)
                    collisions = self.predictCollisions(int(self.x) + 0.1, ny + 0.1, 0.8, 0.8)
                    removeFromCollisions(collisions, ["player"])
                    if (len(collisions) != 0):
                        self.dirR = not self.dirR
                        self.y = int(self.y) + (1 - self.height) / 2
                        self.state = "rise"
                        self.pastCoord = self.x
                        nx = int(self.x) + (1 if self.rise else -1)
                        collisions = self.predictCollisions(nx + 0.1, int(self.y) + 0.1, 0.8, 0.8)
                        removeFromCollisions(collisions, ["player"])
                        if (len(collisions) != 0):
                            self.rise = not self.rise
                        self.animator.setAnimation("moveD" if self.rise else "moveA")
                        self.speedY = 0
                        self.speedX = self.speed * (1 if self.rise else -1)
                if (self.state == "go"):
                    self.animator.setAnimation("moveW" if self.dirR else "moveS")
            if (self.state == "go" and self.screen.player.visibleForEnemies):
                self.attack()
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
        elif (self.state == "attack"):
            if (self.animator.lastState[1]):
                if (self.attackDelay <= 0):
                    self.state = "go"
                    if (self.checkInTrap()):
                        self.state = "stay"
                else:
                    self.animator.setAnimation("attack", 1)
            elif (self.animator.lastState[0]):
                self.attackDelay = 2000
                if (self.bone is not None):
                    self.screen.addEntity(self.bone)
                    self.bone = None
        elif (self.state == "stay"):
            self.animator.setAnimation("stay")
            if (self.screen.player.visibleForEnemies):
                self.attack()

    def attack(self):
        if (abs(self.x - self.screen.player.x) < self.screen.player.width or
                abs(self.y - self.screen.player.y) < self.screen.player.height):
            self.speedX = 0
            self.speedY = 0
            self.state = "attack"
            self.animator.setAnimation("attack")
            self.bone = EntityAlive.createById("bone", self.screen)
            if (abs(self.x - self.screen.player.x) < self.screen.player.width):
                self.bone.x = self.x + (self.width - self.bone.width) / 2
                if (self.screen.player.y >= self.y):
                    self.bone.y = self.y + self.height
                    self.bone.speedY = self.bone.speed
                else:
                    self.bone.y = self.y - self.height - self.bone.height
                    self.bone.speedY = -self.bone.speed
            if (abs(self.y - self.screen.player.y) < self.screen.player.height):
                self.bone.y = self.y + (self.height - self.bone.height) / 2
                if (self.screen.player.x >= self.x):
                    self.bone.x = self.x + self.width
                    self.bone.speedX = self.bone.speed
                else:
                    self.bone.x = self.x - self.width - self.bone.height
                    self.bone.speedX = -self.bone.speed

    def checkInTrap(self):
        top = self.get_tile(0, -1)[0]
        right = self.get_tile(1, 0)[0]
        bottom = self.get_tile(0, 1)[0]
        left = self.get_tile(-1, 0)[0]
        free = 0
        free += 1 if top and self.canGoOn(top) else 0
        free += 1 if right and self.canGoOn(right) else 0
        free += 1 if bottom and self.canGoOn(bottom) else 0
        free += 1 if left and self.canGoOn(left) else 0
        return free == 0


EntityAlive.registerEntity("skeleton", EntitySkeleton)
