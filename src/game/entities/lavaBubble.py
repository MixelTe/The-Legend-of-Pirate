from random import randint
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
        self.counter = randint(500, 1500)

    def canGoOn(self, tile: Tile) -> bool:
        return True
        return "lava" in tile.tags

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return

        self.counter -= 1000 / Settings.fps
        if (self.state == "bubble"):
            if (self.counter <= 0):
                self.state = "jump"
                self.animator.setAnimation("stay")
                self.speedY = -0.125
        elif (self.state == "jump"):
            self.speedY += 0.003
            self.animator.setAnimation("stay" if self.speedY <= 0 else "stayS")
            if (self.speedY >= 0):
                if (self.y >= self.startPos[1] + self.height / 2):
                    self.state = "bubble"
                    self.speedY = 0
                    self.y = self.startPos[1] + self.height / 2
                    self.animator.setAnimation("bubble")
                    self.counter = randint(500, 1500)


EntityAlive.registerEntity("lavaBubble", EntityLavaBubble)
