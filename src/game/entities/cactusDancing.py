import pygame
from backMusic import getCurMusic, startMusicBreak
from functions import joinPath, load_sound
from game.entity import Entity, EntityAlive, EntityGroups
from game.animator import Animator, AnimatorData
from settings import Settings


animatorData = AnimatorData("cactusDancing", [
    ("stay.png", 0, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("appear.png", 200, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("cactus.png", 0, (16, 16), (-0.075, -0.075, 1, 1)),
    ("dancing.png", 200, (20, 24), (-0.3625, -0.9, 1.25, 1.5)),
])
musicPath = joinPath(Settings.folder_data, Settings.folder_sounds, "back", "background2.mp3")


class EntityCactusDancing(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.X = 0
        self.Y = 0
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "cactus")
        self.immortal = True
        self.width = 0.85
        self.height = 0.85
        self.group = EntityGroups.enemy
        self.speech = ""
        self.speechCounter = 0
        if (getCurMusic() == musicPath):
            self.animator.setAnimation("dancing")

    def applyData(self, data: dict):
        self.X = data["x"]
        self.Y = data["y"]

    def takeDamage(self, damage: int, attacker: Entity = None):
        if (self.animator.curAnimation() == "cactus" and attacker.id == "shovel"):
            self.animator.setAnimation("appear")
            self.animator.endDamageAnim()
            self.width = 0.5
            self.height = 0.6
            self.attackPushbackA = 0
            self.attackPushbackX = 0
            self.attackPushbackY = 0
            self.x = self.X + 0.17
            self.y = self.Y + 0.59
        if (self.animator.curAnimation() == "stay"):
            if (getCurMusic() != musicPath):
                self.animator.setAnimation("dancing")
                startMusicBreak(musicPath, 0.3)

    def update(self):
        super().update()
        if (self.animator.curAnimation() == "appear"):
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - self.animator.frame / 10
            if (self.animator.lastState[1]):
                self.x = self.X + 0.17
                self.y = self.Y + 0.59 - 0.4
                self.animator.setAnimation("dancing")
                if (getCurMusic() != musicPath):
                    startMusicBreak(musicPath, 0.3)
        elif (self.animator.curAnimation() == "cactus"):
            self.x = self.X
            self.y = self.Y
        else:
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - 0.4
        if (self.animator.curAnimation() == "dancing"):
            if (getCurMusic() != musicPath):
                self.animator.setAnimation("stay")


EntityAlive.registerEntity("cactusDancing", EntityCactusDancing)
