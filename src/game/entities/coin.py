from functions import load_image, load_sound, scaleImg
from game.entity import Entity

sound_coin = load_sound("coin1.wav", "coin")


class EntityCoin(Entity):
    image = scaleImg(load_image("coin.png"), 0.33, 0.4)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityCoin.image
        self.hidden = True
        self.ghostE = True
        self.width = 0.33
        self.height = 0.4
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
                self.screen.saveData.coins += 1
                sound_coin.play()
                self.remove()


Entity.registerEntity("coin", EntityCoin)
