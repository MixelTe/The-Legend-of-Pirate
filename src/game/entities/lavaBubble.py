from random import randint
from functions import distanceRects
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("lavaBubble", [
    ("stay.png", 0, (16, 16), (-0.25, -0.25, 1, 1)),
    ("stayS.png", 0, (16, 16), (-0.25, -0.25, 1, 1)),
    ("bubble.png", 500, (16, 16), (-0.25, -0.25, 1, 1)),
    ("moveA.png", 250, (16, 16), (-0.25, -0.25, 1, 1)),
    ("moveD.png", 250, (16, 16), (-0.25, -0.25, 1, 1)),
    ("moveW.png", 250, (16, 16), (-0.25, -0.25, 1, 1)),
    ("moveS.png", 250, (16, 16), (-0.25, -0.25, 1, 1)),
])


class EntityLavaBubble(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "bubble")
        self.group = EntityGroups.enemy
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 0.5625
        self.height = 0.5
        self.startPos = (int(self.x), int(self.y))
        self.state = "bubble"
        self.counter = randint(1500, 2500)
        self.lavaPathPast = (0, 0)
        self.attackD = (0, 0)
        self.speedXA = 0
        self.speedYA = 0

    def canGoOn(self, tile: Tile) -> bool:
        return "lava" in tile.tags or super().canGoOn(tile) or self.state == "jump"

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return

        untouchable = False
        self.counter = max(0, self.counter - 1000 / Settings.fps)
        if (self.state == "bubble"):
            untouchable = True
            self.animator.setAnimation("bubble")
            if (self.counter <= 0):
                self.state = "jump"
                self.animator.setAnimation("stay")
                self.speedY = -0.125
            else:
                self.startAttack()
        elif (self.state == "jump"):
            untouchable = True
            self.speedY += 0.003
            self.animator.setAnimation("stay" if self.speedY <= 0 else "stayS")
            if (self.speedY >= 0):
                if (self.y >= self.startPos[1] + self.height / 2):
                    self.state = "bubble"
                    self.speedY = 0
                    self.y = self.startPos[1] + self.height / 2
                    self.animator.setAnimation("bubble")
                    self.counter = randint(1500, 2500)
        elif (self.state == "charging"):
            untouchable = True
            self.speedX = 0
            self.speedY = 0
            self.counter -= 1000 / Settings.fps
            if (self.counter <= 0):
                self.state = "attack"
                attackTime = 500 / 1000 * Settings.fps
                dx, dy = self.attackD
                # if (abs(dx) > abs(dy)):
                #     self.animator.setAnimation("moveD" if dx > 0 else "moveA")
                # else:
                #     self.animator.setAnimation("moveS" if dy > 0 else "moveW")
                self.animator.setAnimation("moveS" if dy > 0 else "moveW")
                self.speedX = dx / attackTime * 2
                self.speedY = dy / attackTime * 2
                self.speedXA = (self.speedX ** 2 / (-2 * dx)) if (dx != 0) else 0
                self.speedYA = (self.speedY ** 2 / (-2 * dy)) if (dy != 0) else 0
        elif (self.state == "attack"):
            self.speedX += self.speedXA
            self.speedY += self.speedYA
            self.addLavaPath()
            if (abs(self.speedX) < abs(self.speedX + self.speedXA)
                or abs(self.speedY) < abs(self.speedY + self.speedYA)):
                self.state = "return"
        elif (self.state == "return"):
            dx = (self.startPos[0] + 0.5) - (self.x + self.width / 2)
            dy = (self.startPos[1] + 0.5) - (self.y + self.height / 2)
            self.addLavaPath()
            if (abs(self.speedX) < abs(self.speedX + self.speedXA)
                or abs(self.speedY) < abs(self.speedY + self.speedYA)):
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
                self.animator.setAnimation("moveD" if dx > 0 else "moveA")
                # if (abs(dx) > abs(dy)):
                #     self.animator.setAnimation("moveD" if dx > 0 else "moveA")
                # else:
                #     self.animator.setAnimation("moveS" if dy > 0 else "moveW")
            if (abs(dx) <= 0.01 and abs(dy) <= 0.01):
                self.state = "bubble"
                self.speedX = 0
                self.speedY = 0
            self.speedX += self.speedXA
            self.speedY += self.speedYA

        self.immortal = untouchable
        self.ghostE = untouchable
        self.hidden = untouchable
        self.strength = 0 if untouchable else 1

    def startAttack(self):
        if (not self.screen.player.visibleForEnemies):
            return
        attackRange = 4
        # if (distanceRects(self.get_rect(), self.screen.player.get_rect()) <= attackRange ** 2):
        if ((abs(self.x - self.screen.player.x) < self.screen.player.width and abs(self.y - self.screen.player.y) < attackRange) or
                (abs(self.y - self.screen.player.y) < self.screen.player.height and abs(self.x - self.screen.player.x) < attackRange)):
            self.returnTile = (int(self.x + self.width / 2), int(self.y + self.height / 2))
            self.state = "charging"
            self.chargingCounter = 0
            # dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
            # dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
            if (abs(self.x - self.screen.player.x) < self.screen.player.width):
                dx = 0
                dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
            else:
                dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
                dy = 0
            self.attackD = (dx, dy)

    def addLavaPath(self):
        if (abs(self.lavaPathPast[0] - self.x) < 0.6 and
            abs(self.lavaPathPast[1] - self.y) < 0.6):
            return
        self.lavaPathPast = (self.x, self.y)
        lavaPath = EntityAlive.createById("lavaPath", self.screen)
        self.screen.addEntity(lavaPath)
        lavaPath.x = self.x - (1 - self.width) / 2
        lavaPath.y = self.y - (1 - self.height) / 2


EntityAlive.registerEntity("lavaBubble", EntityLavaBubble)
