from functions import load_image, scaleImg
from game.entity import Entity


class EntityHeart(Entity):
    image = scaleImg(load_image("hpF.png"), 0.5, 0.5)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityHeart.image
        self.hidden = True
        self.ghostE = True
        self.width = 0.5
        self.height = 0.6
        self.counter = 0
        self.speedY = -0.005

    def update(self):
        collisions = super().update()
        self.counter += 1
        if (self.counter >= 20):
            self.speedY *= -1
            self.counter = 0
        for rect, collision in collisions:
            if (collision == self.screen.player):
                self.screen.player.heal(1)
                self.remove()


Entity.registerEntity("heart", EntityHeart)
