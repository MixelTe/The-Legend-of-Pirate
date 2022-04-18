from functions import dropCoin
from game.entity import Entity
from game.animator import Animator, AnimatorData


animatorData = AnimatorData("stone", [
    ("stay.png", 0, (16, 16), (0, 0, 1, 1)),
    ("broken.png", 0, (16, 16), (0, 0, 1, 1)),
    ("breaking.png", 150, (16, 16), (0, 0, 1, 1)),
])


class EntityStone(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 1
        self.height = 1
        self.hit = False

    def update(self):
        self.animator.update()
        if (self.animator.curAnimation() == "breaking"):
            if (self.animator.lastState[1]):
                dropCoin(self)
                self.remove()
            return
        for e in self.get_entities(self.get_rect()):
            if (e.id == "shovel"):
                if (self.hit):
                    return
                self.hit = True
                if (self.animator.curAnimation() == "stay"):
                    self.animator.setAnimation("broken")
                else:
                    self.animator.setAnimation("breaking")
                return
        self.hit = False


Entity.registerEntity("stone", EntityStone)
