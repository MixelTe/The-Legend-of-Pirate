from functions import load_sound
from game.entity import Entity, EntityAlive, EntityGroups
from game.animator import Animator, AnimatorData


animatorData = AnimatorData("cactusDancing", [
    ("stay.png", 0, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("appear.png", 200, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("cactus.png", 0, (16, 16), (-0.075, -0.075, 1, 1)),
    ("dancing.png", 200, (20, 24), (-0.3625, -0.9, 1.25, 1.5)),
])

sound = load_sound("background2.mp3", "back")
sound.set_volume(0.5)
sound.get_num_channels()


class EntityCactusDancing(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "cactus")
        self.immortal = True
        self.width = 0.85
        self.height = 0.85
        self.group = EntityGroups.enemy
        self.speech = ""
        self.speechCounter = 0
        self.X = 0
        self.Y = 0
        if (sound.get_num_channels() != 0):
            self.animator.setAnimation("dancing")

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
            if (sound.get_num_channels() == 0):
                self.animator.setAnimation("dancing")
                sound.play()

    def update(self):
        super().update()
        if (self.animator.curAnimation() == "appear"):
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - self.animator.frame / 10
            if (self.animator.lastState[1]):
                self.x = self.X + 0.17
                self.y = self.Y + 0.59 - 0.4
                self.animator.setAnimation("dancing")
                if (sound.get_num_channels() == 0):
                    sound.play()
        elif (self.animator.curAnimation() == "cactus"):
            self.x = self.X
            self.y = self.Y
        else:
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - 0.4
        if (self.animator.curAnimation() == "dancing"):
            if (sound.get_num_channels() == 0):
                self.animator.setAnimation("stay")


EntityAlive.registerEntity("cactusDancing", EntityCactusDancing)
