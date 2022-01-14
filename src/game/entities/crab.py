from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups


animatorData = AnimatorData("crab", [
    ("stay.png", 0, (20, 11), (0, 0, 1, 0.55)),
    ("attack.png", 150, (20, 11), (0, 0, 1, 0.55)),
    ("agr.png", 150, (20, 21), (0, 0, 1, 1.5)),
    ("sleep.png", 150, (20, 21), (0, 0, 1, 1.5)),
])


class EntityCrab(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "attack")
        self.group = EntityGroups.enemy
        self.strength = 1
        self.width = 1
        self.height = 0.55
        self.speed = 0.04
        self.speedX = self.speed
        self.speedY = self.speed

    def update(self):
        collisions = super().update()
        if (not self.alive):
            self.animator.setAnimation("stay")
            self.speedX = 0
            self.speedY = 0
            return
        for rect, collision in collisions:
            pos = self.get_relPos(rect)
            if (pos[0] > 0):
                self.speedX = self.speed
            if (pos[0] < 0):
                self.speedX = -self.speed
            if (pos[1] > 0):
                self.speedY = self.speed
            if (pos[1] < 0):
                self.speedY = -self.speed


EntityAlive.registerEntity("crab", EntityCrab)
