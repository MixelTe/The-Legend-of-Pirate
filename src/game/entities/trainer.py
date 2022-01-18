from random import choice
from game.entity import Entity, EntityAlive, EntityGroups
from game.animator import Animator, AnimatorData
from settings import Settings


animatorData = AnimatorData("trainer", [
    ("stay.png", 0, (9, 18), (0, -0.8, 0.75, 1.5)),
    ("attacked.png", 20, (9, 18), (0, -0.8, 0.75, 1.5)),
])


class EntityTrainer(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.immortal = True
        self.width = 0.75
        self.height = 0.7
        self.group = EntityGroups.enemy
        self.speech = ""
        self.speechCounter = 0

    def takeDamage(self, damage: int, attacker: Entity = None):
        super().takeDamage(damage, attacker)
        if (attacker != self.screen.player):
            if (self.animator.curAnimation() != "attacked"):
                self.animator.setAnimation("attacked")
                self.speech = choice(["Ой!", "Ай!", "Эй, я всего лишь манекен!"])

    def update(self):
        super().update()
        if (self.speech != ""):
            self.screen.player.message = self.speech
            self.speechCounter += 1000 / Settings.fps
            if (self.speechCounter >= 1500):
                self.speech = ""
                self.speechCounter = 0
        if (self.animator.curAnimation() == "attacked" and self.animator.lastState[1]):
            self.animator.setAnimation("stay")


EntityAlive.registerEntity("trainer", EntityTrainer)
