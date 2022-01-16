import pygame
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from random import randint

from settings import Settings


animatorData = AnimatorData("crab", [
    ("stay.png", 0, (20, 11), (0, 0, 1, 0.55)),
    ("attack.png", 150, (20, 11), (0, 0, 1, 0.55)),
    ("agr.png", 600, (20, 21), (0, -0.5, 1, 1.05)),
    ("sleep.png", 800, (20, 21), (0, -0.5, 1, 1.05)),
])


class EntityCrab(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "sleep")
        self.animator.setAnimation("sleep", randint(0, 3))
        self.group = EntityGroups.enemy
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 1
        self.height = 0.55
        self.state = "sleep"
        self.lookZone = (-3 + self.width / 2, -3 + self.height / 2, 6, 6)
        self.attackTime = 20
        self.attackShift = 1
        self.attackCounter = 0
        self.aX = 0
        self.aY = 0

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "red", self.lookZone, False, True, True)

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return
        if (self.state == "sleep"):
            if (self.is_inRectD(self.lookZone, self.screen.player)):
                self.state = "agr"
                self.animator.setAnimation("agr")
        elif (self.state == "agr"):
            if (not self.is_inRectD(self.lookZone, self.screen.player)):
                self.state = "sleep"
                self.animator.setAnimation("sleep")
            elif (self.animator.lastState[1]):
                self.state = "attack"
                self.animator.setAnimation("attack")
                dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
                dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
                self.speedX = dx / self.attackTime
                self.speedY = dy / self.attackTime
                self.attackCounter = 0
        elif (self.state == "attack"):
            if (self.attackCounter >= self.attackTime):
                self.speedX = 0
                self.speedY = 0
                self.state = "sleep"
                self.animator.setAnimation("sleep")
            self.attackCounter += 1

        # for rect, collision in collisions:
        #     pos = self.get_relPos(rect)
        #     if (pos[0] > 0):
        #         self.speedX = self.speed
        #     if (pos[0] < 0):
        #         self.speedX = -self.speed
        #     if (pos[1] > 0):
        #         self.speedY = self.speed
        #     if (pos[1] < 0):
        #         self.speedY = -self.speed


EntityAlive.registerEntity("crab", EntityCrab)
