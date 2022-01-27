from functions import load_sound
from game.entity import Entity
from game.animator import Animator, AnimatorData


animatorData = AnimatorData("cannon", [
    ("stay.png", 0, (11, 12), (0, 0, 1, 1)),
    ("fire.png", 200, (11, 12), (0, 0, 1, 1)),
])
sound_shoot = load_sound("cannonShot.wav")


class EntityCannon(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 1
        self.height = 1
        self.actionZone = (-0.5, -0.5, 2, 2)
        self.a = 0

    def update(self):
        super().update()
        self.speedY += self.a
        if (self.speedY < 0):
            self.speedY = 0
        if ("island-market-cannonball" in self.screen.saveData.tags
                and "island-door" not in self.screen.saveData.tags
                and self.is_inRectD(self.actionZone, self.screen.player)):
            self.screen.player.action = self.fire
        if (self.animator.curAnimation() == "fire" and self.animator.lastState[1]):
            self.animator.setAnimation("stay")
            sound_shoot.play()
            self.speedY = 0.25
            self.a = -0.05
            cannonball = Entity.createById("cannonball", self.screen)
            self.screen.addEntity(cannonball)
            cannonball.x = self.x + (self.width - cannonball.width) / 2
            cannonball.y = self.y
            cannonball.speedY = -0.1

    def fire(self):
        self.animator.setAnimation("fire")


Entity.registerEntity("cannon", EntityCannon)
