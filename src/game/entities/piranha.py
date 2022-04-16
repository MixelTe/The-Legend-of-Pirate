import math
from typing import Any, Callable
from functions import compare, distanceRects, dropCoin, removeFromCollisions
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("piranha", [
    ("stay.png", 0, (16, 16), (0, -0.4375, 1, 1)),
    ("moveA.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("moveD.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("moveW.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("moveS.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("swimA.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("swimD.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("swimW.png", 150, (16, 16), (0, -0.4375, 1, 1)),
    ("swimS.png", 150, (16, 16), (0, -0.4375, 1, 1)),
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
        self.width = 0.9
        self.height = 0.5
        self.speedXA = 0
        self.speedYA = 0
        self.state = "go"
        self.chargingCounter = 0
        self.returnTile = (0, 0)
        self.attackD = (0, 0)

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("moveStyle", self.moveStyle)
        dataSetter("dirR", self.dirR)
        dataSetter("rise", self.rise)

    def canGoOn(self, tile: Tile) -> bool:
        if (self.state == "attack" or self.state == "return"):
            return not tile.solid or "water-deep" in tile.tags
        return "water" in tile.tags or "water-deep" in tile.tags

    def tileSpeed(self, tile: Tile) -> float:
        if ("water" in tile.tags):
            return 1.3
        return super().tileSpeed(tile)

    def onDeath(self):
        tile = self.get_tile()
        if (tile[0] and not tile[0].solid):
            dropCoin(self)

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
                        self.animator.setAnimation("swimW" if self.rise else "swimS")
                        self.speedX = 0
                        self.speedY = self.speed * (-1 if self.rise else 1)
                if (self.state == "go"):
                    self.animator.setAnimation("swimD" if self.dirR else "swimA")
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
                        self.animator.setAnimation("swimD" if self.rise else "swimA")
                        self.speedY = 0
                        self.speedX = self.speed * (1 if self.rise else -1)
                if (self.state == "go"):
                    self.animator.setAnimation("swimW" if self.dirR else "swimS")
            if (self.state == "go"):
                self.startAttack()
        elif (self.state == "rise"):
            if (self.moveStyle == "ver"):
                self.animator.setAnimation("swimW" if self.rise else "swimS")
                self.x = int(self.x) + (1 - self.width) / 2
                self.speedX = 0
                self.speedY = self.speed * (-1 if self.rise else 1)
                if (compare(abs(self.pastCoord - self.y), ">=", 1) or len(collisions) != 0):
                    self.y = int(self.y) + (1 - self.height) / 2
                    self.state = "go"
            else:
                self.animator.setAnimation("swimD" if self.rise else "swimA")
                self.y = int(self.y) + (1 - self.height) / 2
                self.speedY = 0
                self.speedX = self.speed * (1 if self.rise else -1)
                if (compare(abs(self.pastCoord - self.x), ">=", 1) or len(collisions) != 0):
                    self.x = int(self.x) + (1 - self.width) / 2
                    self.state = "go"
            if (self.state == "rise"):
                self.startAttack()
        elif (self.state == "charging"):
            self.speedX = 0
            self.speedY = 0
            self.chargingCounter -= 1000 / Settings.fps
            if (self.chargingCounter <= 0):
                self.state = "attack"
                attackTime = 500 / 1000 * Settings.fps
                dx, dy = self.attackD
                if (abs(dx) > abs(dy)):
                    self.animator.setAnimation("moveD" if dx > 0 else "moveA")
                else:
                    self.animator.setAnimation("moveS" if dy > 0 else "moveW")
                self.speedX = dx / attackTime * 2
                self.speedY = dy / attackTime * 2
                self.speedXA = (self.speedX ** 2 / (-2 * dx)) if (dx != 0) else 0
                self.speedYA = (self.speedY ** 2 / (-2 * dy)) if (dy != 0) else 0
        elif (self.state == "attack"):
            self.speedX += self.speedXA
            self.speedY += self.speedYA
            if (abs(self.speedX) < abs(self.speedX + self.speedXA)
                or abs(self.speedY) < abs(self.speedY + self.speedYA)):
                self.state = "return"
        elif (self.state == "return"):
            dx = (self.returnTile[0] + 0.5) - (self.x + self.width / 2)
            dy = (self.returnTile[1] + 0.5) - (self.y + self.height / 2)
            tileUnder = self.get_tile()[0]
            if (tileUnder and (tileUnder.id == "water_deep" or tileUnder.id == "water_low")):
                a = math.atan2(dy, dx)
                self.speedX = math.cos(a) * self.speed
                self.speedY = math.sin(a) * self.speed
                if (abs(dx) > abs(dy)):
                    self.animator.setAnimation("swimD" if dx > 0 else "swimA")
                else:
                    self.animator.setAnimation("swimS" if dy > 0 else "swimW")
            else:
                if (abs(self.speedX) < abs(self.speedX + self.speedXA)
                    or abs(self.speedY) < abs(self.speedY + self.speedYA)
                    or ((abs(dx) > 0.4 or abs(dy) > 0.4) and self.speedXA == 0 and self.speedYA == 0)):
                    returnTime = 800 / 1000 * Settings.fps
                    dx = max(min(dx, 1), -1)
                    dy = max(min(dy, 1), -1)
                    if (abs(dx) <= 0.4 and abs(dy) <= 0.4):
                        self.speedX = dx / returnTime * 4
                        self.speedY = dy / returnTime * 4
                        self.speedXA = 0
                        self.speedYA = 0
                    else:
                        self.speedX = dx / returnTime * 2
                        self.speedY = dy / returnTime * 2
                        self.speedXA = (self.speedX ** 2 / (-2 * dx)) if (dx != 0) else 0
                        self.speedYA = (self.speedY ** 2 / (-2 * dy)) if (dy != 0) else 0
                    if (abs(dx) > abs(dy)):
                        self.animator.setAnimation("moveD" if dx > 0 else "moveA")
                    else:
                        self.animator.setAnimation("moveS" if dy > 0 else "moveW")
            if (abs(dx) <= 0.01 and abs(dy) <= 0.01):
                self.state = "go"
            self.speedX += self.speedXA
            self.speedY += self.speedYA

    def startAttack(self):
        if (not self.screen.player.visibleForEnemies):
            return
        attackRange = 4
        # if (distanceRects(self.get_rect(), self.screen.player.get_rect()) <= attackRange ** 2):
        if ((abs(self.x - self.screen.player.x) < self.screen.player.width and abs(self.y - self.screen.player.y) < attackRange) or
                (abs(self.y - self.screen.player.y) < self.screen.player.height and abs(self.x - self.screen.player.x) < attackRange)):
            self.returnTile = (int(self.x + self.width / 2), int(self.y + self.height / 2))
            self.state = "charging"
            self.chargingCounter = 400
            # dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
            # dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
            if (abs(self.x - self.screen.player.x) < self.screen.player.width):
                dx = 0
                dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
            else:
                dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
                dy = 0
            self.attackD = (dx, dy)


EntityAlive.registerEntity("piranha", EntityPiranha)
