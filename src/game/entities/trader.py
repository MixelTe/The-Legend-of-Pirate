from game.entity import Entity
from game.animator import AnimatorData, Animator

animatorData = AnimatorData("trader", [
    ("stay.png", 0, (14, 24), (0, -0.8, 0.75, 1.5)),
    ("trade.png", 1000, (14, 24), (0, -0.8, 0.75, 1.5)),
])

class EntityTrader(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 0.75
        self.height = 0.7
        self.imagePos = (0, -0.8)

    def somethingBought(self):
        self.animator.setAnimation("trade")

    def update(self):
        super().update()
        if (self.animator.anim == "trade"):
            if (self.animator.lastState[1]):
                self.animator.setAnimation("stay")


Entity.registerEntity("trader", EntityTrader)